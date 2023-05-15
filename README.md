# BAG (Berkeley Analog Generator) Primitives Library for [SKY130](https://github.com/google/skywater-pdk)

This repository contains the required primitives to use the BAG3 framework with
the SkyWater proprietary S8 130nm PDK. You can get access to this PDK through
signing an NDA and legal agreement with
[SkyWater Technologies](https://www.skywatertechnology.com/).

This repository also contains a **work in progress** to make these primitives
and the BAG3 framework compatible with
[the Google skywater-pdk, a fully open source, manufacturable PDK for SkyWater's 130nm (SKY130) process node](https://github.com/google/skywater-pdk).

When combined with appropriate generator code, the primitives enables the
creation of analog integrated circuits that are manufacturable at
[SkyWater Technologies](https://www.skywatertechnology.com/) commercially or
through programs like
[Google's no-cost MPW shuttle program for open source designs, done in collaboration with efabless](https://efabless.com/open_shuttle_program).

## What is BAG?

[BAG AMS Generator (BAG)](https://bag3-readthedocs.readthedocs.io/en/latest/index.html) is the 3rd generation
of the Berkeley Analog Generator framework (see also
[BAG v2 framework](https://github.com/ucb-art/bag)).

These primitives are updated for V2.0.0 of the PDK. It currently support layout generation and LVS using Virtuoso pcells, which was previously not supported. Simulations using BAG is also supported. To use the full workspace associated with these primitives, please use the [BAG3 Skywater 130nm workspace](https://github.com/ucb-art/bag3_skywater130_workspace).

This workspace and tech plugin are primarily maintained by Ayan Biswas, Felicia
Guo, Sean Huang, and Bob Zhou.

## Technology features and hints

- Layout resolution is in 5nm.
- Min channel length is 150nm, so min channel units is 30.
- This tech has standard, lvt, and hvt devices. pch hvt and lvt have min
  channel length of 350um, so they cannot be used for logic-style MOS with nch.
- Min nch width is 420nm (84 units). Min pch width is 550nm (110 units).
- Widths are quantized in irregular intervals. See the pcells for examples.
  - Nch has 840nm. Pch has 1120nm.
- This tech has 5 metal layers and an "M0" (LI) layer.
- This tech has pcell MOM caps. M1-M2 caps provide ~0.4 fF / um^2. M1-M4 caps
  provide ~0.74 fF / um^2.
- This tech has pcell MIM caps, between M3-M4 and M4-M5. Both provide ~2.2 fF / um^2.

SD pitch: 0.430 um ~ 86 units. BAG quantizes vertical metal pitches to match
the SD pitch ~ li, met2, met4

Metal min width and space (um):
- li : 0.170, 0.170
- met1: 0.140, 0.140
- met2: 0.140, 0.140
- met3: 0.300, 0.300
- met4: 0.300, 0.300
- met5: 1.600, 1.600

Track manager hints:
- m4 needs to be at least w=5 to connect to m5

### Resistors

- This tech has two flavors of "precisions" poly resistors: hrpoly (300 ohm /
  sq) and uhrpoly (2K ohm / sq). Min width is 0.33 um / 66 units, min resistor
  length is 0.5 um / 100 units. The contacts have a 2.16um length, required by
  DRC, so the min overall length is 4.82um.

- `res_type: standard` ~ hrpoly

Width selection

- For nice compatibility with the routing grid, make the unit cell width
  quantized to the sd pitch ~ 430 nm / 86 units. (not a hard requirement)
- LR edges account for up to an additional 780nm / 156 unit
- Some good values: 102, 360, 532

Length selection
- To minimize unused area, quantize unit height to sd pitch ~ 86 for working
  with the routing grid. (not a hard requirement)
    - Otherwise, unit height will round up to the next pitch of 86
- TB edges, including taps, account for up to 5.530 um / 1106 units
- Some good values: 270, 614

## Abstract Generation

Abstract generation in this technology does not work out of the box. More
details in [this README.](abstract_setup/README.md)

## Extraction

- This tech uses Calibre xRC for extraction. See $PDK_HOME/PEX/xRC and the
  manual for details.
- The xRC SVRF is set up to produce SPF files, to match other PEX tools. It can
  produce Spectre-format PEX netlists, but this has not been tested rigorously.
- xRC automatically capitalizes cell names, so top level cell names need to be
  full capitalized.

## License

To enable wide compatibility with the existing BAG ecosystem, this repository
is dual-licensed. It is available to you under your choice of the
[the Apache 2.0 license](LICENSE) or a [3 clause BSD style](LICENSE.alternative).

SPDX-License-Identifier: BSD-3-Clause OR Apache 2.0
