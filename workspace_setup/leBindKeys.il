;;-----------------------------------------------------------------------------
;; Bindkeys for 'Layout'
;; Inherited by:
;;             * Dracula Interactive
;;             * High Capacity Power IR/EM
;;             * NC-Verilog-MaskLayout
;;             * Other-Layout
;;             * Other-MaskLayout
;;             * Other-Symbolic
;;             * Pcell
;;             * Power IR/EM
;;             * Spectre-Layout
;;             * Spectre-MaskLayout
;;             * Spectre-Symbolic
;;             * UltraSim-Layout
;;             * UltraSim-MaskLayout
;;             * UltraSim-Symbolic
;;             * VLS-GXL
;;             * Virtuoso CE
;;             * Virtuoso XL
;;             * adegxl-maskLayout
;;             * adexl-maskLayout
;;             * parasitics-MaskLayout
;;-----------------------------------------------------------------------------

procedure(enable_sch_layers()
    leSetLayerVisible( list("wire" "label") t )
    leSetLayerVisible( list("wire" "drawing") t )
    leSetLayerVisible( list("pin" "label") t )
    leSetLayerVisible( list("pin" "drawing") t )
    leSetLayerVisible( list("device" "drawing") t )
    leSetLayerVisible( list("device" "drawing1") t )
    leSetLayerVisible( list("device" "label") t )
    leSetLayerVisible( list("instance" "label") t )
    leSetLayerVisible( list("border" "drawing") t )

    leSetLayerVisible( list("instance" "drawing") t )
    leSetLayerVisible( list("text" "drawing") t )
    leSetLayerVisible( list("device" "annotate") t )
)

procedure(show_od_m1()
    leSetEntryLayer(list("poly" "drawing"))
    leSetAllLayerVisible(nil)
    leSetLayerVisible(list("nwell" "drawing") t)
    leSetLayerVisible(list("nsdm" "drawing") t)
    leSetLayerVisible(list("psdm" "drawing") t)
    leSetLayerVisible(list("npc" "drawing") t)
    leSetLayerVisible(list("diff" "drawing") t)
    leSetLayerVisible(list("tap" "drawing") t)
    leSetLayerVisible(list("poly" "drawing") t)
    leSetLayerVisible(list("lvtn" "drawing") t)
    leSetLayerVisible(list("hvtp" "drawing") t)
    leSetLayerVisible(list("li1" "drawing") t)
    leSetLayerVisible(list("licon1" "drawing") t)
    leSetLayerVisible(list("mcon" "drawing") t)
    leSetLayerVisible(list("met1" "drawing") t)
    leSetLayerVisible(list("met1" "pin") t)

    enable_sch_layers()
    hiRedraw()
)

procedure(toggle_od()
    leSetLayerVisible(list("diff" "drawing") not(leIsLayerVisible(list("diff" "drawing"))))
    hiRedraw()
)

procedure( show_adjacent_metals( bot_layer )
    let( (bot_name top_name via_name bot_dum top_dum)
        sprintf(bot_name "met%d" bot_layer)
	    if( bot_layer < 2 then
            sprintf(via_name "via")
        else
            sprintf(via_name "via%d" bot_layer)
        )
	    sprintf(top_name "met%d" bot_layer + 1)
	
        leSetEntryLayer(list(bot_name "drawing"))
        leSetAllLayerVisible(nil)
        leSetLayerVisible(list(bot_name "drawing") t)
        leSetLayerVisible(list(bot_name "pin") t)
        leSetLayerVisible(list(top_name "drawing") t)
        leSetLayerVisible(list(top_name "pin") t)
        leSetLayerVisible(list(via_name "drawing") t)
	enable_sch_layers()
	hiRedraw()
    )
)


procedure( toggle_metal( layer_id )
    let( (metal_name draw_layer dum_layer pin_layer exc_layer)
	sprintf(metal_name "met%d" layer_id)
	draw_layer = list(metal_name "drawing")
	pin_layer = list(metal_name "pin")
	leSetLayerVisible(draw_layer not(leIsLayerVisible(draw_layer)))
	leSetLayerVisible(pin_layer not(leIsLayerVisible(pin_layer)))
        hiRedraw()
    )
)


hiSetBindKeys( "Layout" list(
    list("Ctrl<Key>q" "leSetAllLayerVisible(t) hiRedraw()")
    list("<Key>`" "show_od_m1()")
    list("<Key>1" "show_adjacent_metals(1)")
    list("<Key>2" "show_adjacent_metals(2)")
    list("<Key>3" "show_adjacent_metals(3)")
    list("<Key>4" "show_adjacent_metals(4)")
    list("<Key>5" "show_adjacent_metals(5)")
    list("<Key>6" "show_adjacent_metals(6)")
    list("<Key>7" "show_adjacent_metals(7)")
    list("<Key>8" "show_adjacent_metals(8)")
    list("<Key>9" "show_adjacent_metals(9)")
    list("Ctrl<Key>`" "toggle_od()")
    list("Ctrl<Key>1" "toggle_metal(1)")
    list("Ctrl<Key>2" "toggle_metal(2)")
    list("Ctrl<Key>3" "toggle_metal(3)")
    list("Ctrl<Key>4" "toggle_metal(4)")
    list("Ctrl<Key>5" "toggle_metal(5)")
    list("Ctrl<Key>6" "toggle_metal(6)")
    list("Ctrl<Key>7" "toggle_metal(7)")
    list("Ctrl<Key>8" "toggle_metal(8)")
    list("Ctrl<Key>9" "toggle_metal(9)")
    list("Ctrl<Key>10" "toggle_metal(10)")
))
