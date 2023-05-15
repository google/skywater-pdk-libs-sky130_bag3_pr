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

;; This skill file compiles schematic PCells for BAG primitives

lib_obj = ddGetObj("BAG_prim")


; nmos4_standard/nshort
pcDefinePCell(
    list( lib_obj "nmos4_standard" "schematic" "schematic")
    ((w string "420n")
     (l string "150n")
     (nf string "1")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        nval = atoi(nf)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "nfet" "symbol"
                                              "N0" -0.375:0 "R0" 1
                                              list(list("hspiceModel" "string" "nshort")
                                                   list("hspiceModelMenu" "string" "nshort")
                                                   list("w" "string" sprintf(nil "%0.2f" wval))
                                                   list("nshort_l0_w" "string" sprintf(nil "%0.2f" wval))
                                                   list("l" "string" sprintf(nil "%0.2f" lval))
                                                   list("nshort_l" "string" sprintf(nil "%0.2f" lval))
                                                   list("m" "string" nf)
                                                   list("totalW" "string" sprintf(nil "%0.2f" wval * nval)))
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "D")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "D" -0.5:0.5625 "R0")
                             "D" dbCreateTerm(io_net "D" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "d"))
        io_net = dbCreateNet(pcCellView "G")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "G" -0.875:0 "R0")
                             "G" dbCreateTerm(io_net "G" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "g"))
        io_net = dbCreateNet(pcCellView "S")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "S" -0.5:-0.5 "R0")
                             "S" dbCreateTerm(io_net "S" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "s"))
        io_net = dbCreateNet(pcCellView "B")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "B" 0.125:0 "R0")
                             "B" dbCreateTerm(io_net "B" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "b"))
    )
)

; nmos4_svt/nshort
pcDefinePCell(
    list( lib_obj "nmos4_svt" "schematic" "schematic")
    ((w string "420n")
     (l string "150n")
     (nf string "1")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        nval = atoi(nf)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "nfet" "symbol"
                                              "N0" -0.375:0 "R0" 1
                                              list(list("hspiceModel" "string" "nshort")
                                                   list("hspiceModelMenu" "string" "nshort")
                                                   list("w" "string" sprintf(nil "%0.2f" wval))
                                                   list("nshort_l0_w" "string" sprintf(nil "%0.2f" wval))
                                                   list("l" "string" sprintf(nil "%0.2f" lval))
                                                   list("nshort_l" "string" sprintf(nil "%0.2f" lval))
                                                   list("m" "string" nf)
                                                   list("totalW" "string" sprintf(nil "%0.2f" wval * nval)))
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "D")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "D" -0.5:0.5625 "R0")
                             "D" dbCreateTerm(io_net "D" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "d"))
        io_net = dbCreateNet(pcCellView "G")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "G" -0.875:0 "R0")
                             "G" dbCreateTerm(io_net "G" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "g"))
        io_net = dbCreateNet(pcCellView "S")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "S" -0.5:-0.5 "R0")
                             "S" dbCreateTerm(io_net "S" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "s"))
        io_net = dbCreateNet(pcCellView "B")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "B" 0.125:0 "R0")
                             "B" dbCreateTerm(io_net "B" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "b"))
    )
)

; nmos4_hv/nhv
pcDefinePCell(
    list( lib_obj "nmos4_hv" "schematic" "schematic")
    ((w string "750n")
     (l string "500n")
     (nf string "1")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        nval = atoi(nf)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "nfet" "symbol"
                                              "N0" -0.375:0 "R0" 1
                                              list(list("hspiceModel" "string" "nhv")
                                                   list("hspiceModelMenu" "string" "nhv")
                                                   list("w" "string" sprintf(nil "%0.2f" wval))
                                                   list("nhv_l0_w" "string" sprintf(nil "%0.2f" wval))
                                                   list("l" "string" sprintf(nil "%0.2f" lval))
                                                   list("nhv_l" "string" sprintf(nil "%0.2f" lval))
                                                   list("m" "string" nf)
                                                   list("totalW" "string" sprintf(nil "%0.2f" wval * nval)))
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "D")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "D" -0.5:0.5625 "R0")
                             "D" dbCreateTerm(io_net "D" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "d"))
        io_net = dbCreateNet(pcCellView "G")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "G" -0.875:0 "R0")
                             "G" dbCreateTerm(io_net "G" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "g"))
        io_net = dbCreateNet(pcCellView "S")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "S" -0.5:-0.5 "R0")
                             "S" dbCreateTerm(io_net "S" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "s"))
        io_net = dbCreateNet(pcCellView "B")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "B" 0.125:0 "R0")
                             "B" dbCreateTerm(io_net "B" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "b"))
    )
)

