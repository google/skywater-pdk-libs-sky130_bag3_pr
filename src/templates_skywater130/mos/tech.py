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

from typing import Tuple, Optional, FrozenSet, List, Mapping, Any

from dataclasses import dataclass
from itertools import chain

from pybag.enum import Orient2D
from pybag.core import COORD_MAX, BBox

from bag.util.immutable import ImmutableSortedDict, ImmutableList, Param
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
    ignore_vm_sp_le_layers: FrozenSet[str] = frozenset(('m1',))

    def __init__(self, tech_info: TechInfo, lch: int, arr_options: Mapping[str, Any]) -> None:
        MOSTech.__init__(self, tech_info, lch, arr_options) 

    @property
    def blk_h_pitch(self) -> int:
        return 2

    @property
    def end_h_min(self) -> int:
        return self.mos_config['imp_h_min'] // 2

    @property
    def min_sep_col(self) -> int:
        #return self._get_od_sep_col(self.mos_config['od_spx'])

        #felicia copied
        lch = self.lch
        sd_pitch = self.sd_pitch
        od_po_extx = self.od_po_extx

        od_spx: int = self.mos_config['od_spx']
        imp_od_encx: int = self.mos_config['imp_od_encx']
        ans = -(-(od_spx + lch + 2 * od_po_extx + 2*imp_od_encx) // sd_pitch) - 1
        return ans + (ans & 1)

    @property
    def sub_sep_col(self) -> int:
        # column separation needed between transistor/substrate and substrate/substrate.
        # This is guaranteed to be even.

        #return self._get_od_sep_col(max(self.mos_config['od_spx'],
        #                            2 * self.mos_config['imp_od_encx']))
        
        #felicia - copied method from cds_ff_mpt
        #does something similar to _get_od_sep_col but seems to have 
        #effective +1 that get_od doesn't have
        lch = self.lch
        sd_pitch = self.sd_pitch
        od_po_extx = self.od_po_extx

        mos_config = self.mos_config
        od_spx: int = mos_config['od_spx']
        imp_od_encx: int = mos_config['imp_od_encx']

        od_spx = max(od_spx, 2 * imp_od_encx)
        ans = -(-(od_spx + lch + 2 * od_po_extx) // sd_pitch) - 1
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
        return -(self.sd_pitch - self.lch) // 2 + self.od_po_extx + nwell_imp + imp_od_encx

    def get_conn_info(self, conn_layer: int, is_gate: bool) -> ConnInfo:
        mconf = self.mos_config
        wire_info = mconf['g_wire_info' if is_gate else 'd_wire_info']

        idx = conn_layer - wire_info['bot_layer']
        w, is_horiz, v_w, v_h, v_sp, v_bot_enc, v_top_enc = wire_info['info_list'][idx]
        orient = Orient2D(int(is_horiz ^ 1))
        if conn_layer == 0:
            sp_le = mconf['md_spy']
            len_min = -(-mconf['md_area_min'] // w)
        else:
            tech_info = self.tech_info
            lay, purp = tech_info.get_lay_purp_list(conn_layer)[0]
            # make sure minimum length satisfies via enclosure rule
            cur_len = 2 * v_top_enc + (v_w if is_horiz else v_h)
            len_min = tech_info.get_next_length(lay, purp, orient, w, cur_len, even=True)
            sp_le = tech_info.get_min_line_end_space(lay, w, purpose=purp, even=True)

        return ConnInfo(w, len_min, sp_le, orient, v_w, v_h, v_sp, v_bot_enc, v_top_enc)

    def can_short_adj_tracks(self, conn_layer: int) -> bool:
        return False

    def get_track_specs(self, conn_layer: int, top_layer: int) -> List[TrackSpec]:
        assert conn_layer == 1, 'currently only work for conn_layer = 1'

        sd_pitch = self.sd_pitch

        grid_info = self.mos_config['grid_info']

        return [TrackSpec(layer=lay, direction=Orient2D.y, width=vm_w,
                          space=num_sd * sd_pitch - vm_w, offset=(num_sd * sd_pitch) // 2)
                for lay, vm_w, num_sd in grid_info if conn_layer <= lay <= top_layer]

    def get_edge_width(self, mos_arr_width: int, blk_pitch: int) -> int:
        w_edge_min = self.mos_config['imp_od_encx'] + self.sd_pitch // 2
        return get_arr_edge_dim(mos_arr_width, w_edge_min, blk_pitch)

    def get_mos_row_info(self, conn_layer: int, specs: MOSRowSpecs, bot_mos_type: MOSType,
                         top_mos_type: MOSType, global_options: Param) -> MOSRowInfo:
        assert conn_layer == 1, 'currently only work for conn_layer = 1'

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

        mg_info = self.get_conn_info(0, False)
        mg_h = mg_info.w

        m1_info = self.get_conn_info(1, False)
        v0_h = m1_info.via_h
        m1_h_min = m1_info.len_min
        m1_spy = m1_info.sp_le
        md_bot_vency = m1_info.via_bot_enc
        m1_vency = m1_info.via_top_enc

        po_yl = po_spy2
        po_yh_gate = po_yl + po_h_gate
        po_yc_gate = (po_yl + po_yh_gate) // 2
        gm1_yh = po_yc_gate + v0_h // 2 + m1_vency
        gm1_yl = min(po_yc_gate - v0_h // 2 - m1_vency, gm1_yh - m1_h_min)
        # fix mg_imp spacing
        imp_yl = max(imp_h_min2, po_yc_gate + mg_h // 2 + mg_imp_spy)
        od_yl = imp_yl + imp_od_ency

        dm1_yl = gm1_yh + m1_spy
        dv0_yl = dm1_yl + m1_vency
        dmd_yl = dv0_yl - md_bot_vency
        dvc_yl = dmd_yl + md_top_vency
        od_yl = max(od_yl, dvc_yl - od_vency)

        od_yh = od_yl + w
        po_yh = od_yh + po_od_exty
        blk_yh = max(od_yh + imp_od_ency + imp_h_min2, po_yh + po_spy2)

        blk_yh = -(-blk_yh // blk_p) * blk_p

        md_yl, md_yh, vc_num = self._get_conn_params(self.get_conn_info(0, False), od_yl, od_yh)
        dm1_yl, dm1_yh, v0_num = self._get_conn_params(m1_info, md_yl, md_yh)

        # return MOSRowInfo
        top_einfo = RowExtInfo(
            mos_type, threshold,
            ImmutableSortedDict(dict(
                mos_type=mos_type,
                margins=dict(
                    od=(blk_yh - od_yh, od_spy),
                    po=(blk_yh - po_yh, po_spy),
                    m1=(blk_yh - dm1_yh, m1_spy),
                )
            )),
        )
        bot_einfo = RowExtInfo(
            mos_type, threshold,
            ImmutableSortedDict(dict(
                mos_type=mos_type,
                margins=dict(
                    od=(od_yl, od_spy),
                    po=(po_yl, po_spy),
                    m1=(gm1_yl, m1_spy),
                ),
            )),
        )
        info = dict(
            imp_y=(od_yl - imp_od_ency, od_yh + imp_od_ency),
            od_y=(od_yl, od_yh),
            po_y=(po_yh_gate, po_yh),
            po_y_gate=(po_yl, po_yh_gate),
        )

        g_y = (gm1_yl, gm1_yh)
        g_m_y = (0, po_yl)
        ds_y = ds_g_y = sub_y = (dm1_yl, dm1_yh)
        ds_m_y = (po_yh, blk_yh)
        return MOSRowInfo(self.lch, w, w_sub, mos_type, specs.threshold, blk_yh, specs.flip,
                          top_einfo, bot_einfo, ImmutableSortedDict(info), g_y, g_m_y, ds_y,
                          ds_m_y, ds_g_y, sub_y, guard_ring=False)

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

    def get_extension_regions(self, bot_info: RowExtInfo, top_info: RowExtInfo, height: int
                              ) -> Tuple[MOSCutMode, int, int]:
        if _get_extend_bot_implant(bot_info, top_info):
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
        assert conn_layer == 1, 'currently only work for conn_layer = 1'

        sep_g = options.get('sep_g', False)
        export_mid = options.get('export_mid', False)
        export_mid = export_mid and stack == 2

        sd_pitch = self.sd_pitch

        height = row_info.height
        row_type = row_info.row_type
        threshold = row_info.threshold
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
        d1_info = self.get_conn_info(1, False)
        md_yl, md_yh, num_vc = self._get_conn_params(d0_info, od_y[0], od_y[1])
        num_v0 = self._get_conn_params(d1_info, md_yl, md_yh)[2]
        md_y = (md_yl, md_yh)
        self._draw_ds_conn(builder, d0_info, d1_info, od_y, md_y, num_vc, num_v0,
                           d_xc, num_d, conn_pitch)
        self._draw_ds_conn(builder, d0_info, d1_info, od_y, md_y, num_vc, num_v0,
                           s_xc, num_s, conn_pitch)

        if export_mid:
            m_xc = sd_pitch
            num_m = fg + 1 - num_s - num_d
            m_info = (m_xc, num_m, wire_pitch)
            self._draw_ds_conn(builder, d0_info, d1_info, od_y, md_y, num_vc, num_v0,
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
        #breakpoint()
        mconf = self.mos_config
        npc_w: int = mconf['npc_w']
        npc_h: int = mconf['npc_h']
        npc_w2 = npc_w // 2
        npc_h2 = npc_h // 2

        g0_info = self.get_conn_info(0, True)
        g1_info = self.get_conn_info(1, True)

        po_lp = ('poly', 'drawing')
        po_conn_w = sd_pitch + lch
        po_xl_gate = g_xc - po_conn_w // 2

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

        # builder.add_rect_arr(po_lp, BBox(po_xl_gate, po_y_gate[0], po_xl_gate + po_conn_w,
                                         # po_y_gate[1]), nx=num_g, spx=conn_pitch)
        builder.add_rect_arr(po_lp, BBox(po_xl_even, po_y_gate[0], po_xh_even, po_y_gate[1]),
                             nx=(fg - (fg // 2)), spx=conn_pitch)
        builder.add_rect_arr(po_lp, BBox(po_xl_odd, po_y_gate[0], po_xh_odd, po_y_gate[1]),
                             nx=(fg // 2), spx=conn_pitch)

        po_yc_gate = (po_y_gate[0] + po_y_gate[1]) // 2
        po_h_gate = po_y_gate[1] - po_y_gate[0]
        builder.add_via(g0_info.get_via_info('PYL1_C', g_xc, po_yc_gate, po_h_gate,
                                             ortho=False, num=1, nx=num_g, spx=conn_pitch))
        # poly via draws npc layer wrong
        npc_box = BBox(g_xc - npc_w2, po_yc_gate - npc_h2, g_xc + npc_w2, po_yc_gate + npc_h2)
        builder.add_rect_arr(('npc', 'drawing'), npc_box, nx=num_g, spx=conn_pitch)

        mp_h = g0_info.w
        mp_w_min = g0_info.len_min
        mp_lp = ('li1', 'drawing')
        mp_yl = po_yc_gate - mp_h // 2
        mp_yh = mp_yl + mp_h
        if sep_g:
            mp_xl = g_xc - mp_w_min // 2
            builder.add_rect_arr(mp_lp, BBox(mp_xl, mp_yl, mp_xl + mp_w_min, mp_yh),
                                 nx=num_g, spx=conn_pitch)
        else:
            mp_dx = g0_info.via_w # felicia - // 2 + g0_info.via_top_enc
                                  # for licon.5
            mp_xl = g_xc - mp_dx
            mp_xh = g_xc + (num_g - 1) * conn_pitch + mp_dx
            builder.add_rect_arr(mp_lp, BBox(mp_xl, mp_yl, mp_xh, mp_yh))

        # connect MP to M1
        builder.add_via(g1_info.get_via_info('L1M1_C', g_xc, po_yc_gate, mp_h, ortho=True,
                                             num=1, nx=num_g, spx=conn_pitch))

    @staticmethod
    def _draw_ds_conn(builder: LayoutInfoBuilder, d0_info: ConnInfo, d1_info: ConnInfo,
                      od_y: Tuple[int, int], md_y: Tuple[int, int], num_vc: int, num_v0: int,
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

        od_yc = (od_y[0] + od_y[1]) // 2
        vc_h_arr = num_vc * vc_p - vc_sp
        vc_yc_bot = od_yc + (vc_h - vc_h_arr) // 2
        vc_box = BBox(xc - vc_w2, vc_yc_bot - vc_h2, xc + vc_w2, vc_yc_bot + vc_h2)
        md_box = BBox(xc - md_w2, md_y[0], xc + md_w2, md_y[1])
        builder.add_rect_arr(('licon1', 'drawing'), vc_box, nx=nx, spx=spx, ny=num_vc, spy=vc_p)
        builder.add_rect_arr(('li1', 'drawing'), md_box, nx=nx, spx=spx)
        # connect to M1
        builder.add_via(d1_info.get_via_info('L1M1_C', xc, od_yc, md_w, ortho=False,
                                             num=num_v0, nx=nx, spx=spx))

    def get_mos_abut_info(self, row_info: MOSRowInfo, edgel: MOSEdgeInfo, edger: MOSEdgeInfo
                          ) -> LayoutInfo:
        raise ValueError('This method is not supported in this technology.')

    def get_mos_tap_info(self, row_info: MOSRowInfo, conn_layer: int, seg: int,
                         options: Param) -> MOSLayInfo:
        assert conn_layer == 1, 'currently only work for conn_layer = 1'
        #print(row_info)
        row_type = row_info.row_type

        guard_ring: bool = options.get('guard_ring', row_info.guard_ring)
        if guard_ring:
            sub_type: MOSType = options.get('sub_type', row_type.sub_type)
        else:
            #print(row_type.sub_type)
            sub_type: MOSType = row_type.sub_type

        sd_pitch = self.sd_pitch

        w = row_info.sub_width
        height = row_info.height
        threshold = row_info.threshold
        imp_y: Tuple[int, int] = row_info['imp_y']

        # draw device
        builder = LayoutInfoBuilder()
        #draws diffusion and tap
        #if (row_type is MOSType.nch):
        od_y = self._add_mos_active(builder, row_info, 0, seg, w, is_sub=True)
        #print(row_info)
        #else:
        #    od_y = (193, 303)
        # draw drain/source connections
        d0_info = self.get_conn_info(0, False)
        d1_info = self.get_conn_info(1, False)
        md_yl, md_yh, num_vc = self._get_conn_params(d0_info, od_y[0], od_y[1])
        num_v0 = self._get_conn_params(d1_info, md_yl, md_yh)[2]
        md_y = (md_yl, md_yh)

        #draws in vias connecting tap cell to metal 1
        self._draw_ds_conn(builder, d0_info, d1_info, od_y, md_y, num_vc, num_v0,
                           0, seg + 1, sd_pitch)

        # draw base
        # add extra imp)od_encx for ntap and ptap
        imp_od_encx: int = self.mos_config['imp_od_encx']
        bbox = BBox(0-2*imp_od_encx, 0, seg * sd_pitch + 2*imp_od_encx, height)
        add_base_mos(builder, sub_type, threshold, imp_y, bbox, is_sub=True)
        
        edge_info = MOSEdgeInfo(mos_type=sub_type, imp_y=imp_y, has_od=True)
        be = BlkExtInfo(row_type, row_info.threshold, guard_ring, ImmutableList([(seg, sub_type)]),
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

        builder = LayoutInfoBuilder()

        # find dummy OD columns
        od_extx = od_po_extx - (sd_pitch - lch) // 2
        delta_implant = od_extx + imp_od_encx
        delta_implant = -(-delta_implant // sd_pitch) * sd_pitch
        if typel == typer:
            # same implant on left and right
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

            be = BlkExtInfo(row_type, threshold, False, ImmutableList(fg_dev_list),
                            ImmutableSortedDict())
            edgel = MOSEdgeInfo(mos_type=typel, imp_y=imp_y, has_od=False)
            edger = edgel.copy_with(mos_type=typer)

        wire_info = (0, 0, 0)
        return MOSLayInfo(builder.get_info(bbox), edgel, edger, be, be, g_info=wire_info,
                          d_info=wire_info, s_info=wire_info, shorted_ports=ImmutableList())

    def get_mos_ext_info(self, num_cols: int, blk_h: int, bot_einfo: RowExtInfo,
                         top_einfo: RowExtInfo, gr_info: Tuple[int, int]) -> ExtEndLayInfo:
        raise ValueError('Not implemented.')

    def get_mos_ext_gr_info(self, num_cols: int, edge_cols: int, blk_h: int, bot_einfo: RowExtInfo,
                            top_einfo: RowExtInfo, sub_type: MOSType, einfo: MOSEdgeInfo
                            ) -> ExtEndLayInfo:
        raise ValueError('Not implemented.')

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
                        start: int, stop: int, w: int, is_sub: bool = False
                        ) -> Tuple[int, int]:
        po_yl: int = row_info['po_y'][0]
        od_yl: int = row_info['od_y'][0]

        lch = self.lch
        sd_pitch = self.sd_pitch
        od_po_extx = self.od_po_extx

        mconf = self.mos_config
        po_h_min: int = mconf['po_h_min']
        po_od_exty: int = mconf['po_od_exty']

        # draw PO
        od_yh = od_yl + w
        if is_sub:
            od_lp = ('tap', 'drawing')
        else:
            od_lp = ('diff', 'drawing')
            po_y = (po_yl, max(po_yl + po_h_min, od_yh + po_od_exty))
            self._add_po_array(builder, po_y, start, stop)

        # draw OD
        po_xl = (sd_pitch - lch) // 2
        od_sd_dx = od_po_extx - po_xl
        od_xl = start * sd_pitch - od_sd_dx
        od_xh = stop * sd_pitch + od_sd_dx
        builder.add_rect_arr(od_lp, BBox(od_xl, od_yl, od_xh, od_yh))

        # draw base
        imp_od_encx: int = self.mos_config['imp_od_encx']
        bbox = BBox(od_xl-imp_od_encx, 0, od_xh+imp_od_encx, row_info.height)
        
        #if drawing tap cells, flip the implant type so its opposite of row
        if is_sub:
            if (row_info.row_type is MOSType.nch):
                add_base_mos(builder, MOSType.pch, row_info.threshold, row_info['imp_y'], bbox, is_sub=True)
            elif (row_info.row_type is MOSType.pch):
                add_base_mos(builder, MOSType.nch, row_info.threshold, row_info['imp_y'], bbox, is_sub=True)
        else:    
            add_base_mos(builder, row_info.row_type, row_info.threshold, row_info['imp_y'], bbox)

        return od_yl, od_yh

    def _add_po_array(self, builder: LayoutInfoBuilder, po_y: Tuple[int, int], start: int,
                      stop: int) -> None:
        lch = self.lch
        sd_pitch = self.sd_pitch

        po_x0 = (sd_pitch - lch) // 2 + sd_pitch * start
        fg = stop - start
        if po_y[1] > po_y[0]:
            builder.add_rect_arr(('poly', 'drawing'), BBox(po_x0, po_y[0], po_x0 + lch, po_y[1]),
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
