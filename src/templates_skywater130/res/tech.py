# BSD 3-Clause License
#
# Copyright (c) 2018, Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from typing import Any, Optional, List, Tuple, Sequence, Mapping

from pybag.enum import Orient2D
from pybag.core import BBox

from bag.util.immutable import ImmutableSortedDict, Param
from bag.layout.routing.grid import TrackSpec
from bag.layout.tech import TechInfo

from xbase.layout.data import LayoutInfo, LayoutInfoBuilder, CornerLayInfo, ViaInfo
from xbase.layout.array.data import ArrayLayInfo, ArrayEndInfo
from xbase.layout.res.tech import ResTech


class ResTechSkywater130(ResTech):
    """Resistor class for SkyWater130
    """
    def __init__(self, tech_info: TechInfo, metal: bool = False) -> None:
        ResTech.__init__(self, tech_info, metal=metal)
        if metal:
            raise RuntimeError("Metal resistors currently not supported")

    def get_width(self, **kwargs) -> int:
        if "unit_specs" not in kwargs:
            raise RuntimeError("Please add unit_specs")
        w_unit: int = kwargs['unit_specs']['params']['w']
        w_min: int = self._res_config['w_min']
        if w_unit < w_min:
            raise ValueError(f'w={w_unit} has to be greater than or equal to w_min={w_min}.')
        return w_unit

    def get_length(self, **kwargs) -> int:
        if "unit_specs" not in kwargs:
            raise RuntimeError("Please add unit_specs")
        l_unit: int = kwargs['unit_specs']['params']['l']
        l_min: int = self._res_config['l_min']
        if l_unit < l_min:
            raise ValueError(f'l={l_unit} has to be greater than or equal to l_min={l_min}.')
        return l_unit

    @property
    def min_size(self) -> Tuple[int, int]:
        return self._res_config['min_size']

    @property
    def blk_pitch(self) -> Tuple[int, int]:
        return self._res_config['blk_pitch']

    def get_track_specs(self, conn_layer: int, top_layer: int) -> List[TrackSpec]:
        grid_info: Sequence[Tuple[int, int, int]] = self._res_config['grid_info']

        return [TrackSpec(layer=lay, direction=Orient2D.y, width=vm_w, space=vm_sp, offset=(vm_w + vm_sp) // 2)
                for lay, vm_w, vm_sp in grid_info if conn_layer < lay <= top_layer]

    def get_edge_width(self, info: ImmutableSortedDict[str, Any], arr_dim: int, blk_pitch: int) -> int:
        edge_margin: int = self._res_config['edge_margin']
        return -(- edge_margin // blk_pitch) * blk_pitch

    def get_end_height(self, info: ImmutableSortedDict[str, Any], arr_dim: int, blk_pitch: int) -> int:
        end_margin: int = self._res_config['end_margin']
        return -(- end_margin // blk_pitch) * blk_pitch

    def get_blk_info(self, conn_layer: int, w: int, h: int, nx: int, ny: int, **kwargs: Any) -> Optional[ArrayLayInfo]:
        po_id_exty: int = self._res_config['po_id_exty']
        npc_po_enc: int = self._res_config['npc_po_enc']
        imp_npc_enc: Tuple[int, int] = self._res_config['imp_npc_enc']
        tap_imp_h: int = self._res_config['tap_imp_h']
        rlay_npc_enc: int = self._res_config['rlay_npc_enc']
        npc_sp: int = self._res_config['npc_sp']

        tap_imp_h2 = tap_imp_h // 2

        # unit resistor dimensions
        w_unit = self.get_width(**kwargs)
        l_unit = self.get_length(**kwargs)

        w_pitch, h_pitch = self.blk_pitch
        w_blk = -(-(w_unit + 2 * (npc_po_enc + max(rlay_npc_enc, npc_sp // 2))) // w_pitch) * w_pitch
        h_blk = -(-(l_unit + 2 * (po_id_exty + npc_po_enc + imp_npc_enc[1] + tap_imp_h2)) // h_pitch) * h_pitch
        if w < w_blk or h < h_blk:
            return None

        res_lay_table = self._tech_info.config['res_lay_table']

        # --- Compute layout --- #
        top_bbox = BBox(0, 0, w, h)
        builder = LayoutInfoBuilder()

        # draw ID layer in the center
        w2 = w // 2
        h2 = h // 2
        w_unit2 = w_unit // 2
        l_unit2 = l_unit // 2
        id_lp = res_lay_table['ID']
        builder.add_rect_arr(id_lp, BBox(w2 - w_unit2, h2 - l_unit2, w2 + w_unit2, h2 + l_unit2))

        # draw cut layer
        cut_lp = res_lay_table['CUT']
        builder.add_rect_arr(cut_lp, BBox(w2 - w_unit2, h2, w2 + w_unit2, h2 + 1))

        # draw poly: same width as ID layer, height extends beyond ID layer
        po_lp = res_lay_table['PO']
        builder.add_rect_arr(po_lp, BBox(w2 - w_unit2, h2 - l_unit2 - po_id_exty,
                                         w2 + w_unit2, h2 + l_unit2 + po_id_exty))

        # draw npc enclosing poly
        npc_lp = res_lay_table['NPC']
        builder.add_rect_arr(npc_lp, BBox(w2 - w_unit2 - npc_po_enc, h2 - l_unit2 - po_id_exty - npc_po_enc,
                                          w2 + w_unit2 + npc_po_enc, h2 + l_unit2 + po_id_exty + npc_po_enc))

        # draw resistor layer: span entire width, extend beyond npc in height
        res_type: str = kwargs['unit_specs']['params']['res_type']
        r_lp = self._res_config['rlay'][res_type]
        builder.add_rect_arr(r_lp, BBox(0, h2 - l_unit2 - po_id_exty - npc_po_enc - rlay_npc_enc,
                                        w, h2 + l_unit2 + po_id_exty + npc_po_enc + rlay_npc_enc))

        # draw implant layer extending beyond taps on top and bottom
        imp_lp = res_lay_table['IMP']
        builder.add_rect_arr(imp_lp, BBox(0, - tap_imp_h2, w, h + tap_imp_h2))

        # add bottom tap
        tap_h: int = self._res_config['tap_h']
        tap_h2 = tap_h // 2
        od_lp = res_lay_table['OD_sub']
        tap_via_specs: Mapping[str, Any] = self._res_config['tap_via_specs']
        tap_via_name: str = tap_via_specs['name']
        tap_via_w, tap_via_h = tap_via_specs['dim']
        tap_via_bot_enc: Tuple[int, int] = tap_via_specs['bot_enc']
        tap_via_top_enc: Tuple[int, int] = tap_via_specs['top_enc']
        tap_via_spx: int = tap_via_specs['spx']
        tap_via_benc = (tap_via_bot_enc[0], tap_via_bot_enc[0], tap_via_bot_enc[1], tap_via_bot_enc[1])
        tap_via_tenc = (tap_via_top_enc[0], tap_via_top_enc[0], tap_via_top_enc[1], tap_via_top_enc[1])
        tap_vnx = (w_unit - 2 * tap_via_bot_enc[0] + tap_via_spx) // (tap_via_w + tap_via_spx)
        tap_via_tot_w = tap_via_w * tap_vnx + tap_via_spx * (tap_vnx - 1)
        builder.add_rect_arr(od_lp, BBox(w2 - w_unit2, - tap_h2, w2 + w_unit2, tap_h2))
        builder.add_via(ViaInfo(tap_via_name, w2, 0, tap_via_w, tap_via_h, tap_via_benc, tap_via_tenc, tap_vnx, 1,
                                tap_via_spx))

        # add top tap
        builder.add_rect_arr(od_lp, BBox(w2 - w_unit2, h - tap_h2, w2 + w_unit2, h + tap_h2))
        builder.add_via(ViaInfo(tap_via_name, w2, h, tap_via_w, tap_via_h, tap_via_benc, tap_via_tenc, tap_vnx, 1,
                                tap_via_spx))

        # vias to conn_layer ports
        po_via_specs: Mapping[str, Any] = self._res_config['po_via_specs']
        po_via_name: str = po_via_specs['name']
        po_via_w, po_via_h = po_via_specs['dim']
        po_via_bot_enc: Tuple[int, int] = po_via_specs['bot_enc']
        po_via_top_enc: Tuple[int, int] = po_via_specs['top_enc']
        po_via_spx: int = po_via_specs['spx']
        po_via_benc = (po_via_bot_enc[0], po_via_bot_enc[0], po_via_bot_enc[1], po_via_bot_enc[1])
        po_via_tenc = (po_via_top_enc[0], po_via_top_enc[0], po_via_top_enc[1], po_via_top_enc[1])
        po_vnx = (w_unit - 2 * po_via_bot_enc[0] + po_via_spx) // (po_via_w + po_via_spx)
        po_via_tot_w = po_via_w * po_vnx + po_via_spx * (po_vnx - 1)
        builder.add_via(ViaInfo(po_via_name, w2, h2 - l_unit2 - po_via_h // 2, po_via_w, po_via_h, po_via_benc,
                                po_via_tenc, po_vnx, 1, po_via_spx))
        builder.add_via(ViaInfo(po_via_name, w2, h2 + l_unit2 + po_via_h // 2, po_via_w, po_via_h, po_via_benc,
                                po_via_tenc, po_vnx, 1, po_via_spx))

        # ports on conn_layer
        conn_lp = self._tech_info.get_lay_purp_list(self.conn_layer)[0]
        minus_bbox = BBox(w2 - po_via_tot_w // 2 - po_via_top_enc[0], h2 - l_unit2 - po_via_h - po_via_top_enc[1],
                          w2 + po_via_tot_w // 2 + po_via_top_enc[0], h2 - l_unit2 + po_via_top_enc[1])
        builder.add_rect_arr(conn_lp, minus_bbox)

        plus_bbox = BBox(w2 - po_via_tot_w // 2 - po_via_top_enc[0], h2 + l_unit2 - po_via_top_enc[1],
                         w2 + po_via_tot_w // 2 + po_via_top_enc[0], h2 + l_unit2 + po_via_h + po_via_top_enc[1])
        builder.add_rect_arr(conn_lp, plus_bbox)

        tap_via_h2 = tap_via_h // 2
        tap_via_tot_w2 = tap_via_tot_w // 2
        bulk0_bbox = BBox(w2 - tap_via_tot_w2 - tap_via_top_enc[0], - tap_via_h2 - tap_via_top_enc[1],
                          w2 + tap_via_tot_w2 + tap_via_top_enc[0], tap_via_h2 + tap_via_top_enc[1])
        builder.add_rect_arr(conn_lp, bulk0_bbox)
        bulk1_bbox = BBox(w2 - tap_via_tot_w2 - tap_via_top_enc[0], h - tap_via_h2 - tap_via_top_enc[1],
                          w2 + tap_via_tot_w2 + tap_via_top_enc[0], h + tap_via_h2 + tap_via_top_enc[1])
        builder.add_rect_arr(conn_lp, bulk1_bbox)

        ports = dict(MINUS=[(conn_lp[0], [minus_bbox])], PLUS=[(conn_lp[0], [plus_bbox])],
                     BULK=[(conn_lp[0], [bulk0_bbox, bulk1_bbox])])

        lay_info = builder.get_info(top_bbox)
        edge_info = Param(dict(od_margin=0))
        end_info = Param(dict(od_margin=0))
        ports = Param(ports)
        return ArrayLayInfo(lay_info, ports, edge_info, end_info)

    # noinspection PyMethodMayBeStatic
    def get_edge_info(self, w: int, h: int, info: ImmutableSortedDict[str, Any], **kwargs: Any) -> LayoutInfo:
        builder = LayoutInfoBuilder()
        blk_bbox = BBox(0, 0, w, h)
        return builder.get_info(blk_bbox)

    # noinspection PyMethodMayBeStatic
    def get_end_info(self, w: int, h: int, info: ImmutableSortedDict[str, Any], **kwargs: Any) -> ArrayEndInfo:
        builder = LayoutInfoBuilder()
        blk_bbox = BBox(0, 0, w, h)
        return ArrayEndInfo(builder.get_info(blk_bbox), ImmutableSortedDict())

    # noinspection PyMethodMayBeStatic
    def get_corner_info(self, w: int, h: int, info: ImmutableSortedDict[str, Any], **kwargs: Any) -> CornerLayInfo:
        x_margins = dict(well=0, base=0)
        y_margins = dict(well=0, base=0)
        edgel = Param(dict(margins=x_margins))
        edgeb = Param(dict(margins=y_margins))
        builder = LayoutInfoBuilder()
        blk_bbox = BBox(0, 0, w, h)
        return CornerLayInfo(builder.get_info(blk_bbox), (0, 0), edgel, edgeb)