; nmos4_hvesd/nhvesd
pcDefinePCell(
    list( lib_obj "nmos4_hvesd" "schematic" "schematic")
    ((w string "17500n")
     (l string "550n")
     (nf string "1")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        nval = atoi(nf)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "nfet" "symbol"
                                              "N0" -0.375:0 "R0" 1
                                              list(list("hspiceModel" "string" "nhvesd")
                                                   list("hspiceModelMenu" "string" "nhvesd")
                                                   list("w" "string" sprintf(nil "%0.2f" wval))
                                                   list("nhvesd_l0_w" "string" sprintf(nil "%0.2f" wval))
                                                   list("l" "string" sprintf(nil "%0.2f" lval))
                                                   list("nhvesd_l" "string" sprintf(nil "%0.2f" lval))
                                                   list("m" "string" nf)
                                                   list("totalW" "string" sprintf(nil "%0.2f" wval * nval)))
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "D")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "D" -0.5:0.5625 "R0")
                             "D" dbCreateTerm(io_net "D" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "d"))
        io_net = dbCreateNet(pcCellView "G")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "G" -0.875:0 "R0")
                             "G" dbCreateTerm(io_net "G" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "g"))
        io_net = dbCreateNet(pcCellView "S")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "S" -0.5:-0.5 "R0")
                             "S" dbCreateTerm(io_net "S" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "s"))
        io_net = dbCreateNet(pcCellView "B")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "B" 0.125:0 "R0")
                             "B" dbCreateTerm(io_net "B" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "b"))
    )
)

; nmos4_lvt/nlowvt
pcDefinePCell(
    list( lib_obj "nmos4_lvt" "schematic" "schematic")
    ((w string "420n")
     (l string "150n")
     (nf string "1")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        nval = atoi(nf)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "nfet" "symbol"
                                              "N0" -0.375:0 "R0" 1
                                              list(list("hspiceModel" "string" "nlowvt")
                                                   list("hspiceModelMenu" "string" "nlowvt")
                                                   list("w" "string" sprintf(nil "%0.2f" wval))
                                                   list("nlowvt_l0_w" "string" sprintf(nil "%0.2f" wval))
                                                   list("l" "string" sprintf(nil "%0.2f" lval))
                                                   list("nlowvt_l" "string" sprintf(nil "%0.2f" lval))
                                                   list("m" "string" nf)
                                                   list("totalW" "string" sprintf(nil "%0.2f" wval * nval)))
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "D")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "D" -0.5:0.5625 "R0")
                             "D" dbCreateTerm(io_net "D" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "d"))
        io_net = dbCreateNet(pcCellView "G")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "G" -0.875:0 "R0")
                             "G" dbCreateTerm(io_net "G" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "g"))
        io_net = dbCreateNet(pcCellView "S")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "S" -0.5:-0.5 "R0")
                             "S" dbCreateTerm(io_net "S" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "s"))
        io_net = dbCreateNet(pcCellView "B")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "B" 0.125:0 "R0")
                             "B" dbCreateTerm(io_net "B" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "b"))
    )
)

