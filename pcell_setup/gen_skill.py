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
# mos_w_default = '0.42'
# mos_l_default = '0.15'
res_w_default = '1u'
res_l_default = '2u'
res_metal_w_default = '400n'
res_metal_l_default = '1u'
dio_w_default = '1u'
dio_l_default = '1u'

mos_list = [
    ('nmos4', 'standard', 'nfet', 'nshort', '0.42', '0.15'),
    ('nmos4', 'svt', 'nfet', 'nshort', '0.42', '0.15'),
    ('nmos4', 'hv', 'nfet', 'nhv', '0.75', '0.50'),
    ('nmos4', 'hvesd', 'nfet', 'nhvesd', '17.50', '0.55'),
    ('nmos4', 'lvt', 'nfet', 'nlowvt', '0.42', '0.15'),
    ('pmos4', 'standard', 'pfet', 'pshort', '0.55', '0.15'),
    ('pmos4', 'svt', 'pfet', 'pshort', '0.55', '0.15'),
    ('pmos4', 'hvt', 'pfet', 'phighvt', '0.54', '0.15'),
    ('pmos4', 'hv', 'pfet', 'phv', '0.42', '0.50'),
    ('pmos4', 'hvesd', 'pfet', 'phvesd', '14.50', '0.55'),
    ('pmos4', 'lvt', 'pfet', 'plowvt', '0.55', '0.35'),
]

res_list = [
]

res_metal_list = [
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
        res_w_default=res_w_default,
        res_l_default=res_l_default,
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
