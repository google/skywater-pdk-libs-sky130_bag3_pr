# skywater130

Skywater130 primitives for [BAG](https://github.com/ucb-art/bag).

These primitives are updated for V2.0.0 of the PDK. It currently support layout generation and LVS using Virtuoso pcells, which was previously not supported. Simulations using BAG is also supported.

## Technology features and hints
- Layout resolution is in 5nm.
- Min channel length is 150nm, so min channel units is 30.
- This tech has standard, lvt, and hvt devices. pch hvt and lvt have min channel length of 350um,
  so they cannot be used for logic-style MOS with nch.
- Min nch width is 420nm (84 units). Min pch width is 550nm (110 units).
- Widths are quantized in irregular intervals. See the pcells for examples.
  - Nch has 840nm. Pch has 1120nm.
- This tech has two flavors of "precisions" poly resistors: hrpoly (300 ohm / sq) and uhrpoly (2K ohm / sq). Min width is 0.33 um, min resistor length is 0.5 um. The contacts have a 2.16um length, required by DRC, so the min overall length is 4.82um.
  - These are not currently supported in BAG.
- This tech has 5 metal layers and an "M0" (LI) layer.
- This tech has pcell MOM caps. M1-M2 caps provide ~0.4 fF / um^2. M1-M4 caps provide ~0.74 fF /
  um^2.
- This tech has pcell MIM caps, between M3-M4 and M4-M5. Both provide ~2.2 fF / um^2.

## Licensing

This library is licensed under the Apache-2.0 license.  See [here](LICENSE) for full text of the 
Apache license.
