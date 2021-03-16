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


from typing import Any


from bag.design.module import MosModuleBase
from bag.design.database import ModuleDB
from bag.util.immutable import Param


# noinspection PyPep8Naming
class BAG_prim__nmos4_lvt(MosModuleBase):
    """design module for BAG_prim__nmos4_lvt.
    """

    def __init__(self, database: ModuleDB, params: Param, **kwargs: Any) -> None:
        MosModuleBase.__init__(self, '', database, params, **kwargs)
