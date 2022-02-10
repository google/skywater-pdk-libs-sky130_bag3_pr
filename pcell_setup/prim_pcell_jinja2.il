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

{% for mtype, threshold, model, model_thres, w_def, l_def in mos_list  %}
; {{ mtype }}_{{ threshold }}/{{ model_thres }}
pcDefinePCell(
    list( lib_obj "{{ mtype }}_{{ threshold }}" "schematic" "schematic")
    ((w string "{{ w_def }}")
     (l string "{{ l_def }}")
     (nf string "1")
    )
    let((inst iopin_master io_net io_pin)
        wval = atoi(w)
        nval = atoi(nf)
        inst = dbCreateParamInstByMasterName( pcCellView "{{ tech_lib }}" "{{ model }}" "symbol"
                                              "N0" -0.375:0 "R0" 1
                                              list(list("hspiceModelMenu" "string" "{{ model_thres }}")
                                                   list("w" "string" w)
                                                   list("l" "string" l)
                                                   list("m" "string" nf)
                                                   list("totalW" "string" sprintf(nil "%dn" wval * nval)))
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
{% endfor %}

{% for intent, model in res_list  %}
; res_{{ intent }}/{{ model }}
pcDefinePCell(
    list( lib_obj "res_{{ intent }}" "schematic" "schematic")
    ((w string "{{ res_w_default }}")
     (l string "{{ res_l_default }}")
    )
    let((inst iopin_master io_net io_pin)
        inst = dbCreateParamInstByMasterName( pcCellView "{{ tech_lib }}" "{{ model }}" "symbol"
                                              "R0" 0.5:0 "R270" 1
                                              list(list("w" "string" w)
                                                   list("l" "string" l)
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
    )
)
{% endfor %}

{% for layer, model, rsq in res_metal_list  %}
; res_metal_{{ layer }}/{{ model }}
pcDefinePCell(
    list( lib_obj "res_metal_{{ layer }}" "schematic" "schematic")
    ((w string "{{ res_metal_w_default }}")
     (l string "{{ res_metal_l_default }}")
    )
    let((inst iopin_master io_net io_pin wval lval rval)
        wval = cdfParseFloatString(w)
        lval = cdfParseFloatString(l)
        rval = {{ rsq }}*lval/wval
        inst = dbCreateParamInstByMasterName( pcCellView "{{ tech_lib }}" "{{ model }}" "symbol"
                                              "R0" 0.1:0 "R90" 1
                                              list(list("w" "string" w)
                                                   list("l" "string" l)
                                                   list("effw" "string" w)
                                                   list("effl" "string" l)
                                                   list("r" "float" rval)
                                                  )
                                            )

        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "PLUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "PLUS" -0.15:0 "R0")
                             "PLUS" dbCreateTerm(io_net "PLUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "PLUS"))
        io_net = dbCreateNet(pcCellView "MINUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "MINUS" 1.15:0 "R0")
                             "MINUS" dbCreateTerm(io_net "MINUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "MINUS"))
    )
)
{% endfor %}


{% for dtype, intent, model in dio_list  %}
; {{ dtype }}_{{ intent }}/{{ model }}
pcDefinePCell(
    list( lib_obj "{{ dtype }}_{{ intent }}" "schematic" "schematic")
    ((w string "{{ dio_w_default }}")
     (l string "{{ dio_l_default }}")
    )
    let((inst iopin_master io_net io_pin wval lval dio_w dio_l)
        wval = atoi(w)
        lval = atoi(l)
        dio_w = (wval - 1)*48 + 14
        dio_l = (lval + 1)*86 - 18

        inst = dbCreateParamInstByMasterName( pcCellView "{{ tech_lib }}" "{{ model }}" "symbol"
                                              "R0" 0.1:0 "R90" 1
                                              list(list("nfin" "string" w)
                                                   list("fw" "string" sprintf(nil "%dn" dio_w))
                                                   list("nf" "string" l)
                                                   list("dl" "string" sprintf(nil "%dn" dio_l))
                                                   list("m" "string" "1")
                                                   list("area" "float" dio_w*dio_l*1e-18)
                                                   list("pj" "float" 2*1e-9*(dio_w + dio_l))
                                                  )
                                            )

        iopin_master = dbOpenCellViewByType("basic" "iopin" "symbolr" nil "r")
        io_net = dbCreateNet(pcCellView "PLUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "PLUS" -0.15:0 "R0")
                             "PLUS" dbCreateTerm(io_net "PLUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "PLUS"))
        io_net = dbCreateNet(pcCellView "MINUS")
        io_pin = dbCreatePin(io_net dbCreateInst(pcCellView iopin_master "MINUS" 1.15:0 "R0")
                             "MINUS" dbCreateTerm(io_net "MINUS" "inputOutput"))
        dbCreateInstTerm(io_net inst dbFindTermByName(inst~>master "MINUS"))
    )
)
{% endfor %}