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

from typing import Optional, Tuple

from pybag.core import BBox

from xbase.layout.enum import MOSType
from xbase.layout.data import LayoutInfoBuilder


def add_base(builder: LayoutInfoBuilder, row_type: MOSType, threshold: str, imp_y: Tuple[int, int],
             rect: BBox, well_x: Optional[Tuple[int, int]] = None) -> None:
    # draws nwell, n+ implant (ndsm) and p+ implant (pdsm)
    # for non mos devices (corners, edges, etc)

    pimp_lp = ('psdm', 'drawing')
    if rect.is_physical():
        if not row_type.is_pwell:
            well_lp = ('nwell', 'drawing')
            if well_x is None:
                builder.add_rect_arr(well_lp, rect)
            else:
                builder.add_rect_arr(well_lp, BBox(well_x[0], rect.yl, well_x[1], rect.yh))
            
        thres_lp = _get_thres_lp(row_type, threshold)
        if thres_lp[0] != '':
            builder.add_rect_arr(thres_lp, rect)
    
def add_base_mos(builder: LayoutInfoBuilder, row_type: MOSType, threshold: str, imp_y: Tuple[int, int],
             rect: BBox, well_x: Optional[Tuple[int, int]] = None, is_sub: bool = False) -> None:
    # new func draws nwell, n+ implant (ndsm) and p+ implant (pdsm)
    
    pimp_lp = ('psdm', 'drawing')

    if rect.is_physical():
        # only draw nwells if not a tap cell and pch, or is tap cell and nch
        if ((not row_type.is_pwell) and (not is_sub)) \
                or (is_sub and (row_type is MOSType.nch or row_type is MOSType.ntap) ):
            well_lp = ('nwell', 'drawing')
            if well_x is None:
                builder.add_rect_arr(well_lp, rect)
            else:
                builder.add_rect_arr(well_lp, BBox(well_x[0], rect.yl, well_x[1], rect.yh))
            
        #draw the respective implant called    
        if (row_type is MOSType.nch):
            builder.add_rect_arr(('nsdm', 'drawing'),  BBox(rect.xl, imp_y[0], rect.xh, imp_y[1]))
        elif (row_type is MOSType.pch):
            builder.add_rect_arr(('psdm', 'drawing'),  BBox(rect.xl, imp_y[0], rect.xh, imp_y[1]))
        elif (row_type is MOSType.ntap):
            builder.add_rect_arr(('nsdm', 'drawing'),  BBox(rect.xl, imp_y[0], rect.xh, imp_y[1]))
        elif (row_type is MOSType.ptap):
            builder.add_rect_arr(('psdm', 'drawing'),  BBox(rect.xl, imp_y[0], rect.xh, imp_y[1]))

        thres_lp = _get_thres_lp(row_type, threshold)
        if thres_lp[0] != '':
            builder.add_rect_arr(thres_lp, rect)


def get_arr_edge_dim(arr_dim: int, edge_min_dim: int, blk_pitch: int, edge_pitch: int = 1,
                     edge_offset: int = 0) -> int:
    dim_tot = -(-(arr_dim + 2 * edge_min_dim) // blk_pitch) * blk_pitch
    dim2 = dim_tot - arr_dim
    if dim2 & 1 == 1:
        if blk_pitch & 1 == 1:
            dim2 += blk_pitch
        else:
            raise RuntimeError(f'Parity Error: impossible to center ArrayBase with '
                               f'arr_dim={arr_dim}, blk_pitch={blk_pitch}, '
                               f'and edge_min_dim={edge_min_dim}.')

    ans = dim2 // 2
    if (ans - edge_offset) % edge_pitch != 0:
        # precondition: we know that edge_pitch divides blk_pitch
        blk_pitch2 = blk_pitch // 2
        if blk_pitch & 1 != 0 or (ans + blk_pitch2 - edge_offset) % edge_pitch != 0:
            raise RuntimeError(f'Parity Error: impossible to center ArrayBase with '
                               f'arr_dim={arr_dim}, blk_pitch={blk_pitch}, '
                               f'edge_min_dim={edge_min_dim}, edge_pitch={edge_pitch}, '
                               f'and edge_offset={edge_offset}')
        ans += blk_pitch2

    return ans


def _get_thres_lp(row_type: MOSType, threshold: str) -> Tuple[str, str]:
    if threshold == 'standard':
        return '', ''
    if threshold == 'lvt':
        return 'lvtn', 'drawing'
    if threshold == 'hvt':
        if row_type.is_n_plus:
            raise ValueError('Threshold hvt not supported for nmos')
        return 'hvtp', 'drawing'
    raise ValueError(f'unknown threshold: {threshold}')