; pmos4_standard/pshort
pcDefinePCell(
    list( lib_obj "pmos4_standard" "schematic" "schematic")
    ((w string "550n")
     (l string "150n")
     (nf string "1")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        nval = atoi(nf)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "pfet" "symbol"
                                              "N0" -0.375:0 "R0" 1
                                              list(list("hspiceModel" "string" "pshort")
                                                   list("hspiceModelMenu" "string" "pshort")
                                                   list("w" "string" sprintf(nil "%0.2f" wval))
                                                   list("pshort_l0_w" "string" sprintf(nil "%0.2f" wval))
                                                   list("l" "string" sprintf(nil "%0.2f" lval))
                                                   list("pshort_l" "string" sprintf(nil "%0.2f" lval))
                                                   list("m" "string" nf)
                                                   list("totalW" "string" sprintf(nil "%0.2f" wval * nval)))
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "D")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "D" -0.5:0.5625 "R0")
                             "D" dbCreateTerm(io_net "D" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "d"))
        io_net = dbCreateNet(pcCellView "G")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "G" -0.875:0 "R0")
                             "G" dbCreateTerm(io_net "G" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "g"))
        io_net = dbCreateNet(pcCellView "S")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "S" -0.5:-0.5 "R0")
                             "S" dbCreateTerm(io_net "S" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "s"))
        io_net = dbCreateNet(pcCellView "B")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "B" 0.125:0 "R0")
                             "B" dbCreateTerm(io_net "B" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "b"))
    )
)

; pmos4_svt/pshort
pcDefinePCell(
    list( lib_obj "pmos4_svt" "schematic" "schematic")
    ((w string "550n")
     (l string "150n")
     (nf string "1")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        nval = atoi(nf)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "pfet" "symbol"
                                              "N0" -0.375:0 "R0" 1
                                              list(list("hspiceModel" "string" "pshort")
                                                   list("hspiceModelMenu" "string" "pshort")
                                                   list("w" "string" sprintf(nil "%0.2f" wval))
                                                   list("pshort_l0_w" "string" sprintf(nil "%0.2f" wval))
                                                   list("l" "string" sprintf(nil "%0.2f" lval))
                                                   list("pshort_l" "string" sprintf(nil "%0.2f" lval))
                                                   list("m" "string" nf)
                                                   list("totalW" "string" sprintf(nil "%0.2f" wval * nval)))
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "D")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "D" -0.5:0.5625 "R0")
                             "D" dbCreateTerm(io_net "D" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "d"))
        io_net = dbCreateNet(pcCellView "G")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "G" -0.875:0 "R0")
                             "G" dbCreateTerm(io_net "G" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "g"))
        io_net = dbCreateNet(pcCellView "S")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "S" -0.5:-0.5 "R0")
                             "S" dbCreateTerm(io_net "S" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "s"))
        io_net = dbCreateNet(pcCellView "B")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "B" 0.125:0 "R0")
                             "B" dbCreateTerm(io_net "B" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "b"))
    )
)

; pmos4_hvt/phighvt
pcDefinePCell(
    list( lib_obj "pmos4_hvt" "schematic" "schematic")
    ((w string "540n")
     (l string "150n")
     (nf string "1")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        nval = atoi(nf)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "pfet" "symbol"
                                              "N0" -0.375:0 "R0" 1
                                              list(list("hspiceModel" "string" "phighvt")
                                                   list("hspiceModelMenu" "string" "phighvt")
                                                   list("w" "string" sprintf(nil "%0.2f" wval))
                                                   list("phighvt_l0_w" "string" sprintf(nil "%0.2f" wval))
                                                   list("l" "string" sprintf(nil "%0.2f" lval))
                                                   list("phighvt_l" "string" sprintf(nil "%0.2f" lval))
                                                   list("m" "string" nf)
                                                   list("totalW" "string" sprintf(nil "%0.2f" wval * nval)))
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "D")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "D" -0.5:0.5625 "R0")
                             "D" dbCreateTerm(io_net "D" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "d"))
        io_net = dbCreateNet(pcCellView "G")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "G" -0.875:0 "R0")
                             "G" dbCreateTerm(io_net "G" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "g"))
        io_net = dbCreateNet(pcCellView "S")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "S" -0.5:-0.5 "R0")
                             "S" dbCreateTerm(io_net "S" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "s"))
        io_net = dbCreateNet(pcCellView "B")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "B" 0.125:0 "R0")
                             "B" dbCreateTerm(io_net "B" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "b"))
    )
)

