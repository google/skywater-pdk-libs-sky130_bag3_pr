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
