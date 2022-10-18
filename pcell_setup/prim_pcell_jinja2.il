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
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        nval = atoi(nf)
        inst = dbCreateParamInstByMasterName( pcCellView "{{ tech_lib }}" "{{ model }}" "symbol"
                                              "N0" -0.375:0 "R0" 1
                                              list(list("hspiceModel" "string" "{{ model_thres }}")
                                                   list("hspiceModelMenu" "string" "{{ model_thres }}")
                                                   list("w" "string" sprintf(nil "%0.2f" wval))
                                                   list("{{ model_thres }}_l0_w" "string" sprintf(nil "%0.2f" wval))
                                                   list("l" "string" sprintf(nil "%0.2f" lval))
                                                   list("{{ model_thres }}_l" "string" sprintf(nil "%0.2f" lval))
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
{% endfor %}

{% for intent, model, w_def, l_def in res_list  %}
; res_{{ intent }}/{{ model }}
pcDefinePCell(
    list( lib_obj "res_{{ intent }}" "schematic" "schematic")
    ((w string "{{ w_def }}")
     (l string "{{ l_def }}")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        wstr = sprintf(nil "%0.3f" wval)
        lstr = sprintf(nil "%0.3f" lval)
        inst = dbCreateParamInstByMasterName( pcCellView "{{ tech_lib }}" "{{ model }}" "symbol"
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
{% endfor %}

{% for layer in res_metal_list  %}
; res_metal_{{ layer }}/mrm{{ layer }}
pcDefinePCell(
    list( lib_obj "res_metal_{{ layer }}" "schematic" "schematic")
    ((w string "{{ res_metal_w_default }}")
     (l string "{{ res_metal_l_default }}")
    )
    let((inst iopin_master io_net io_pin)
        wval = cdfParseFloatString(w) * 1e6
        lval = cdfParseFloatString(l) * 1e6
        wstr = sprintf(nil "%0.3f" wval)
        lstr = sprintf(nil "%0.3f" lval)
        inst = dbCreateParamInstByMasterName( pcCellView "{{ tech_lib }}" "res" "symbol"
                                              "R0" 0.1:0 "R90" 1
                                              list(list("resistorTypr" "string" "met{{ layer }}")
                                                   list("rw" "string" wstr)
                                                   list("rl" "string" lstr)
                                                   list("model" "string" "mrm{{ layer }}")
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
