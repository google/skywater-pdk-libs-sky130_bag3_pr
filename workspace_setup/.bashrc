#! /usr/bin/env bash
export PYTHONPATH=""

### Setup BAG
source .bashrc_bag

export PDK_HOME=$BAG_TECH_CONFIG_DIR/workspace_setup/PDK
export SW_PDK_ROOT=/tools/commercial/skywater
export SW_IP_HOME=${SW_PDK_ROOT}/s8_ip
export METAL_STACK="s8phirs_10r"

# location of various tools
export MGC_HOME=/path/to/mentor/calibre/aoi_cal_2022.2_24.16
export CDS_INST_DIR=/path/to/cadence/ICADVM/ICADVM181
export PVS_HOME=/path/to/cadence/PVS/PVS151
export SPECTRE_HOME=/path/to/cadence/SPECTRE/SPECTRE201
export QRC_HOME=/path/to/cadence/EXT/EXT191_ISR3
export SRR_HOME=/path/to/cadence/SRR/SRR_0618 #Not necessary if not using simulator dataparsing features
export CMAKE_HOME=/path/to/programs/cmake-3.17.0-Linux-x86_64

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
export PATH=/path/to/programs/core/bin:${PATH} # location of dependency binaries, likely same parent directory as CMAKE

# LD_LIBRARY_PATH setup
# export LD_LIBRARY_PATH=${OA_LINK_DIR}:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${BAG_WORK_DIR}/cadence_libs:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${SRR_HOME}/tools/lib/64bit:${LD_LIBRARY_PATH:-}
export LD_LIBRARY_PATH=${BAG_TOOLS_ROOT}/lib:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=$/path/to/programs/core/lib:${LD_LIBRARY_PATH} # location of dependency lib
export LD_LIBRARY_PATH=$/path/to/programs/core/lib64:${LD_LIBRARY_PATH} # location of dependency lib64

# PYTHONPATH_CUSTOM setup
export PYTHONPATH_CUSTOM=${PYTHONPATH_CUSTOM}:${SRR_HOME}/tools/srrpython  #Not necessary if not using simulator dataparsing features

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
