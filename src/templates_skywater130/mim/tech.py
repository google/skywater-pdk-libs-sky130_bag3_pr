# SPDX-License-Identifier: Apache-2.0
# Copyright 2019 Blue Cheetah Analog Design Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import FrozenSet

from pybag.core import BBox

from bag.layout.tech import TechInfo

from xbase.layout.data import LayoutInfoBuilder, ViaInfo
from xbase.layout.cap.tech import MIMTech
from xbase.layout.cap.tech import MIMLayInfo


class MIMTechSkywater130(MIMTech):
    ignore_vm_sp_le_layers: FrozenSet[str] = frozenset(('m1',))

    def __init__(self, tech_info: TechInfo) -> None:
        MIMTech.__init__(self, tech_info) 

    def get_mim_cap_info(self, top_layer: int,
                         bot_layer: int, rows: int, columns: int,
                         dum_columns: int,
                         unit_width: int,
                         unit_height: int) -> MIMLayInfo:    
        
        top_cap = max(top_layer, bot_layer)
        bot_cap = min(top_layer, bot_layer)

        avail_top = False
        avail_bot = False

        top_metal, topm_wid, topm_sp = self.grid_info[top_cap]
        bot_metal, botm_wid, botm_sp = self.grid_info[bot_cap]
        
        if (top_cap in self.mim_config['cap_info']) and \
            (bot_cap == top_cap - 1):
            cap_lay, cap_wid, cap_off = self.mim_config['cap_info'][top_cap]
            avail_top = True
            avail_bot = True

        top_metal = tuple(top_metal)
        bot_metal = tuple(bot_metal)
        cap_lay = tuple(cap_lay)

        width = columns * unit_width
        width_total = (columns + dum_columns) * unit_width
        height = rows * unit_height

        for list in self.mim_config['via_info']:
            if (bot_cap == int(list[0])):
                via_type, via_dim, via_sp, via_bot_enc, via_top_enc = list[1:]

        if (abs(top_cap-bot_cap) != 1):
            raise ValueError("MIM cap can only be constructed \
                             between adjacent layers")
        if (not avail_top):
            raise ValueError(f"MIM cap not available on top layer {top_cap}")
        if (not avail_bot):
            raise ValueError(f"MIM cap not available on bot layer {bot_cap}")
        if (min(width, height) < cap_wid):
            raise ValueError("Dimension too small")
 
        # DRC rules
        ratio: int = self.mim_config['max_ratio'] 
        cap_bound: int = self.mim_config['top_to_cap_sp'] 

        if top_cap == 4:
            via_bnd: int = self.mim_config['capvia_cap']
            bot_sp = -(-cap_off//2)
        else:
            via_bnd = via_bot_enc
            bot_sp = botm_wid
      
        top_ext = 3*topm_wid+cap_bound
        bot_ext = 3*botm_wid+cap_bound

        builder = LayoutInfoBuilder()

        # Cap construction
        # array
        if (rows > 1 or columns > 1 or dum_columns > 0):
            cap_off_h = cap_off+bot_ext

            if (unit_height/unit_width > ratio or unit_width/unit_height
                    > ratio):
                raise ValueError("Unit dimensions violate DRC rules")
            
            tot_columns = columns + dum_columns
            block_w = unit_width
            base_y = bot_sp+cap_bound
            for j in range(0, rows):  
                y_bot = base_y + j*(int(unit_height+cap_off))
                for n in range(0, tot_columns):
                    xl_cap = bot_ext+(n) * (block_w+cap_off_h)
                    xh_cap = bot_ext+(n+1)*(block_w)+(n)*cap_off_h
                    yl_cap = y_bot
                    yh_cap = y_bot+unit_height

                    xl_via = (bot_ext+via_bnd)+n*(block_w+cap_off_h)
                    xh_via = bot_ext-via_bnd+(n+1)*(block_w)+n*cap_off_h
                    yl_via = y_bot + cap_bound
                    yh_via = y_bot+unit_height-via_bnd

                    builder.add_rect_arr(cap_lay, BBox(xl_cap, yl_cap,
                                                       xh_cap, yh_cap))
                    builder.add_via(get_via_info(via_type,
                                                 BBox(xl_via, yl_via,
                                                      xh_via, yh_via),
                                                 via_dim, via_sp, via_bot_enc,
                                                 via_top_enc))
            if (dum_columns > 0):
                # for the actual cap
                xl_top = width_total-width+(dum_columns)*cap_off_h + bot_ext
                xh_top = width_total+(tot_columns-1)*cap_off_h+top_ext + \
                             bot_ext+cap_bound
                yl_top = bot_sp+cap_bound
                yh_top = height+(rows-1)*cap_off+bot_sp+cap_bound

                xl_bot = width_total-width+(dum_columns)*cap_off_h
                xh_bot = width_total+(tot_columns-1)*cap_off_h + \
                             bot_ext+cap_bound
                yl_bot = bot_sp
                yh_bot = height+(rows-1)*cap_off+2*cap_bound+bot_sp

                builder.add_rect_arr(bot_metal, BBox(xl_bot, yl_bot, 
                                                     xh_bot, yh_bot))
                builder.add_rect_arr(top_metal, BBox(xl_top, yl_top,
                                                     xh_top, yh_top))
                # for the dummy
                xl_dtop = bot_ext
                xh_dtop = width_total-width+(dum_columns-1)*cap_off_h + \
                              bot_ext+cap_bound
                yl_dtop = bot_sp+cap_bound
                yh_dtop = height+(rows-1)*cap_off+bot_sp+cap_bound

                xl_dbot = 0
                xh_dbot = width_total-width+(dum_columns-1)*cap_off_h + \
                              bot_ext+cap_bound
                yl_dbot = bot_sp
                yh_dbot = height+(rows-1)*cap_off+2*cap_bound+bot_sp

                builder.add_rect_arr(bot_metal, BBox(xl_dbot, yl_dbot,
                                                     xh_dbot, yh_dbot))
                builder.add_rect_arr(top_metal, BBox(xl_dtop, yl_dtop,
                                                     xh_dtop, yh_dtop))
            else:
                xl_top = bot_ext
                xh_top = width+(tot_columns-1)*cap_off_h+(top_ext+bot_ext)
                yl_top = bot_sp+cap_bound
                yh_top = height+(rows-1)*cap_off+bot_sp+cap_bound

                xl_bot = 0
                xh_bot = width+(tot_columns-1)*cap_off_h+bot_ext+cap_bound
                yl_bot = bot_sp
                yh_bot = height+(rows-1)*cap_off+2*cap_bound+bot_sp

                builder.add_rect_arr(bot_metal, BBox(xl_bot, yl_bot,
                                                     xh_bot, yh_bot))
                builder.add_rect_arr(top_metal, BBox(xl_top, yl_top,
                                                     xh_top, yh_top))

            # add top metal and bottom 
            w_tot = xh_top
            h_tot = bot_sp+cap_bound+height+(rows-1)*cap_off + cap_off
            
            pin_bot_yl = bot_sp
            pin_bot_yh = h_tot-cap_off

            pin_top_yl = bot_sp+cap_bound
            pin_top_yh = h_tot-cap_off
            pin_bot_xh = width_total-width+(dum_columns)*cap_off_h
            
            bnd_box = BBox(0, 0, w_tot, h_tot)

        # not arrayed
        else:
            xl_top = bot_ext
            xh_top = width+(top_ext+bot_ext)
            yl_top = bot_sp+cap_bound
            yh_top = height+bot_sp+cap_bound

            xl_bot = 0
            xh_bot = width+bot_ext+cap_bound
            yl_bot = bot_sp
            yh_bot = height+2*cap_bound+bot_sp

            builder.add_rect_arr(bot_metal, BBox(xl_bot, yl_bot,
                                                 xh_bot, yh_bot))
            builder.add_rect_arr(top_metal, BBox(xl_top, yl_top,
                                                 xh_top, yh_top))

            # This only sections long widths
            if (width/height > ratio): 
                num_blocks = -(-max(width, height) //
                                              (20*min(width, height)))

                block_w = -(-(width-(num_blocks-1)*cap_off)//num_blocks)
                for n in range(0, num_blocks):
                    xl_cap = bot_ext+(n)*(block_w+cap_off)
                    xh_cap = bot_ext+(n+1)*(block_w)+(n)*cap_off
                    yl_cap = bot_sp+cap_bound
                    yh_cap = height+cap_bound+bot_sp

                    xl_via = (bot_ext+via_bnd)+n*(block_w+cap_off)
                    xh_via = bot_ext-via_bnd+(n+1)*(block_w)+n*cap_off
                    yl_via = bot_sp+2*cap_bound
                    yh_via = height+cap_bound+bot_sp-via_bnd

                    builder.add_rect_arr(cap_lay, BBox(xl_cap, yl_cap,
                                                       xh_cap, yh_cap))
                    builder.add_via(get_via_info(via_type, 
                                                 BBox(xl_via, yl_via,
                                                      xh_via, yh_via),
                                                 via_dim, via_sp,
                                                 via_bot_enc, via_top_enc))
 
            else:
                xl_cap = bot_ext
                xh_cap = bot_ext+width
                yl_cap = bot_sp+cap_bound
                yh_cap = height+cap_bound+bot_sp

                xl_via = bot_ext+via_bnd
                xh_via = bot_ext+width-via_bnd
                yl_via = bot_sp+cap_bound+via_bnd
                yh_via = height+bot_sp
                builder.add_rect_arr(cap_lay, BBox(xl_cap, yl_cap,
                                                   xh_cap, yh_cap))
                builder.add_via(get_via_info(via_type,
                                             BBox(xl_via, yl_via,
                                                  xh_via, yh_via),
                                             via_dim, via_sp,
                                             via_bot_enc, via_top_enc))
        
            w_tot = bot_ext+width+top_ext
            h_tot = bot_sp+2*cap_bound+height+cap_off

            pin_bot_yl = bot_sp
            pin_bot_yh = height+2*cap_bound+bot_sp

            pin_top_yl = bot_sp+cap_bound
            pin_top_yh = bot_sp+height+cap_bound
            pin_bot_xh = 0

            # # set size
            bnd_box = BBox(0, 0, w_tot, h_tot)
        
        return MIMLayInfo(builder.get_info(bnd_box),
                          pin_bot_yl, pin_bot_yh, pin_top_yl,
                          pin_top_yh, pin_bot_xh)
     

def get_via_info(via_type: str, box: BBox,
                 via_dim: int, via_sp: int, bot_enc: int,
                 top_enc: int) -> ViaInfo:
    """Create vias over specified area."""
    xc = int((box.xl + box.xh)//2)
    yc = int((box.yl + box.yh)//2)

    enc1 = (bot_enc, bot_enc, bot_enc, bot_enc)
    enc2 = (top_enc, top_enc, top_enc, top_enc)

    vnx = (int(box.xh - box.xl)//(int(via_dim+via_sp)))
    vny = (int(box.yh - box.yl)//(int(via_dim+via_sp)))

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
    # vnx: vias x direction
    # vny: vias y direction
    # vspx: via x spacing
    # vspy: via y spacing
    # nx: int = 1
    # ny: int = 1
    # spx: int = 0
    # spy: int = 0
 