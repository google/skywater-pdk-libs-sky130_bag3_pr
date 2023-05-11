#! /usr/bin/env bash
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

export PYTHONPATH=""

### Setup BAG
source .bashrc_bag

export PDK_HOME=$BAG_TECH_CONFIG_DIR/workspace_setup/PDK
export SW_PDK_ROOT=/tools/commercial/skywater
export SW_IP_HOME=${SW_PDK_ROOT}/s8_ip
export METAL_STACK="s8phirs_10r"

# location of various tools
export MGC_HOME=/tools/mentor/calibre/aoi_cal_2022.2_24.16
export CDS_INST_DIR=/tools/cadence/ICADVM/ICADVM181
export PVS_HOME=/tools/cadence/PVS/PVS151
export SPECTRE_HOME=/tools/cadence/SPECTRE/SPECTRE201
export QRC_HOME=/tools/cadence/EXT/EXT191_ISR3
export CMAKE_HOME=/tools/C/bag/programs/cmake-3.17.0 

export CDSHOME=${CDS_INST_DIR}
export MMSIM_HOME=${SPECTRE_HOME}

# OA settings
export OA_CDS_ROOT=${CDS_INST_DIR}/oa_v22.60.s007
export OA_PLUGIN_PATH=${OA_CDS_ROOT}/data/plugins:${OA_PLUGIN_PATH:-}
export OA_BIT=64

# PATH setup
export PATH=${MGC_HOME}/bin:${PATH}
export PATH=${PVS_HOME}/bin:${PATH}
export PATH=${QRC_HOME}/bin:${PATH}
export PATH=${CDS_INST_DIR}/tools/plot/bin:${PATH}
export PATH=${CDS_INST_DIR}/tools/dfII/bin:${PATH}
export PATH=${CDS_INST_DIR}/tools/bin:${PATH}
export PATH=${MMSIM_HOME}/bin:${PATH}
export PATH=${BAG_TOOLS_ROOT}/bin:${PATH}
export PATH=${CMAKE_HOME}/bin:${PATH}

# LD_LIBRARY_PATH setup
export LD_LIBRARY_PATH=${BAG_WORK_DIR}/cadence_libs:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${BAG_TOOLS_ROOT}/lib:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${BAG_TOOLS_ROOT}/lib64:${LD_LIBRARY_PATH}

# Virtuoso options
export SPECTRE_DEFAULTS=-E
export CDS_Netlisting_Mode="Analog"
export CDS_AUTO_64BIT=ALL

# License setup
source /license/paths

# Setup LSF (BWRC specific)
# source /tools/support/lsf/conf/profile.lsf
# export LBS_BASE_SYSTEM=LBS_LSF

# Enable devtoolset
source /opt/rh/devtoolset-8/enable
source /opt/rh/rh-git29/enable
source /opt/rh/httpd24/enable

# pybag compiler settings
export CMAKE_PREFIX_PATH=${BAG_TOOLS_ROOT} 