; pmos4_hv/phv
pcDefinePCell(
    list( lib_obj "pmos4_hv" "schematic" "schematic")
    ((w string "420n")
     (l string "500n")
     (nf string "1")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        nval = atoi(nf)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "pfet" "symbol"
                                              "N0" -0.375:0 "R0" 1
                                              list(list("hspiceModel" "string" "phv")
                                                   list("hspiceModelMenu" "string" "phv")
                                                   list("w" "string" sprintf(nil "%0.2f" wval))
                                                   list("phv_l0_w" "string" sprintf(nil "%0.2f" wval))
                                                   list("l" "string" sprintf(nil "%0.2f" lval))
                                                   list("phv_l" "string" sprintf(nil "%0.2f" lval))
                                                   list("m" "string" nf)
                                                   list("totalW" "string" sprintf(nil "%0.2f" wval * nval)))
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "D")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "D" -0.5:0.5625 "R0")
                             "D" dbCreateTerm(io_net "D" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "d"))
        io_net = dbCreateNet(pcCellView "G")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "G" -0.875:0 "R0")
                             "G" dbCreateTerm(io_net "G" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "g"))
        io_net = dbCreateNet(pcCellView "S")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "S" -0.5:-0.5 "R0")
                             "S" dbCreateTerm(io_net "S" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "s"))
        io_net = dbCreateNet(pcCellView "B")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "B" 0.125:0 "R0")
                             "B" dbCreateTerm(io_net "B" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "b"))
    )
)

; pmos4_hvesd/phvesd
pcDefinePCell(
    list( lib_obj "pmos4_hvesd" "schematic" "schematic")
    ((w string "14500n")
     (l string "550n")
     (nf string "1")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        nval = atoi(nf)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "pfet" "symbol"
                                              "N0" -0.375:0 "R0" 1
                                              list(list("hspiceModel" "string" "phvesd")
                                                   list("hspiceModelMenu" "string" "phvesd")
                                                   list("w" "string" sprintf(nil "%0.2f" wval))
                                                   list("phvesd_l0_w" "string" sprintf(nil "%0.2f" wval))
                                                   list("l" "string" sprintf(nil "%0.2f" lval))
                                                   list("phvesd_l" "string" sprintf(nil "%0.2f" lval))
                                                   list("m" "string" nf)
                                                   list("totalW" "string" sprintf(nil "%0.2f" wval * nval)))
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "D")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "D" -0.5:0.5625 "R0")
                             "D" dbCreateTerm(io_net "D" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "d"))
        io_net = dbCreateNet(pcCellView "G")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "G" -0.875:0 "R0")
                             "G" dbCreateTerm(io_net "G" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "g"))
        io_net = dbCreateNet(pcCellView "S")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "S" -0.5:-0.5 "R0")
                             "S" dbCreateTerm(io_net "S" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "s"))
        io_net = dbCreateNet(pcCellView "B")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "B" 0.125:0 "R0")
                             "B" dbCreateTerm(io_net "B" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "b"))
    )
)

