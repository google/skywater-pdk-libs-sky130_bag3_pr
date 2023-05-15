;; Copyright 2019-2021 SkyWater PDK Authors
;;
;; Licensed under the Apache License, Version 2.0 (the "License");
;; you may not use this file except in compliance with the License.
;; You may obtain a copy of the License at
;;
;;     https://www.apache.org/licenses/LICENSE-2.0
;;
;; Unless required by applicable law or agreed to in writing, software
;; distributed under the License is distributed on an "AS IS" BASIS,
;; WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
;; See the License for the specific language governing permissions and
;; limitations under the License.
;;
;; This code is *alternatively* available under a BSD-3-Clause license, see
;; details in the README.md at the top level and the license text at
;; https://github.com/google/skywater-pdk-libs-sky130_bag3_pr/blob/master/LICENSE.alternative
;;
;; SPDX-License-Identifier: BSD-3-Clause OR Apache 2.0

;; This skill file compiles schematic PCells for BAG primitives for MIM

lib_obj = ddGetObj("BAG_prim")


; mim_standard/xcmimc2
pcDefinePCell(
    list( lib_obj "mim_standard" "schematic" "schematic")
    ((unit_width string "1u")
     (unit_height string "1u")
     (num_rows string "1")
     (num_cols string "1")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(unit_width) * 1e6
        lval = cdfParseFloatString(unit_height) * 1e6
        rval = atoi(num_rows)
        cval = atoi(num_cols)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "cmimc" "symbol"
                                              "C0" 0:0 "R0" 1
                                              list(list("ctype" "string" "xcmimc2")
                                                   list("cw" "string" sprintf(nil "%0.2f" wval))
                                                   list("cl" "string" sprintf(nil "%0.2f" lval))
                                                   list("nrow" "string" num_rows)
                                                   list("ncol" "string" num_cols)
                                                   list("cm" "string" sprintf(nil "%d" rval * cval)))
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "TOP")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "TOP" 0:0.5 "R0")
                             "TOP" dbCreateTerm(io_net "TOP" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "c0"))
        io_net = dbCreateNet(pcCellView "BOT")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "BOT" 0:-0.75 "R0")
                             "BOT" dbCreateTerm(io_net "BOT" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "c1"))
    )
)

; mim_45/xcmimc2
pcDefinePCell(
    list( lib_obj "mim_45" "schematic" "schematic")
    ((unit_width string "1u")
     (unit_height string "1u")
     (num_rows string "1")
     (num_cols string "1")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(unit_width) * 1e6
        lval = cdfParseFloatString(unit_height) * 1e6
        rval = atoi(num_rows)
        cval = atoi(num_cols)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "cmimc" "symbol"
                                              "C0" 0:0 "R0" 1
                                              list(list("ctype" "string" "xcmimc2")
                                                   list("cw" "string" sprintf(nil "%0.2f" wval))
                                                   list("cl" "string" sprintf(nil "%0.2f" lval))
                                                   list("nrow" "string" num_rows)
                                                   list("ncol" "string" num_cols)
                                                   list("cm" "string" sprintf(nil "%d" rval * cval)))
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "TOP")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "TOP" 0:0.5 "R0")
                             "TOP" dbCreateTerm(io_net "TOP" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "c0"))
        io_net = dbCreateNet(pcCellView "BOT")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "BOT" 0:-0.75 "R0")
                             "BOT" dbCreateTerm(io_net "BOT" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "c1"))
    )
)

; mim_34/xcmimc1
pcDefinePCell(
    list( lib_obj "mim_34" "schematic" "schematic")
    ((unit_width string "1u")
     (unit_height string "1u")
     (num_rows string "1")
     (num_cols string "1")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(unit_width) * 1e6
        lval = cdfParseFloatString(unit_height) * 1e6
        rval = atoi(num_rows)
        cval = atoi(num_cols)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "cmimc" "symbol"
                                              "C0" 0:0 "R0" 1
                                              list(list("ctype" "string" "xcmimc1")
                                                   list("cw" "string" sprintf(nil "%0.2f" wval))
                                                   list("cl" "string" sprintf(nil "%0.2f" lval))
                                                   list("nrow" "string" num_rows)
                                                   list("ncol" "string" num_cols)
                                                   list("cm" "string" sprintf(nil "%d" rval * cval)))
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "TOP")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "TOP" 0:0.5 "R0")
                             "TOP" dbCreateTerm(io_net "TOP" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "c0"))
        io_net = dbCreateNet(pcCellView "BOT")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "BOT" 0:-0.75 "R0")
                             "BOT" dbCreateTerm(io_net "BOT" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "c1"))
    )
)
