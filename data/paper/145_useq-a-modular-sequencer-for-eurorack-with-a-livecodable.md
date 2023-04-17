---
slug: useq-a-modular-sequencer-for-eurorack-with-a-livecodable
title: 'uSEQ: A Modular Sequencer for Eurorack with a Livecodable Microcontroller'
type: paper
status: proof
submission_type: Paper-Long
contributors:
- person: $kyriakoudis-dimitris
- person: $kiefer-chris
---

# $ABSTRACT

*uSEQ* is a new livecodable sequencer module for the Eurorack modular synthesiser ecosystem. It draws inspiration from both the practices of live coding and hardware modular synthesis, aiming to examine and combine their respective ergodynamic strengths and weaknesses into a new, hybrid practice. It embeds *uLisp*, a tiny interpreter for the general-purpose language with a small-enough footprint to run even on inexpensive microcontrollers. The interpreter's REPL has been modified for the purposes of live coding, and its reader has been "hacked" to the limited resources of the sub-£5 microcontroller at the heart of the module. On top of the Lisp general-purpose language, a minimal DSL layer has been designed to take full advantage of the linguistic flexibility of the underlying language. Simultaneously, the semantics of this DSL tries to stay close to one of the central philosophies of modular synthesis: everything is a signal, and sequences are no exception. Its open-source firmware and design files (PCB and 3D-printable faceplate), with an approximate total cost of £20 in parts, *uSEQ* is highly DIY-friendly can be built as a weekend project. It provides multiple input and output interfaces to the rest of the Eurorack ecosystem, and can be controlled from a mobile phone, tablet, or any (micro)computer with a USB port. The prototyping of this module is a practical exploration into the ways in which the ergonomic and ergodynamic tensions between the practices of livecoding and modular synthesis can be successfully addressed when bridging the two worlds, following a practice-led, research-through-design approach.
