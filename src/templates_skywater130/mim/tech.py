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

from typing import Tuple

from pybag.core import BBox

from bag.layout.tech import TechInfo

from xbase.layout.data import LayoutInfoBuilder, ViaInfo
from xbase.layout.cap.tech import MIMTech
from xbase.layout.cap.tech import MIMLayInfo


class MIMTechSkywater130(MIMTech):
    def __init__(self, tech_info: TechInfo) -> None:
        MIMTech.__init__(self, tech_info)

    # noinspection PyMethodMayBeStatic
    def get_port_layers(self, mim_type: str) -> Tuple[int, int]:
        if mim_type == 'standard' or mim_type == '45' or mim_type == 45:
            return 4, 5
        if mim_type == '34' or mim_type == 34:
            return 3, 4
        raise ValueError(f'Invalid mim_type={mim_type}. Use \'standard\' or \'45\' or \'34\'')

    def get_mim_cap_info(self, bot_layer: int, top_layer: int, unit_width: int, unit_height: int,
                         num_rows: int, num_cols: int, dum_row_b: int, dum_row_t: int, dum_col_l: int, dum_col_r: int,
                         bot_w: int, top_w: int) -> MIMLayInfo:
        assert bot_layer == top_layer - 1, 'MIMCap can exist between adjacent layers only'
        cap_info = self.mim_config['cap_info']
        if top_layer not in cap_info:
            raise ValueError(f'MIMCap does not exist with top_layer={top_layer}')

        cap_lp, cap_w, cap_sp = cap_info[top_layer]
        bot_lp = self._tech_info.get_lay_purp_list(bot_layer)[0]
        top_lp = self._tech_info.get_lay_purp_list(top_layer)[0]

        width = num_cols * unit_width
        width_total = (num_cols + dum_col_l + dum_col_r) * unit_width
        height = num_rows * unit_height
        height_total = (num_rows + dum_row_b + dum_row_t) * unit_height

        if dum_row_b > 0 or dum_row_t > 0:
            raise NotImplementedError('Contact Felicia')
        if dum_col_r > 0:
            raise NotImplementedError('Contact Felicia')

        via_info = self.mim_config['via_info']
        via_type, via_dim, via_sp, via_bot_enc, via_top_enc = via_info[bot_layer]

        if min(width, height) < min(bot_w, top_w):
            raise ValueError('Unit cell dimensions are too small')
 
        # DRC rules
        ratio: int = self.mim_config['max_ratio'] 
        cap_bound: int = self.mim_config['top_to_cap_sp'] 

        if top_layer == 4:
            via_bnd: int = self.mim_config['capvia_cap']
            bot_sp = -(- cap_sp // 2)
        else:
            via_bnd = via_bot_enc
            bot_sp = bot_w
      
        top_ext = 3 * top_w + cap_bound
        bot_ext = 3 * bot_w + cap_bound

        builder = LayoutInfoBuilder()

        # Cap construction
        # array
        if max(num_rows, num_cols) > 1 or max(dum_row_b, dum_row_t, dum_col_l, dum_col_r) > 0:
            cap_off_h = cap_sp + bot_ext

            if unit_height / unit_width > ratio or unit_width / unit_height > ratio:
                raise ValueError('Unit dimensions violate DRC rules')
            
            tot_rows = num_rows + dum_row_b + dum_row_t
            tot_cols = num_cols + dum_col_l + dum_col_r
            block_w = unit_width
            base_y = bot_sp + cap_bound
            for ridx in range(0, tot_rows):
                y_bot = base_y + ridx * (unit_height + cap_sp)
                for cidx in range(0, tot_cols):
                    xl_cap = bot_ext + cidx * (block_w + cap_off_h)
                    xh_cap = xl_cap + block_w
                    yl_cap = y_bot
                    yh_cap = y_bot + unit_height

                    xl_via = xl_cap + via_bnd
                    xh_via = xh_cap - via_bnd
                    yl_via = yl_cap + via_bnd
                    yh_via = yh_cap - via_bnd

                    builder.add_rect_arr(cap_lp, BBox(xl_cap, yl_cap, xh_cap, yh_cap))
                    builder.add_via(get_via_info(via_type, BBox(xl_via, yl_via, xh_via, yh_via),
                                                 via_dim, via_sp, via_bot_enc, via_top_enc))
            if dum_col_l > 0 or dum_col_r > 0:
                # for the actual cap
                xl_top = width_total - width + dum_col_l * cap_off_h + bot_ext
                xh_top = width_total + (tot_cols - 1) * cap_off_h + top_ext + bot_ext + cap_bound
                yl_top = bot_sp + cap_bound
                yh_top = height_total + (tot_rows - 1) * cap_sp + bot_sp + cap_bound

                xl_bot = width_total - width + dum_col_l * cap_off_h
                xh_bot = width_total + (tot_cols - 1) * cap_off_h + bot_ext + cap_bound
                yl_bot = bot_sp
                yh_bot = height_total + (tot_rows - 1) * cap_sp + 2 * cap_bound + bot_sp

                builder.add_rect_arr(bot_lp, BBox(xl_bot, yl_bot, xh_bot, yh_bot))
                builder.add_rect_arr(top_lp, BBox(xl_top, yl_top, xh_top, yh_top))

                # for the dummy
                xl_dtop = bot_ext
                xh_dtop = width_total - width + (dum_col_l - 1) * cap_off_h + bot_ext + cap_bound
                yl_dtop = bot_sp + cap_bound
                yh_dtop = height + (tot_rows - 1) * cap_sp + bot_sp + cap_bound

                xl_dbot = 0
                xh_dbot = width_total - width + (dum_col_l - 1) * cap_off_h + bot_ext + cap_bound
                yl_dbot = bot_sp
                yh_dbot = height + (tot_rows - 1) * cap_sp + 2 * cap_bound + bot_sp

                builder.add_rect_arr(bot_lp, BBox(xl_dbot, yl_dbot, xh_dbot, yh_dbot))
                builder.add_rect_arr(top_lp, BBox(xl_dtop, yl_dtop, xh_dtop, yh_dtop))
            else:
                xl_top = bot_ext
                xh_top = width + (tot_cols - 1) * cap_off_h + top_ext + bot_ext
                yl_top = bot_sp + cap_bound
                yh_top = height + (tot_rows - 1) * cap_sp + bot_sp + cap_bound

                xl_bot = 0
                xh_bot = width + (tot_cols - 1) * cap_off_h + bot_ext + cap_bound
                yl_bot = bot_sp
                yh_bot = height + (tot_rows - 1) * cap_sp + 2 * cap_bound + bot_sp

                builder.add_rect_arr(bot_lp, BBox(xl_bot, yl_bot, xh_bot, yh_bot))
                builder.add_rect_arr(top_lp, BBox(xl_top, yl_top, xh_top, yh_top))

            # add top metal and bottom 
            w_tot = xh_top
            h_tot = bot_sp + cap_bound + height + tot_rows * cap_sp
            
            pin_bot_yl = bot_sp
            pin_bot_yh = h_tot - cap_sp

            pin_top_yl = bot_sp + cap_bound
            pin_top_yh = h_tot - cap_sp
            pin_bot_xl = width_total - width + dum_col_l * cap_off_h
            pin_top_xh = w_tot

            bnd_box = BBox(0, 0, w_tot, h_tot)

        # not arrayed
        else:
            xl_top = bot_ext
            xh_top = width + top_ext + bot_ext
            yl_top = bot_sp + cap_bound
            yh_top = height + bot_sp + cap_bound

            xl_bot = 0
            xh_bot = width + bot_ext + cap_bound
            yl_bot = bot_sp
            yh_bot = height + 2 * cap_bound + bot_sp

            builder.add_rect_arr(bot_lp, BBox(xl_bot, yl_bot, xh_bot, yh_bot))
            builder.add_rect_arr(top_lp, BBox(xl_top, yl_top, xh_top, yh_top))

            # This only deals with long widths
            if width / height > ratio:
                num_blocks = -(- max(width, height) // (ratio * min(width, height)))

                block_w = -(- (width - (num_blocks - 1) * cap_sp) // num_blocks)
                for bidx in range(0, num_blocks):
                    xl_cap = bot_ext + bidx * (block_w + cap_sp)
                    xh_cap = xl_cap + block_w
                    yl_cap = bot_sp + cap_bound
                    yh_cap = yl_cap + height

                    xl_via = xl_cap + via_bnd
                    xh_via = xh_cap - via_bnd
                    yl_via = yl_cap + via_bnd
                    yh_via = yh_cap - via_bnd

                    builder.add_rect_arr(cap_lp, BBox(xl_cap, yl_cap, xh_cap, yh_cap))
                    builder.add_via(get_via_info(via_type, BBox(xl_via, yl_via, xh_via, yh_via),
                                                 via_dim, via_sp, via_bot_enc, via_top_enc))
 
            else:
                xl_cap = bot_ext
                xh_cap = xl_cap + width
                yl_cap = bot_sp + cap_bound
                yh_cap = yl_cap + height

                xl_via = xl_cap + via_bnd
                xh_via = xh_cap - via_bnd
                yl_via = yl_cap + via_bnd
                yh_via = yh_cap - via_bnd
                builder.add_rect_arr(cap_lp, BBox(xl_cap, yl_cap, xh_cap, yh_cap))
                builder.add_via(get_via_info(via_type, BBox(xl_via, yl_via, xh_via, yh_via),
                                             via_dim, via_sp, via_bot_enc, via_top_enc))
        
            w_tot = bot_ext + width + top_ext
            h_tot = bot_sp + 2 * cap_bound + height + cap_sp

            pin_bot_yl = bot_sp
            pin_bot_yh = height + 2 * cap_bound + bot_sp

            pin_top_yl = bot_sp + cap_bound
            pin_top_yh = bot_sp + height + cap_bound
            pin_bot_xl = 0
            pin_top_xh = w_tot

            # set size
            bnd_box = BBox(0, 0, w_tot, h_tot)
        
        return MIMLayInfo(builder.get_info(bnd_box), (pin_bot_yl, pin_bot_yh), (pin_top_yl, pin_top_yh),
                          pin_bot_xl, pin_top_xh)
     

def get_via_info(via_type: str, box: BBox, via_dim: int, via_sp: int, bot_enc: int, top_enc: int) -> ViaInfo:
    """Create vias over specified area."""
    xc = (box.xl + box.xh) // 2
    yc = (box.yl + box.yh) // 2

    enc1 = (bot_enc, bot_enc, bot_enc, bot_enc)
    enc2 = (top_enc, top_enc, top_enc, top_enc)

    vnx = (box.xh - box.xl) // (via_dim + via_sp)
    vny = (box.yh - box.yl) // (via_dim + via_sp)

    nx = 1
    ny = 1
    return ViaInfo(via_type, xc, yc, via_dim, via_dim, enc1, enc2,
                   vnx, vny, via_sp, via_sp, nx, ny, 0, 0)

    # viaInfo needs
    # via_type - via name
    # xc: x coordinate center
    # yc: y coordinate center
    # w: via width
    # h: via height
    # enc1: Tuple[int, int, int, int] = (0, 0, 0, 0)
    #       bottom layer via enclosure  
    # enc2: Tuple[int, int, int, int] = (0, 0, 0, 0)
    #       top layer via enclosure
    # vnx: number of vias in x direction
    # vny: number of vias in y direction
    # vspx: via x spacing
    # vspy: via y spacing
    # nx: int = 1
    # ny: int = 1
    # spx: int = 0
    # spy: int = 0
 