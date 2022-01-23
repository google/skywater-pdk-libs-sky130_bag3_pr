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
#
# CDSLIBRARY entry - add this entry if the directory containing
# this cdsinfo.tag file is the root of a Cadence library.
# CDSLIBRARY
#
# CDSLIBCHECK - set this entry to require that libraries have
# a cdsinfo.tag file with a CDSLIBRARY entry. Legal values are
# ON and OFF. By default (OFF), directories named in a cds.lib file
# do not have to have a cdsinfo.tag file with a CDSLIBRARY entry.
# CDSLIBCHECK ON
#
# DMTYPE - set this entry to define the DM system for Cadence's
# Generic DM facility. Values will be shifted to lower case.
# DMTYPE none
# DMTYPE crcs
# DMTYPE tdm
# DMTYPE sync
#
# NAMESPACE - set this entry to define the library namespace according
# to the type of machine on which the data is stored. Legal values are
# `LibraryNT' and
# `LibraryUnix'.
# NAMESPACE LibraryUnix
#
# Other entries may be added for use by specific applications as
# name-value pairs. Application documentation will describe the
# use and behaviour of these entries when appropriate.
#
# Current Settings:
#
CDSLIBRARY
DMTYPE none
NAMESPACE LibraryUnix
