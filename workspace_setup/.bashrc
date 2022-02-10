#! /usr/bin/env bash

### Setup BAG
export BAG_TOOLS_ROOT=/tools/bag3/core
source .bashrc_bag

# PDK specific stuff
export SW_PDK_ROOT=${BAG_TECH_CONFIG_DIR}/workspace_setup/PDK_root
export PDK_HOME=${BAG_TECH_CONFIG_DIR}/workspace_setup/PDK
export METAL_STACK=s8phirs_10r

# calibre setup
export MGLS_LICENSE_FILE=5282@login1.bcanalog.com
export MGC_HOME=/tools/mentor/aoi_cal_2018.1_27.18
export MGLS_HOME=/tools/mentor/mgls
export CALIBRE_HOME=$MGC_HOME

# location of various tools
export CDS_INST_DIR=/tools/cadence/IC618
export PEGASUS_HOME=/tools/cadence/PEGASUS184
export SRR_HOME=/tools/cadence/SRR
# export CDS_INST_DIR=/tools/cadence/IC618
export SPECTRE_HOME=/tools/cadence/SPECTRE181
export QRC_HOME=/tools/cadence/EXT191
export INNOVUSHOME=/tools/cadence/installs/INNOVUS181
export CDSLIB_HOME=/tools/bag3/programs/cdsLibPlugin
export LATEX_BIN=/tools/texlive/2019/bin/x86_64-linux

export CDSHOME=$CDS_INST_DIR
export CDSLIB_TOOL=${CDSLIB_HOME}/tools.lnx86
export MMSIM_HOME=${SPECTRE_HOME}

# OA settings
export OA_SRC_ROOT=/tools/bag3/programs/oa_22d6
export OA_LINK_DIR=${OA_SRC_ROOT}/lib/linux_rhel60_64/opt
# export OA_LINK_DIR=${OA_SRC_ROOT}/lib/linux_rhel50_gcc48x_64/opt
export OA_CDS_ROOT=${CDS_INST_DIR}/oa_v22.60.007
export OA_INCLUDE_DIR=${OA_SRC_ROOT}/include
export OA_PLUGIN_PATH=${CDSLIB_HOME}/share/oaPlugIns:${OA_CDS_ROOT}/data/plugins:${OA_PLUGIN_PATH:-}
export OA_BIT=64

# PATH setup
export PATH=${MGLS_HOME}/bin:${PATH}
export PATH=${CALIBRE_HOME}/bin:${PATH}
export PATH=${CDSLIB_TOOL}/bin:${PATH}
export PATH=${PEGASUS_HOME}/bin:${PATH}
export PATH=${CDS_INST_DIR}/tools/plot/bin:${PATH}
export PATH=${CDS_INST_DIR}/tools/dfII/bin:${PATH}
export PATH=${CDS_INST_DIR}/tools/bin:${PATH}
export PATH=${MMSIM_HOME}/bin:${PATH}
export PATH=${QRC_HOME}/bin:${PATH}
export PATH=${LATEX_BIN}:${PATH}
export PATH=${BAG_TOOLS_ROOT}/bin:${PATH}

# LD_LIBRARY_PATH setup
export LD_LIBRARY_PATH=${CDSLIB_TOOL}/lib/64bit:${LD_LIBRARY_PATH:-}
export LD_LIBRARY_PATH=${OA_LINK_DIR}:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${BAG_TOOLS_ROOT}/lib64:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${BAG_TOOLS_ROOT}/lib:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${SRR_HOME}/tools/lib/64bit:${LD_LIBRARY_PATH}

# Virtuoso options
export SPECTRE_DEFAULTS=-E
export CDS_Netlisting_Mode="Analog"
export CDS_AUTO_64BIT=ALL
export CDS_LIC_FILE=5280@login1.bcanalog.com

# pybag compiler settings
export CMAKE_PREFIX_PATH=${BAG_TOOLS_ROOT}
export HDF5_PLUGIN_PATH=${BAG_TOOLS_ROOT}/lib/hdf5/plugin

# clear out PYTHONPATH
export PYTHONPATH=""
export PYTHONPATH_CUSTOM=${SRR_HOME}/tools/srrpython
