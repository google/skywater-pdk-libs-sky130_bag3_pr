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


from jinja2 import Template

tech_lib = 's8phirs_10r'
# mos_w_default = '420n'
# mos_l_default = '150n'
# res_w_default = '1u'
# res_l_default = '2u'
res_metal_w_default = '720n'
res_metal_l_default = '290n'
dio_w_default = '1u'
dio_l_default = '1u'

mos_list = [
    ('nmos4', 'standard', 'nfet', 'nshort', '420n', '150n'),
    ('nmos4', 'svt', 'nfet', 'nshort', '420n', '150n'),
    ('nmos4', 'hv', 'nfet', 'nhv', '750n', '500n'),
    ('nmos4', 'hvesd', 'nfet', 'nhvesd', '17500n', '550n'),
    ('nmos4', 'lvt', 'nfet', 'nlowvt', '420n', '150n'),
    ('pmos4', 'standard', 'pfet', 'pshort', '550n', '150n'),
    ('pmos4', 'svt', 'pfet', 'pshort', '550n', '150n'),
    ('pmos4', 'hvt', 'pfet', 'phighvt', '540n', '150n'),
    ('pmos4', 'hv', 'pfet', 'phv', '420n', '500n'),
    ('pmos4', 'hvesd', 'pfet', 'phvesd', '14500n', '550n'),
    ('pmos4', 'lvt', 'pfet', 'plowvt', '550n', '350n'),
]

res_list = [
    ('standard', 'hrpoly', '1000n', '2105n'),
    ('high_res', 'uhrpoly', '350n', '17400n'),
]

res_metal_list = [
    '1',
    '2',
    '3',
    '4',
    '5',
]

dio_list = [
]


def run_main() -> None:
    in_fname = 'prim_pcell_jinja2.il'
    out_fname = 'prim_pcell.il'

    with open(in_fname, 'r') as f:
        content = f.read()

    result = Template(content).render(
        tech_lib=tech_lib,
        mos_list=mos_list,
        # mos_w_default=mos_w_default,
        # mos_l_default=mos_l_default,
        res_list=res_list,
        # res_w_default=res_w_default,
        # res_l_default=res_l_default,
        res_metal_list=res_metal_list,
        res_metal_w_default=res_metal_w_default,
        res_metal_l_default=res_metal_l_default,
        dio_list=dio_list,
        dio_w_default=dio_w_default,
        dio_l_default=dio_l_default,
    )

    with open(out_fname, 'w') as f:
        f.write(result)


if __name__ == '__main__':
    run_main()
