#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# Copyright 2019-2021 SkyWater PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This code is *alternatively* available under a BSD-3-Clause license, see
# details in the README.md at the top level and the license text at
# https://github.com/google/skywater-pdk-libs-sky130_bag3_pr/blob/master/LICENSE.alternative
#
# SPDX-License-Identifier: BSD-3-Clause OR Apache 2.0


from typing import Tuple, FrozenSet, List, Mapping, Any, Union, Optional

from dataclasses import dataclass

from pybag.enum import Orient2D
from pybag.core import BBox

from bag.layout.tech import TechInfo
from bag.layout.routing.grid import TrackSpec
from bag.util.immutable import ImmutableSortedDict, ImmutableList, Param

from xbase.layout.enum import MOSType, MOSPortType, MOSCutMode, MOSAbutMode, DeviceType
from xbase.layout.data import LayoutInfoBuilder, ViaInfo, CornerLayInfo
from xbase.layout.exception import ODImplantEnclosureError
from xbase.layout.mos.tech import MOSTech
from xbase.layout.mos.data import (
    MOSRowSpecs, MOSRowInfo, BlkExtInfo, MOSEdgeInfo, MOSLayInfo, ExtWidthInfo, LayoutInfo,
    ExtEndLayInfo, RowExtInfo
)
from ..util import add_base, add_base_mos, get_arr_edge_dim

MConnInfoType = Tuple[int, int, Orient2D, int, Tuple[str, str]]


@dataclass(eq=True, frozen=True)
class ConnInfo:
    w: int
    len_min: int
    sp_le: int
    orient: Orient2D
    via_w: int
    via_h: int
    via_sp: int
    via_bot_enc: int
    via_top_enc: int

    def get_via_info(self, via_type: str, xc: int, yc: int, bot_w: int, ortho: bool = True,
                     num: int = 1, nx: int = 1, ny: int = 1, spx: int = 0, spy: int = 0) -> ViaInfo:
        vw = self.via_w
        vh = self.via_h
        vsp = self.via_sp

        bot_orient = self.orient
        if ortho:
            bot_orient = bot_orient.perpendicular()

        if bot_orient is Orient2D.x:
            bot_encx = self.via_bot_enc
            bot_ency = (bot_w - vh) // 2
        else:
            bot_encx = (bot_w - vw) // 2
            bot_ency = self.via_bot_enc

        if self.orient is Orient2D.x:
            top_encx = self.via_top_enc
            top_ency = (self.w - vh) // 2
            vnx = num
            vny = 1
        else:
            top_encx = (self.w - vw) // 2
            top_ency = self.via_top_enc
            vnx = 1
            vny = num

        enc1 = (bot_encx, bot_encx, bot_ency, bot_ency)
        enc2 = (top_encx, top_encx, top_ency, top_ency)
        return ViaInfo(via_type, xc, yc, self.via_w, self.via_h, enc1, enc2,
                       vnx, vny, vsp, vsp, nx, ny, spx, spy)