; pmos4_lvt/plowvt
pcDefinePCell(
    list( lib_obj "pmos4_lvt" "schematic" "schematic")
    ((w string "550n")
     (l string "350n")
     (nf string "1")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        nval = atoi(nf)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "pfet" "symbol"
                                              "N0" -0.375:0 "R0" 1
                                              list(list("hspiceModel" "string" "plowvt")
                                                   list("hspiceModelMenu" "string" "plowvt")
                                                   list("w" "string" sprintf(nil "%0.2f" wval))
                                                   list("plowvt_l0_w" "string" sprintf(nil "%0.2f" wval))
                                                   list("l" "string" sprintf(nil "%0.2f" lval))
                                                   list("plowvt_l" "string" sprintf(nil "%0.2f" lval))
                                                   list("m" "string" nf)
                                                   list("totalW" "string" sprintf(nil "%0.2f" wval * nval)))
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "D")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "D" -0.5:0.5625 "R0")
                             "D" dbCreateTerm(io_net "D" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "d"))
        io_net = dbCreateNet(pcCellView "G")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "G" -0.875:0 "R0")
                             "G" dbCreateTerm(io_net "G" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "g"))
        io_net = dbCreateNet(pcCellView "S")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "S" -0.5:-0.5 "R0")
                             "S" dbCreateTerm(io_net "S" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "s"))
        io_net = dbCreateNet(pcCellView "B")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "B" 0.125:0 "R0")
                             "B" dbCreateTerm(io_net "B" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "b"))
    )
)



