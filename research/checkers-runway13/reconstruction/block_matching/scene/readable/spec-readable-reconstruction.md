---
title: Readable reconstruction views
type: bugfix
created: 2026-10-13
status: done
route: one-shot
---

# Readable reconstruction views

## Intent

**Problem:** Aryan could see the previous previews but could not make out their content. The grey oblique surface lacked orientation and recognizable locators.

**Approach:** Add a labelled north-up historical map, a matched height-coloured recovered-surface plot, and a market-area close-up. Preserve original inputs, null historical heights, source epochs, conditional calibration and unknown gaps. These are presentation artifacts, not improved geometry or a completed reconstruction.

## Suggested Review Order

- [Reading page](index.html): start with landmarks and responsive interpretation.
- [Renderer](render.py): unchanged source data, matching map coordinates and no hole filling.
- [Verification receipt](verification.json): source hash and image hashes.
- [Full reconstruction limitations](../../REPORT.md): scientific status remains incomplete.

Independent review identified four presentation issues, all patched: hidden B annotation, omitted control-hull qualification, small raster captions on mobile, and obscured north/scale aids. All three generated figures visually inspected after repairs; hashes, image decoding and local links checked. Browser interaction remains unverified. No VCS, publication or original viewer changes.