class MOSTechSkywater130(MOSTech):
    ignore_vm_sp_le_layers: FrozenSet[str] = frozenset(('li1',))

    def __init__(self, tech_info: TechInfo, lch: int, arr_options: Mapping[str, Any]) -> None:
        MOSTech.__init__(self, tech_info, lch, arr_options)

    @property
    def can_draw_double_gate(self) -> bool:
        return False

    @property
    def has_double_guard_ring(self) -> bool:
        return True

    @property
    def blk_h_pitch(self) -> int:
        return self.mos_config['blk_h_pitch']

    @property
    def end_h_min(self) -> int:
        # return self.mos_config['imp_h_min'] // 2
        end_margin: int = self.mos_config['end_margin']
        return -(-end_margin//self.blk_h_pitch) * self.blk_h_pitch

    @property
    def min_sep_col(self) -> int:
        sd_pitch = self.sd_pitch
        od_spx: int = self.mos_config['od_spx']
        imp_od_encx: int = self.mos_config['imp_od_encx']
        imp_sp: int = self.mos_config['imp_same_sp']
        od_sep = max(od_spx, imp_sp + 2 * imp_od_encx)
        ans = -(-(od_sep + sd_pitch) // sd_pitch)

        return ans  # This is not enforcing even col spacing for smallest possible spacing

    @property
    def sub_sep_col(self) -> int:
        sd_pitch = self.sd_pitch
        od_spx: int = self.mos_config['od_spx']
        imp_od_encx: int = self.mos_config['imp_od_encx']
        imp_sp: int = self.mos_config['imp_diff_sp']
        od_sep = max(od_spx, imp_sp + 2 * imp_od_encx)
        ans = -(-(od_sep + sd_pitch) // sd_pitch)

        return ans + (ans & 1)

    @property
    def min_sub_col(self) -> int:
        return self.min_od_col

    @property
    def gr_edge_col(self) -> int:
        return self.min_od_col

    @property
    def min_od_col(self) -> int:
        lch = self.lch
        sd_pitch = self.sd_pitch
        od_po_extx = self.od_po_extx

        od_w_min: int = self.mos_config['mos_w_range'][0]
        return -(-max(0, od_w_min - 2 * od_po_extx - lch) // sd_pitch) + 1

    @property
    def abut_mode(self) -> MOSAbutMode:
        return MOSAbutMode.NONE

    @property
    def od_po_extx(self) -> int:
        return self.mos_config['od_po_extx']

    @property
    def well_w_edge(self) -> int:
        imp_od_encx: int = self.mos_config['imp_od_encx']
        nwell_imp: int = self.mos_config['nwell_imp']
        well_w_edge = -(self.sd_pitch - self.lch) // 2 + self.od_po_extx + nwell_imp + imp_od_encx
        return -(-well_w_edge // self.sd_pitch) * self.sd_pitch

    def get_max_col_spacing_from_tap(self, pad_prox: bool = True) -> int:
        """Gets maximum columns from nearest well tap rule.

        Parameters
        ----------
        pad_prox:  Union[str, int, bool]
            Proximity to signal pad to determine appropriate rule. Default True.
            If True, cell is assumed close to pad diffusion. If False, cell is
            assumed far from pad diffusion.
        """
        max_dist_tap_far = self.mos_config['latchup']['max_distance_from_tap__far']
        max_dist_tap_near = self.mos_config['latchup']['max_distance_from_tap__near']
        dist = max_dist_tap_near if pad_prox else max_dist_tap_far
        col_dist = dist // self.sd_pitch
        return col_dist

    def get_conn_info(self, conn_layer: int, is_gate: bool) -> ConnInfo:
        mconf = self.mos_config
        wire_info = mconf['g_wire_info' if is_gate else 'd_wire_info']

        idx = conn_layer - wire_info['bot_layer']
        w, is_horiz, v_w, v_h, v_sp, v_bot_enc, v_top_enc = wire_info['info_list'][idx]
        orient = Orient2D(int(is_horiz ^ 1))
        tech_info = self.tech_info
        lay, purp = tech_info.get_lay_purp_list(conn_layer)[0]
        # make sure minimum length satisfies via enclosure rule
        cur_len = 2 * v_top_enc + (v_w if is_horiz else v_h)
        len_min = tech_info.get_next_length(lay, purp, orient, w, cur_len, even=True)
        sp_le = tech_info.get_min_line_end_space(lay, w, purpose=purp, even=True)

        return ConnInfo(w, len_min, sp_le, orient, v_w, v_h, v_sp, v_bot_enc, v_top_enc)

    # noinspection PyMethodMayBeStatic
    def can_short_adj_tracks(self, conn_layer: int) -> bool:
        return False

    def get_track_specs(self, conn_layer: int, top_layer: int) -> List[TrackSpec]:
        assert conn_layer == 0, 'currently only work for conn_layer = 0'

        grid_info = self.mos_config['grid_info']

        return [TrackSpec(layer=lay, direction=Orient2D.y, width=vm_w,
                          space=vm_sp, offset=(num_sd * (vm_w + vm_sp)) // 2)
                for lay, vm_w, vm_sp, num_sd in grid_info if conn_layer <= lay <= top_layer]

    def get_edge_width(self, mos_arr_width: int, blk_pitch: int) -> int:
        # w_edge_min = self.mos_config['imp_od_encx'] + self.sd_pitch // 2
        # return = get_arr_edge_dim(mos_arr_width, w_edge_min, blk_pitch)
        edge_margin: int = self.mos_config['edge_margin']
        imp_od_encx: int = self.mos_config['imp_od_encx']
        od_extx = self.od_po_extx - (self.sd_pitch - self.lch) // 2
        num_sd = -(-(od_extx + imp_od_encx) // self.sd_pitch)
        return -(-edge_margin // self.sd_pitch) * self.sd_pitch + num_sd * self.sd_pitch

    def get_mos_row_info(self, conn_layer: int, specs: MOSRowSpecs, bot_mos_type: MOSType,
                         top_mos_type: MOSType, global_options: Param) -> MOSRowInfo:
        guard_ring: bool = specs.options.get('guard_ring', False)
        guard_ring_col: bool = specs.options.get('guard_ring_col', False)

        assert conn_layer == 0, 'currently only work for conn_layer = 0'

        blk_p = self.blk_h_pitch

        w = specs.width
        w_sub = specs.sub_width
        mos_type = specs.mos_type
        threshold = specs.threshold

        mconf = self.mos_config
        po_spy: int = mconf['po_spy']
        od_spy: int = mconf['od_spy']
        po_h_gate: int = mconf['po_h_gate']
        po_od_exty: int = mconf['po_od_exty']
        mg_imp_spy: int = mconf['mg_imp_spy']
        imp_h_min: int = mconf['imp_h_min']
        imp_od_ency: int = mconf['imp_od_ency']
        po_spy2 = po_spy // 2
        imp_h_min2 = imp_h_min // 2

        md_info = self.get_conn_info(0, False)
        od_vency = md_info.via_bot_enc
        md_top_vency = md_info.via_top_enc
        md_vency = md_info.via_top_enc
        md_spy = md_info.sp_le
        md_h_min = md_info.len_min
        v0_h = md_info.via_h

        if mos_type.is_substrate:
            mg_h = 0
        else:
            mg_info = self.get_conn_info(0, True)
            mg_h = mg_info.w

        po_yl = po_spy2
        po_yh_gate = po_yl + po_h_gate

        if mos_type.is_substrate:
            od_yl = po_spy2 + po_od_exty
        else:
            po_yc_gate = (po_yl + po_yh_gate) // 2
            gmd_yh = po_yc_gate + v0_h // 2 + md_vency
            gmd_yl = min(po_yc_gate - v0_h // 2 - md_vency, gmd_yh - md_h_min)
            # fix mg_imp spacing
            imp_yl = max(imp_h_min2, po_yc_gate + mg_h // 2 + mg_imp_spy)
            od_yl = imp_yl + imp_od_ency

            dmd_yl = gmd_yh + md_spy
            dvc_yl = dmd_yl + md_top_vency
            od_yl = max(od_yl, dvc_yl - od_vency)

        od_yh = od_yl + w
        po_yh = od_yh + po_od_exty
        blk_yh = max(od_yh + imp_od_ency + imp_h_min2, po_yh + po_spy2)
        blk_yh = -(-blk_yh // blk_p) * blk_p

        dmd_yl, dmd_yh, _ = self._get_conn_params(md_info, od_yl, od_yh)

        if guard_ring:
            dmd_yl = min(dmd_yl, od_yl)
            dmd_yh = max(dmd_yh, od_yh)

        if mos_type.is_substrate:
            gmd_yl, gmd_yh = dmd_yl, dmd_yh

        # return MOSRowInfo
        top_einfo = RowExtInfo(
            mos_type, threshold,
            ImmutableSortedDict(dict(
                mos_type=mos_type,
                margins=dict(
                    od=(blk_yh - od_yh, od_spy),
                    po=(blk_yh - po_yh, po_spy),
                    md=(blk_yh - dmd_yh, md_spy),
                ),
                guard_ring=guard_ring,
                guard_ring_col=guard_ring_col,
            )),
        )
        bot_einfo = RowExtInfo(
            mos_type, threshold,
            ImmutableSortedDict(dict(
                mos_type=mos_type,
                margins=dict(
                    od=(od_yl, od_spy),
                    po=(po_yl, po_spy),
                    md=(gmd_yl, md_spy),
                ),
                guard_ring=guard_ring,
                guard_ring_col=guard_ring_col,
            )),
        )
        info = dict(
            imp_y=(od_yl - imp_od_ency, od_yh + imp_od_ency),
            od_y=(od_yl, od_yh),
            po_y=(po_yh_gate, po_yh),
            po_y_gate=(po_yl, po_yh_gate),
        )

        if mos_type.is_substrate:
            g_y = ds_y = ds_g_y = sub_y = (dmd_yl, dmd_yh)
            g_m_y = (0, po_yl)
            ds_m_y = (po_yh, blk_yh)
        else:
            g_y = (gmd_yl, gmd_yh)
            g_m_y = (0, po_yl)
            ds_y = ds_g_y = sub_y = (dmd_yl, dmd_yh)
            ds_m_y = (po_yh, blk_yh)
        return MOSRowInfo(self.lch, w, w_sub, mos_type, specs.threshold, blk_yh, specs.flip,
                          top_einfo, bot_einfo, ImmutableSortedDict(info), g_y, g_m_y, ds_y,
                          ds_m_y, ds_g_y, sub_y, guard_ring=guard_ring, guard_ring_col=guard_ring_col)

    def get_ext_width_info(self, bot_row_ext_info: RowExtInfo, top_row_ext_info: RowExtInfo,
                           ignore_vm_sp_le: bool = False) -> ExtWidthInfo:
        assert not ignore_vm_sp_le, 'ignore_vm_sp_le is not supported'

        blk_p = self.blk_h_pitch

        bot_margins = bot_row_ext_info['margins']
        top_margins = top_row_ext_info['margins']
        ext_h_min = 0
        for key, (bot_val, sp) in bot_margins.items():
            top_info = top_margins.get(key, None)
            if top_info is not None:
                top_val = top_info[0]
                ext_h_min = max(ext_h_min, sp - (top_val + bot_val))
        w_min = -(-ext_h_min // blk_p)

        return ExtWidthInfo([], w_min)

    # noinspection PyMethodMayBeStatic
    def get_extension_regions(self, bot_info: RowExtInfo, top_info: RowExtInfo, height: int
                              ) -> Tuple[MOSCutMode, int, int]:
        bot_gr = bot_info.info['guard_ring'] or bot_info.info['guard_ring_col']
        top_gr = top_info.info['guard_ring'] or top_info.info['guard_ring_col']
        if bot_gr and top_gr:
            cut_mode = MOSCutMode.BOTH
            bot_exty = 0
            top_exty = 0
        elif _get_extend_bot_implant(bot_info, top_info):
            # split at top
            cut_mode = MOSCutMode.TOP
            bot_exty = height
            top_exty = 0
        else:
            # split at bottom
            cut_mode = MOSCutMode.BOT
            bot_exty = 0
            top_exty = height

        return cut_mode, bot_exty, top_exty

    def get_mos_conn_info(self, row_info: MOSRowInfo, conn_layer: int, seg: int, w: int, stack: int,
                          g_on_s: bool, options: Param) -> MOSLayInfo:
        assert conn_layer == 0, 'currently only work for conn_layer = 0'

        sep_g = options.get('sep_g', False)
        export_mid = options.get('export_mid', False)
        export_mid = export_mid and stack == 2

        sd_pitch = self.sd_pitch

        height = row_info.height
        row_type = row_info.row_type
        imp_y: Tuple[int, int] = row_info['imp_y']
        po_y_gate: Tuple[int, int] = row_info['po_y_gate']

        # compute gate wires location
        fg = seg * stack
        wire_pitch = stack * sd_pitch
        conn_pitch = 2 * wire_pitch
        num_s = seg // 2 + 1
        num_d = (seg + 1) // 2
        s_xc = 0
        d_xc = wire_pitch

        # get gate wires
        g_pitch = 2 * sd_pitch
        if g_on_s:
            g_xc = 0
            num_g = fg // 2 + 1
        else:
            g_xc = sd_pitch
            num_g = (fg + 1) // 2

        # draw device
        builder = LayoutInfoBuilder()
        od_y = self._add_mos_active(builder, row_info, 0, fg, w)

        # draw gate connection
        self._draw_g_conn(builder, sep_g, g_xc, po_y_gate, fg, g_pitch, g_on_s)

        # draw drain/source connections
        d0_info = self.get_conn_info(0, False)
        md_yl, md_yh, num_vc = self._get_conn_params(d0_info, od_y[0], od_y[1])
        md_y = (md_yl, md_yh)
        self._draw_ds_conn(builder, d0_info, od_y, md_y, num_vc,
                           d_xc, num_d, conn_pitch)
        self._draw_ds_conn(builder, d0_info, od_y, md_y, num_vc,
                           s_xc, num_s, conn_pitch)

        if export_mid:
            m_xc = sd_pitch
            num_m = fg + 1 - num_s - num_d
            m_info = (m_xc, num_m, wire_pitch)
            self._draw_ds_conn(builder, d0_info, od_y, md_y, num_vc,
                               m_xc, num_m, wire_pitch)
        else:
            m_info = None

        bbox = BBox(0, 0, fg * sd_pitch, height)

        edge_info = MOSEdgeInfo(mos_type=row_type, imp_y=imp_y, has_od=True)
        be = BlkExtInfo(row_type, row_info.threshold, False, ImmutableList([(fg, row_type)]),
                        ImmutableSortedDict())
        return MOSLayInfo(builder.get_info(bbox), edge_info, edge_info, be, be,
                          g_info=(g_xc, num_g, g_pitch), d_info=(d_xc, num_d, conn_pitch),
                          s_info=(s_xc, num_s, conn_pitch), m_info=m_info,
                          shorted_ports=ImmutableList([MOSPortType.G]))

    def _draw_g_conn(self, builder: LayoutInfoBuilder, sep_g: bool, g_xc: int,
                     po_y_gate: Tuple[int, int], fg: int, conn_pitch: int, g_on_s: bool) -> None:
        lch = self.lch
        sd_pitch = self.sd_pitch
        mconf = self.mos_config
        npc_w: int = mconf['npc_w']
        npc_h: int = mconf['npc_h']
        npc_w2 = npc_w // 2
        npc_h2 = npc_h // 2

        g0_info = self.get_conn_info(0, True)

        po_lp = self.tech_info.config['mos_lay_table']['PO']

        if g_on_s:
            g_xc = 0
            num_g = fg // 2 + 1
            po_xl_even = g_xc
            po_xh_even = g_xc + sd_pitch // 2 + lch // 2
            po_xl_odd = sd_pitch + sd_pitch // 2 - lch // 2
            po_xh_odd = 2 * sd_pitch
        else:
            g_xc = sd_pitch
            num_g = (fg + 1) // 2
            po_xl_even = sd_pitch // 2 - lch // 2
            po_xh_even = sd_pitch
            po_xl_odd = sd_pitch
            po_xh_odd = sd_pitch + sd_pitch // 2 + lch // 2

        builder.add_rect_arr(po_lp, BBox(po_xl_even, po_y_gate[0], po_xh_even, po_y_gate[1]),
                             nx=(fg - (fg // 2)), spx=conn_pitch)
        builder.add_rect_arr(po_lp, BBox(po_xl_odd, po_y_gate[0], po_xh_odd, po_y_gate[1]),
                             nx=(fg // 2), spx=conn_pitch)

        po_yc_gate = (po_y_gate[0] + po_y_gate[1]) // 2
        po_h_gate = sd_pitch - lch
        builder.add_via(g0_info.get_via_info('PYL1_C', g_xc, po_yc_gate, po_h_gate,
                                             ortho=False, num=1, nx=num_g, spx=conn_pitch))
        # poly via draws npc layer wrong
        npc_box = BBox(g_xc - npc_w2, po_yc_gate - npc_h2, g_xc + npc_w2, po_yc_gate + npc_h2)
        builder.add_rect_arr(('npc', 'drawing'), npc_box, nx=num_g, spx=conn_pitch)

        po_w_min = g0_info.len_min
        if sep_g:
            mp_xl = g_xc - po_w_min // 2
            builder.add_rect_arr(po_lp, BBox(mp_xl, po_y_gate[0], mp_xl + po_w_min, po_y_gate[1]),
                                 nx=num_g, spx=conn_pitch)
        else:
            mp_dx = g0_info.via_w
            mp_xl = g_xc - mp_dx
            mp_xh = g_xc + (num_g - 1) * conn_pitch + mp_dx
            builder.add_rect_arr(po_lp, BBox(mp_xl, po_y_gate[0], mp_xh, po_y_gate[1]))

    def _draw_ds_conn(self, builder: LayoutInfoBuilder, d0_info: ConnInfo,
                      od_y: Tuple[int, int], md_y: Tuple[int, int], num_vc: int,
                      xc: int, nx: int, spx: int) -> None:
        # connect to MD
        md_w = d0_info.w
        vc_w = d0_info.via_w
        vc_h = d0_info.via_h
        vc_sp = d0_info.via_sp
        vc_p = vc_w + vc_sp
        vc_w2 = vc_w // 2
        vc_h2 = vc_h // 2
        md_w2 = md_w // 2
        md_lp = self.tech_info.config['mos_lay_table']['MD']

        od_yc = (od_y[0] + od_y[1]) // 2
        vc_h_arr = num_vc * vc_p - vc_sp
        vc_yc_bot = od_yc + (vc_h - vc_h_arr) // 2
        vc_box = BBox(xc - vc_w2, vc_yc_bot - vc_h2, xc + vc_w2, vc_yc_bot + vc_h2)
        md_box = BBox(xc - md_w2, md_y[0], xc + md_w2, md_y[1])
        builder.add_rect_arr(('licon1', 'drawing'), vc_box, nx=nx, spx=spx, ny=num_vc, spy=vc_p)
        builder.add_rect_arr(md_lp, md_box, nx=nx, spx=spx)

    def get_mos_abut_info(self, row_info: MOSRowInfo, edgel: MOSEdgeInfo, edger: MOSEdgeInfo
                          ) -> LayoutInfo:
        raise ValueError('This method is not supported in this technology.')

    def get_mos_tap_info(self, row_info: MOSRowInfo, conn_layer: int, seg: int,
                         options: Param) -> MOSLayInfo:
        assert conn_layer == 0, 'currently only work for conn_layer = 0'
        row_type = row_info.row_type

        guard_ring: bool = options.get('guard_ring', row_info.guard_ring)
        guard_ring_col: bool = options.get('guard_ring_col', row_info.guard_ring_col)
        gr = guard_ring or guard_ring_col
        if gr:
            sub_type: MOSType = options.get('sub_type', row_type.sub_type)
        else:
            sub_type: MOSType = row_type.sub_type

        sd_pitch: int = self.sd_pitch

        w: int = row_info.sub_width
        height: int = row_info.height
        imp_y: Tuple[int, int] = row_info['imp_y']

        # draw device
        builder = LayoutInfoBuilder()
        # draws diffusion and tap
        od_y = self._add_mos_active(builder, row_info, 0, seg, w, is_sub=True, sub_type=sub_type)

        # draw drain/source connections
        d0_info = self.get_conn_info(0, False)
        md_yl, md_yh, num_vc = self._get_conn_params(d0_info, od_y[0], od_y[1])
        md_y = (md_yl, md_yh)
        if guard_ring:
            md_y = row_info.ds_conn_y

        # draws in vias connecting tap cell to metal 1
        self._draw_ds_conn(builder, d0_info, od_y, md_y, num_vc, 0, seg + 1, sd_pitch)

        bbox = BBox(0, 0, seg * sd_pitch, height)
        edge_info = MOSEdgeInfo(mos_type=sub_type, imp_y=imp_y, has_od=True)
        be = BlkExtInfo(row_type, row_info.threshold, gr, ImmutableList([(seg, sub_type)]),
                        ImmutableSortedDict())
        wire_info = (0, seg + 1, sd_pitch)
        return MOSLayInfo(builder.get_info(bbox), edge_info, edge_info, be, be,
                          g_info=wire_info, d_info=wire_info, s_info=wire_info,
                          shorted_ports=ImmutableList())

    def get_mos_space_info(self, row_info: MOSRowInfo, num_cols: int, left_info: MOSEdgeInfo,
                           right_info: MOSEdgeInfo) -> MOSLayInfo:
        lch = self.lch
        sd_pitch = self.sd_pitch
        od_po_extx = self.od_po_extx

        imp_od_encx: int = self.mos_config['imp_od_encx']

        row_type = row_info.row_type
        threshold = row_info.threshold
        imp_y: Tuple[int, int] = row_info['imp_y']

        blk_xh = num_cols * sd_pitch
        blk_yh = row_info.height
        bbox = BBox(0, 0, blk_xh, blk_yh)

        # get information from edge information dictionary
        # if MOSEdgeInfo evaluates to False, that means this space block is on the boundary.
        if left_info:
            typel: MOSType = left_info['mos_type']
            if right_info:
                typer: MOSType = right_info['mos_type']
            else:
                typer = typel
        elif right_info:
            typer: MOSType = right_info['mos_type']
            typel = typer
        else:
            typel = typer = row_type

        guard_ring = row_info.guard_ring or row_info.guard_ring_col

        builder = LayoutInfoBuilder()

        # find dummy OD columns
        od_extx = od_po_extx - (sd_pitch - lch) // 2
        delta_implant = od_extx + imp_od_encx
        delta_implant = -(-delta_implant // sd_pitch) * sd_pitch
        if typel == typer:
            # same implant on left and right
            if guard_ring and typel.is_substrate:
                raise ValueError('Cannot have empty spaces between guard ring edges.')

            be = BlkExtInfo(row_type, threshold, False, ImmutableList([(num_cols, typel)]),
                            ImmutableSortedDict())
            add_base(builder, typel, threshold, imp_y, bbox)
            edger = edgel = MOSEdgeInfo(mos_type=typel, imp_y=imp_y, has_od=False)
        else:
            # find implant split coordinate
            # split closer to the side with the following priority:
            # 1. is a opposite tap (i.e. ntap in nmos row)
            # 2. is a substrate tap (i.e. ptap in nmos row)
            if typel is not row_type:
                if delta_implant > blk_xh:
                    raise ODImplantEnclosureError('Insufficient space to satisfy '
                                                  'implant-OD horizontal enclosure.')
                add_base(builder, typel, threshold, imp_y, BBox(0, 0, delta_implant, blk_yh))
                xl = delta_implant
                fgl = delta_implant // sd_pitch
            else:
                xl = 0
                fgl = 0

            if typer is not row_type:
                xr = blk_xh - delta_implant
                if xr < xl:
                    raise ODImplantEnclosureError('Insufficient space to satisfy '
                                                  'implant-OD horizontal enclosure.')
                add_base(builder, typer, threshold, imp_y, BBox(xr, 0, blk_xh, blk_yh))
                fgr = delta_implant // sd_pitch
            else:
                xr = blk_xh
                fgr = 0

            if xr > xl:
                # draw implant in middle region
                fgm = (xr - xl) // sd_pitch
                if typel is row_type:
                    fgl += fgm
                    add_base(builder, typel, threshold, imp_y, BBox(xl, 0, xr, blk_yh))
                else:
                    fgr += fgm
                    add_base(builder, typer, threshold, imp_y, BBox(xl, 0, xr, blk_yh))

            fg_dev_list = []
            if fgl > 0:
                fg_dev_list.append((fgl, typel))
            if fgr > 0:
                fg_dev_list.append((fgr, typer))

            be = BlkExtInfo(row_type, threshold, guard_ring, ImmutableList(fg_dev_list),
                            ImmutableSortedDict())
            edgel = MOSEdgeInfo(mos_type=typel, imp_y=imp_y, has_od=False)
            edger = edgel.copy_with(mos_type=typer)

        wire_info = (0, 0, 0)
        return MOSLayInfo(builder.get_info(bbox), edgel, edger, be, be, g_info=wire_info,
                          d_info=wire_info, s_info=wire_info, shorted_ports=ImmutableList())

    def get_mos_ext_info(self, num_cols: int, blk_h: int, bot_einfo: RowExtInfo,
                         top_einfo: RowExtInfo, gr_info: Tuple[int, int]) -> ExtEndLayInfo:
        if _get_extend_bot_implant(bot_einfo, top_einfo):
            row_type = bot_einfo.row_type
            threshold = bot_einfo.threshold
        else:
            row_type = top_einfo.row_type
            threshold = top_einfo.threshold
        return self._get_mos_ext_info_helper(num_cols, blk_h, row_type, threshold)

    def get_mos_ext_gr_info(self, num_cols: int, edge_cols: int, blk_h: int, bot_einfo: RowExtInfo,
                            top_einfo: RowExtInfo, sub_type: MOSType, einfo: MOSEdgeInfo
                            ) -> ExtEndLayInfo:
        if _get_extend_bot_implant(bot_einfo, top_einfo):
            threshold = bot_einfo.threshold
        else:
            threshold = top_einfo.threshold
        return self._get_mos_ext_info_helper(num_cols, blk_h, sub_type, threshold, guard_ring=True)

    def _get_mos_ext_info_helper(self, num_cols: int, blk_h: int, row_type: MOSType, threshold: str,
                                 guard_ring: bool = False) -> ExtEndLayInfo:
        sd_pitch = self.sd_pitch

        blk_w = num_cols * sd_pitch
        blk_rect = BBox(0, 0, blk_w, blk_h)

        builder = LayoutInfoBuilder()

        if guard_ring:
            md_info = self.get_conn_info(0, False)
            v_w = md_info.via_w
            od_tap_extx = self.mos_config['od_tap_extx']  # determines the amount to extend material from licon
            od_sd_dx = od_tap_extx + v_w // 2

            od_lp = self.tech_info.config['mos_lay_table']['OD']['sub']
            md_lp = self.tech_info.config['mos_lay_table']['MD']
            od_xl = - od_sd_dx
            od_xr = sd_pitch * (num_cols - 1) + od_sd_dx
            builder.add_rect_arr(od_lp, BBox(od_xl, 0, od_xr, blk_h))
            builder.add_rect_arr(md_lp, BBox(od_xl, 0, od_xr, blk_h))
            blk_xl = od_xl - (blk_w - od_xr)
            blk_rect = BBox(blk_xl, 0, blk_w, blk_h)
            imp_y = (0, blk_h)
            imp_od_encx: int = self.mos_config['imp_od_encx']
            add_base_mos(builder, row_type, threshold, imp_y, blk_rect,
                         imp_x=(od_xl - imp_od_encx, od_xr + imp_od_encx), is_sub=row_type.is_substrate)
        else:
            imp_y = (0, 0)
            add_base(builder, row_type, threshold, imp_y, blk_rect)

        edge_info = MOSEdgeInfo(blk_h=blk_h, row_type=row_type, mos_type=row_type, threshold=threshold, imp_y=imp_y)
        return ExtEndLayInfo(builder.get_info(blk_rect), edge_info)

    def get_ext_geometries(self, re_bot: RowExtInfo, re_top: RowExtInfo,
                           be_bot: ImmutableList[BlkExtInfo], be_top: ImmutableList[BlkExtInfo],
                           cut_mode: MOSCutMode, bot_exty: int, top_exty: int,
                           dx: int, dy: int, w_edge: int) -> LayoutInfo:
        sd_pitch = self.sd_pitch
        well_w_edge = self.well_w_edge

        ymid = dy + bot_exty
        ytop = ymid + top_exty

        # draw extensions
        builder = LayoutInfoBuilder()
        if bot_exty > 0:
            xcur = dx
            for info in be_bot:
                xcur = _add_blk_ext_info(sd_pitch, builder, info, xcur, dy, ymid)
            w_tot = xcur + w_edge
            _add_blk_ext_edge(sd_pitch, builder, be_bot[0], dy, ymid, w_edge, 0, well_w_edge)
            _add_blk_ext_edge(sd_pitch, builder, be_bot[-1], dy, ymid, w_edge, w_tot, well_w_edge)
        if top_exty > 0:
            xcur = dx
            for info in be_top:
                xcur = _add_blk_ext_info(sd_pitch, builder, info, xcur, ymid, ytop)
            w_tot = xcur + w_edge
            _add_blk_ext_edge(sd_pitch, builder, be_top[0], ymid, ytop, w_edge, 0, well_w_edge)
            _add_blk_ext_edge(sd_pitch, builder, be_top[-1], ymid, ytop, w_edge, w_tot, well_w_edge)

        # Note: bbox not used, just pass in some value.
        return builder.get_info(BBox(0, 0, 0, 0))

    def get_mos_end_info(self, blk_h: int, num_cols: int, einfo: RowExtInfo) -> ExtEndLayInfo:
        blk_rect = BBox(0, 0, num_cols * self.sd_pitch, blk_h)
        builder = LayoutInfoBuilder()
        row_type = einfo.row_type
        threshold = einfo.threshold
        imp_y = (blk_rect.yl, blk_rect.yl)
        add_base(builder, row_type, threshold, imp_y, blk_rect)
        edge_info = MOSEdgeInfo(row_type=row_type, imp_y=imp_y, threshold=threshold)
        return ExtEndLayInfo(builder.get_info(blk_rect), edge_info)

    def get_mos_row_edge_info(self, blk_w: int, rinfo: MOSRowInfo, einfo: MOSEdgeInfo
                              ) -> LayoutInfo:
        blk_h = rinfo.height
        mos_type: MOSType = einfo['mos_type']
        return self._edge_info_helper(blk_w, blk_h, mos_type, rinfo.threshold, rinfo['imp_y'])

    def get_mos_ext_edge_info(self, blk_w: int, einfo: MOSEdgeInfo) -> LayoutInfo:
        row_type: MOSType = einfo['row_type']
        threshold: str = einfo['threshold']
        blk_h: int = einfo['blk_h']
        imp_y: Tuple[int, int] = einfo['imp_y']
        return self._edge_info_helper(blk_w, blk_h, row_type, threshold, imp_y)

    def get_mos_corner_info(self, blk_w: int, blk_h: int, einfo: MOSEdgeInfo) -> CornerLayInfo:
        lch = self.lch
        sd_pitch = self.sd_pitch
        well_w_edge = self.well_w_edge

        row_type: MOSType = einfo['row_type']
        threshold: str = einfo['threshold']

        well_yl = 0
        blk_rect = BBox(blk_w - sd_pitch, well_yl, blk_w, blk_h)
        builder = LayoutInfoBuilder()

        well_xl = blk_w - well_w_edge
        add_base(builder, row_type, threshold, (blk_rect.yl, blk_rect.yl), blk_rect,
                 well_x=(well_xl, blk_w))

        x_margins = dict(well=well_xl)
        y_margins = dict(well=well_yl)
        edgel = ImmutableSortedDict(dict(dev_type=DeviceType.MOS, lch=lch, margins=x_margins))
        edgeb = ImmutableSortedDict(dict(dev_type=DeviceType.MOS, lch=lch, margins=y_margins))
        return CornerLayInfo(builder.get_info(blk_rect), (0, 0), edgel, edgeb)

    @staticmethod
    def _get_conn_params(info: ConnInfo, bot_cl: int, bot_ch: int) -> Tuple[int, int, int]:
        v_dim = info.via_h if info.orient is Orient2D.y else info.via_w
        v_sp = info.via_sp
        v_bot_enc = info.via_bot_enc
        v_top_enc = info.via_top_enc
        v_pitch = v_dim + v_sp

        v_num = (bot_ch - bot_cl - v_bot_enc * 2 + v_sp) // v_pitch
        v_dim_arr = v_num * v_pitch - v_sp
        top_dim = max(info.len_min, v_dim_arr + 2 * v_top_enc)
        top_cl = (bot_cl + bot_ch - top_dim) // 2
        top_ch = top_cl + top_dim
        return top_cl, top_ch, v_num

    def _get_od_sep_col(self, spx: int) -> int:
        lch = self.lch
        sd_pitch = self.sd_pitch
        od_po_extx = self.od_po_extx

        return -(-(spx + lch + 2 * od_po_extx) // sd_pitch) - 1

    def _add_mos_active(self, builder: LayoutInfoBuilder, row_info: MOSRowInfo,
                        start: int, stop: int, w: int, is_sub: bool = False, sub_type: Optional[MOSType] = None
                        ) -> Tuple[int, int]:
        po_yl: int = row_info['po_y'][0]
        od_yl: int = row_info['od_y'][0]
        guard_ring: bool = row_info.guard_ring
        guard_ring_col: bool = row_info.guard_ring_col
        blk_yh: int = row_info.height

        sd_pitch = self.sd_pitch

        mconf = self.mos_config
        po_h_min: int = mconf['po_h_min']
        po_od_exty: int = mconf['po_od_exty']

        md_info = self.get_conn_info(0, False)
        v_w = md_info.via_w

        # draw PO
        od_yh = od_yl + w
        if is_sub:
            od_lp = self.tech_info.config['mos_lay_table']['OD']['sub']
            od_tap_extx = mconf['od_tap_extx']  # determines the amount to extend material from licon
            od_sd_dx = od_tap_extx + v_w // 2
        else:
            od_lp = self.tech_info.config['mos_lay_table']['OD']['active']
            po_y = (po_yl, max(po_yl + po_h_min, od_yh + po_od_exty))
            self._add_po_array(builder, po_y, start, stop)
            od_sd_dx = sd_pitch // 2

        # draw OD
        od_xl = start * sd_pitch - od_sd_dx
        od_xh = stop * sd_pitch + od_sd_dx
        builder.add_rect_arr(od_lp, BBox(od_xl, od_yl, od_xh, od_yh))
        imp_y = row_info['imp_y']
        if is_sub:
            md_lp = self.tech_info.config['mos_lay_table']['MD']
            if guard_ring and stop - start > self.gr_edge_col:
                if sub_type.is_n_plus:
                    imp_lp = ('nsdm', 'drawing')
                else:
                    imp_lp = ('psdm', 'drawing')
                imp_od_encx: int = mconf['imp_od_encx']
                md_y = row_info.ds_conn_y
                # OD, implant, li1 for left small rectangle
                od_xh2 = start * sd_pitch + self.gr_edge_col * sd_pitch + od_sd_dx
                builder.add_rect_arr(od_lp, BBox(od_xl, od_yh, od_xh2, blk_yh))
                builder.add_rect_arr(imp_lp, BBox(od_xl - imp_od_encx, od_yh, od_xh2 + imp_od_encx, blk_yh))
                builder.add_rect_arr(md_lp, BBox(od_xl, od_yh, od_xh2, blk_yh))
                od_xl2 = stop * sd_pitch - self.gr_edge_col * sd_pitch - od_sd_dx
                # OD, implant, li1 for right small rectangle
                builder.add_rect_arr(od_lp, BBox(od_xl2, od_yh, od_xh, blk_yh))
                builder.add_rect_arr(imp_lp, BBox(od_xl2 - imp_od_encx, od_yh, od_xh + imp_od_encx, blk_yh))
                builder.add_rect_arr(md_lp, BBox(od_xl2, od_yh, od_xh, blk_yh))
                # li1 for main OD
                builder.add_rect_arr(md_lp, BBox(od_xl, md_y[0], od_xh, md_y[1]))
            if guard_ring_col and stop - start == self.gr_edge_col:
                # OD, implant, li1 for entire height
                builder.add_rect_arr(od_lp, BBox(od_xl, 0, od_xh, blk_yh))
                builder.add_rect_arr(md_lp, BBox(od_xl, 0, od_xh, blk_yh))
                imp_y = (0, blk_yh)

        # draw base
        imp_od_encx: int = self.mos_config['imp_od_encx']
        bbox = BBox(od_xl-imp_od_encx, 0, od_xh+imp_od_encx, blk_yh)

        if is_sub:
            mos_type = sub_type
        else:
            mos_type = row_info.row_type
        add_base_mos(builder, mos_type, row_info.threshold, imp_y, bbox, is_sub=is_sub)

        return od_yl, od_yh

    def _add_po_array(self, builder: LayoutInfoBuilder, po_y: Tuple[int, int], start: int,
                      stop: int) -> None:
        po_lp = self.tech_info.config['mos_lay_table']['PO']
        lch = self.lch
        sd_pitch = self.sd_pitch
        po_x0 = (sd_pitch - lch) // 2 + sd_pitch * start
        fg = stop - start
        if po_y[1] > po_y[0]:
            builder.add_rect_arr(po_lp, BBox(po_x0, po_y[0], po_x0 + lch, po_y[1]),
                                 nx=fg, spx=sd_pitch)

    def _edge_info_helper(self, blk_w: int, blk_h: int, row_type: MOSType, threshold: str,
                          imp_y: Tuple[int, int]) -> LayoutInfo:
        sd_pitch = self.sd_pitch
        well_w_edge = self.well_w_edge

        blk_rect = BBox(blk_w - sd_pitch, 0, blk_w, blk_h)
        builder = LayoutInfoBuilder()
        add_base(builder, row_type, threshold, imp_y, blk_rect, well_x=(blk_w - well_w_edge, blk_w))
        return builder.get_info(blk_rect)


def _get_extend_bot_implant(bot_info: RowExtInfo, top_info: RowExtInfo) -> bool:
    # prefer n implant over p implant, prefer transistor over substrate
    bot_row_type = bot_info.row_type
    top_row_type = top_info.row_type
    if bot_row_type.is_pwell:
        return True
    if top_row_type.is_pwell:
        return False
    if not bot_row_type.is_substrate and top_row_type.is_substrate:
        return True
    if not top_row_type.is_substrate and bot_row_type.is_substrate:
        return False
    return bot_info.threshold < top_info.threshold


def _add_blk_ext_edge(sd_pitch: int, builder: LayoutInfoBuilder, binfo: BlkExtInfo,
                      yl: int, yh: int, blk_w: int, w_tot: int, well_w_edge: int) -> None:
    threshold = binfo.threshold

    if w_tot == 0:
        blk_rect = BBox(blk_w - sd_pitch, yl, blk_w, yh)
        mos_idx = 0
        well_x = (blk_w - well_w_edge, blk_w)
    else:
        xl = w_tot - blk_w
        blk_rect = BBox(xl, yl, xl + sd_pitch, yh)
        mos_idx = -1
        well_x = (xl, xl + well_w_edge)

    add_base(builder, binfo.fg_dev[mos_idx][1], threshold, (blk_rect.yl, blk_rect.yl),
             blk_rect, well_x=well_x)


def _add_blk_ext_info(sd_pitch: int, builder: LayoutInfoBuilder,
                      info: BlkExtInfo, xl: int, yl: int, yh: int) -> int:
    threshold = info.threshold

    # add base
    xcur = xl
    for fg, dev in info.fg_dev:
        xh = xcur + fg * sd_pitch
        add_base(builder, dev, threshold, (yl, yl), BBox(xcur, yl, xh, yh))
        xcur = xh

    return xcur