; res_standard/hrpoly
pcDefinePCell(
    list( lib_obj "res_standard" "schematic" "schematic")
    ((w string "1000n")
     (l string "2105n")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        wstr = sprintf(nil "%0.3f" wval)
        lstr = sprintf(nil "%0.3f" lval)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "hrpoly" "symbol"
                                              "R0" 0.5:0 "R270" 1
                                              list(list("segW" "string" wstr)
                                                   list("w" "string" wstr)
                                                   list("segL" "string" lstr)
                                                   list("l" "string" lstr)
                                                   list("rCalcMethod" "string" "Segment Length")
                                                  )
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "PLUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "PLUS" 1:0 "R0")
                             "PLUS" dbCreateTerm(io_net "PLUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "PLUS"))
        io_net = dbCreateNet(pcCellView "MINUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "MINUS" -0.15:0 "R0")
                             "MINUS" dbCreateTerm(io_net "MINUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "MINUS"))
        io_net = dbCreateNet(pcCellView "BULK")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "BULK" -0.15:-0.4 "R0")
                             "BULK" dbCreateTerm(io_net "BULK" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "B"))
    )
)

; res_high_res/uhrpoly
pcDefinePCell(
    list( lib_obj "res_high_res" "schematic" "schematic")
    ((w string "350n")
     (l string "17400n")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        wstr = sprintf(nil "%0.3f" wval)
        lstr = sprintf(nil "%0.3f" lval)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "uhrpoly" "symbol"
                                              "R0" 0.5:0 "R270" 1
                                              list(list("segW" "string" wstr)
                                                   list("w" "string" wstr)
                                                   list("segL" "string" lstr)
                                                   list("l" "string" lstr)
                                                   list("rCalcMethod" "string" "Segment Length")
                                                  )
                                            )
        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "PLUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "PLUS" 1:0 "R0")
                             "PLUS" dbCreateTerm(io_net "PLUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "PLUS"))
        io_net = dbCreateNet(pcCellView "MINUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "MINUS" -0.15:0 "R0")
                             "MINUS" dbCreateTerm(io_net "MINUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "MINUS"))
        io_net = dbCreateNet(pcCellView "BULK")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "BULK" -0.15:-0.4 "R0")
                             "BULK" dbCreateTerm(io_net "BULK" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "B"))
    )
)



; res_metal_1/mrm1
pcDefinePCell(
    list( lib_obj "res_metal_1" "schematic" "schematic")
    ((w string "720n")
     (l string "290n")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        wstr = sprintf(nil "%0.3f" wval)
        lstr = sprintf(nil "%0.3f" lval)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "res" "symbol"
                                              "R0" 0.1:0 "R90" 1
                                              list(list("resistorTypr" "string" "met1")
                                                   list("rw" "string" wstr)
                                                   list("rl" "string" lstr)
                                                   list("model" "string" "mrm1")
                                                  )
                                            )

        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "PLUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "PLUS" -0.15:0 "R0")
                             "PLUS" dbCreateTerm(io_net "PLUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "r0"))
        io_net = dbCreateNet(pcCellView "MINUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "MINUS" 1.15:0 "R0")
                             "MINUS" dbCreateTerm(io_net "MINUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "r1"))
    )
)

; res_metal_2/mrm2
pcDefinePCell(
    list( lib_obj "res_metal_2" "schematic" "schematic")
    ((w string "720n")
     (l string "290n")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        wstr = sprintf(nil "%0.3f" wval)
        lstr = sprintf(nil "%0.3f" lval)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "res" "symbol"
                                              "R0" 0.1:0 "R90" 1
                                              list(list("resistorTypr" "string" "met2")
                                                   list("rw" "string" wstr)
                                                   list("rl" "string" lstr)
                                                   list("model" "string" "mrm2")
                                                  )
                                            )

        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "PLUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "PLUS" -0.15:0 "R0")
                             "PLUS" dbCreateTerm(io_net "PLUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "r0"))
        io_net = dbCreateNet(pcCellView "MINUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "MINUS" 1.15:0 "R0")
                             "MINUS" dbCreateTerm(io_net "MINUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "r1"))
    )
)

; res_metal_3/mrm3
pcDefinePCell(
    list( lib_obj "res_metal_3" "schematic" "schematic")
    ((w string "720n")
     (l string "290n")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        wstr = sprintf(nil "%0.3f" wval)
        lstr = sprintf(nil "%0.3f" lval)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "res" "symbol"
                                              "R0" 0.1:0 "R90" 1
                                              list(list("resistorTypr" "string" "met3")
                                                   list("rw" "string" wstr)
                                                   list("rl" "string" lstr)
                                                   list("model" "string" "mrm3")
                                                  )
                                            )

        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "PLUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "PLUS" -0.15:0 "R0")
                             "PLUS" dbCreateTerm(io_net "PLUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "r0"))
        io_net = dbCreateNet(pcCellView "MINUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "MINUS" 1.15:0 "R0")
                             "MINUS" dbCreateTerm(io_net "MINUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "r1"))
    )
)

; res_metal_4/mrm4
pcDefinePCell(
    list( lib_obj "res_metal_4" "schematic" "schematic")
    ((w string "720n")
     (l string "290n")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        wstr = sprintf(nil "%0.3f" wval)
        lstr = sprintf(nil "%0.3f" lval)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "res" "symbol"
                                              "R0" 0.1:0 "R90" 1
                                              list(list("resistorTypr" "string" "met4")
                                                   list("rw" "string" wstr)
                                                   list("rl" "string" lstr)
                                                   list("model" "string" "mrm4")
                                                  )
                                            )

        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "PLUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "PLUS" -0.15:0 "R0")
                             "PLUS" dbCreateTerm(io_net "PLUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "r0"))
        io_net = dbCreateNet(pcCellView "MINUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "MINUS" 1.15:0 "R0")
                             "MINUS" dbCreateTerm(io_net "MINUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "r1"))
    )
)

; res_metal_5/mrm5
pcDefinePCell(
    list( lib_obj "res_metal_5" "schematic" "schematic")
    ((w string "720n")
     (l string "290n")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        wstr = sprintf(nil "%0.3f" wval)
        lstr = sprintf(nil "%0.3f" lval)
        inst = dbCreateParamInstByMasterName( pcCellView "s8phirs_10r" "res" "symbol"
                                              "R0" 0.1:0 "R90" 1
                                              list(list("resistorTypr" "string" "met5")
                                                   list("rw" "string" wstr)
                                                   list("rl" "string" lstr)
                                                   list("model" "string" "mrm5")
                                                  )
                                            )

        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "PLUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "PLUS" -0.15:0 "R0")
                             "PLUS" dbCreateTerm(io_net "PLUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "r0"))
        io_net = dbCreateNet(pcCellView "MINUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "MINUS" 1.15:0 "R0")
                             "MINUS" dbCreateTerm(io_net "MINUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "r1"))
    )
)



