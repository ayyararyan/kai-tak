# Kai Tak: dated sheets, photographs and structure evidence

**Verified 13 October 2026. Source acquisition and documentary classification are usable; the complete historical city and 3D scene remain incomplete.**

We can now inspect actual dated imagery, locate relevant map/photo coverage for current features, and query documentary completion evidence by date. This does not yet recover the identity, footprint and height of every structure that ever occupied Hong Kong.

## Look at the evidence

- [Side-by-side historical maps and photograph](source_comparison.png): the same neighbourhood in October 1989, November 1993, July 1994 and April 1997. Different scales/orientations; **not pixel registered**.
- [Historical aerial gallery](aerial/gallery.html): 48 acquired full frames, including the Checkerboard, Kowloon City and runway.
- [Coverage map](coverage.png): downloaded sheet locations and documentary support attached to **current** polygons, not a picture of the 1993 city. Landmark dots are approximate acquisition anchors, not surveyed flight geometry.
- [52 visual observations concerning 17 named structures/sites](historical_visual_observations.csv): actual bounded source interpretations, kept separate from documentary inference.

## Sources acquired and matched

| Evidence | Verified scope |
|---|---:|
| Historical survey-sheet index entries, whole HK | 72,691 |
| Index entries intersecting Kowloon/Kai Tak acquisition rectangle | 18,440 |
| Actual map editions downloaded and ZIP/CRC checked | 227, covering 93 sheet locations |
| Historical aerial frame index entries, local rectangle, 1985–1998 | 14,927 across 316 capture dates |
| 1993 frame index entries | 1,277 |
| Actual full DAP-L0 aerial JPEGs / additional previews | 48 / 47 |
| Downloaded-sheet / 1993-frame index-polygon overlap pairs | 16,968 |
| Current local features with source-coverage candidate rows | 69,915 |

The local rectangle is WGS84 `[114.10,22.27,114.25,22.40]`; the map acquisition core is `[114.16,22.30,114.22,22.35]`. This is not an approved aircraft corridor. All 69,915 local representative points have preceding and following **1993 index coverage**; that does not mean all corresponding images have been downloaded or inspected. 69,851 have bracketing survey-sheet months; 22,006 have at least one acquired bracketing sheet.

Maps include older index families from 1922 onward. Actual selected maps concentrate on the 1980s/1990s. The photograph selection samples dates and anchor locations; it is not complete photographic coverage of all Hong Kong.

Each overlap row retains identifiers, dates, intersection area and fractions. A map edition identifies publication/revision timing, not the survey date of every object. November 1993 editions are kept date-sensitive for a 4 November query; they are not silently treated as preceding it.

## Documentary classification: example 4 November 1993

| Current-feature evidence category | Whole HK | Local rectangle |
|---|---:|---:|
| Classified, including unresolved cases | 342,195 | 69,915 |
| At least one linked documentary event | 71,382 | 29,082 |
| Some completion/permit evidence on or before query | 35,540 | 21,746 |
| Completion date agrees with linked permit date before query | 34,387 | 21,066 |
| Only later completion/permit evidence | 19,588 | 6,562 |
| Administrative/undated evidence only | 16,254 | 774 |
| No linked documentary chronology | 270,813 | 40,833 |

These count source polygons/CSUIDs, **not independent historical buildings**. Agreement between two linked tables is corroboration, not independent witnessing. Completion by a date does not establish continued presence, identical geometry, occupancy or roof height on that date. Later completion does not establish an empty site before it. Those distinctions remain in every row.

All four relevant official tables were acquired completely: 168,042 works rows, 53,349 building/structure relationships, 54,505 structure/permit links and 24,469 permits. All 221,383 resolved evidence paths are retained with provenance; duplicated paths are not additional buildings. The source graph adds **zero vanished identities outside the current polygon universe**, so it cannot alone supply a demolished-building census.

### A material source inconsistency

52,552 works-table records labelled OP Date all fall in 2019 or 2020; 52,202 CSUIDs disagree with their explicitly linked permit-table dates. Eight fresh individual source requests confirmed the discrepancy exists in raw official responses. We preserve both values and the conflict, without guessing its cause. For the Regal Oriental Hotel tower, completion and linked permit agree on **18 May 1982**, while the works OP field says **18 May 2019**. See [source audit and interpretation](structures/README.md).

## What direct image inspection establishes

- **Kowloon Walled City:** dense contiguous roof mass in frame A23632, **13 November 1990**; largely cleared site with residual structures in CN4581, **8 October 1993**, and A36143, **2 November 1993**; park layout depicted on the **April 1997** sheet. Individual remnants and exact change dates are unresolved. The blank interior on the **October 1989 map** is a cartographic omission, not evidence of absence.
- **Chung Tung House site:** the October 1989 sheet marks construction in progress; July 1994 and April 1997 sheets show the named structure. This brackets a mapped transition, not an exact completion date.
- **Fourteen other named forms** were read across the three sheets, including Shing Tung, Mau Tung, On Tung and Hong Tung Houses, Ng Wah College, Lee Kau Yan Memorial School, Regal Airport Hotel, the terminal and multi-storey car park. Historical/current identity joins have not been certified.
- **Checkerboard Hill:** the painted landmark is visible in CN4581. No height or slope measurement was derived from that image.

The central ledger contains **52 observations, 17 named objects/sites, three map editions and three distinct full aerial frames directly inspected by the parent**. It is not 52 independent buildings or full inspection of every downloaded image. Additional acquisition-lane notes are in [aerial observations](aerial/VISUAL_OBSERVATIONS.md).

## Machine-readable handoff

- [HANDOFF.json](HANDOFF.json): paths, coordinate/datum conventions, epochs, uncertainty and permitted interpretation.
- [Local classification CSV](structures/aoi_features_1993-11-04.csv) and [whole-HK classification CSV](structures/current_features_1993-11-04.csv).
- [Source candidates per local feature](structure_source_matches_1993-11-04.csv) and [sheet/photo coverage pairs](sheet_photo_pairs_1993.csv).
- [Chronology database](structures/chronology.sqlite), [event provenance](structures/events.csv), [visual observations](historical_visual_observations.csv).
- [Verification](validation.json), [requirement audit](MODEL_REQUIREMENTS_TRACEABILITY.md), [integrity manifest](manifest.json).

The documentary query accepts another date without reacquiring the tables:

```sh
research/checkers-runway13/geospatial/.venv/bin/python research/checkers-runway13/reconstruction/chronology/structures/chronology.py --date 1985-01-01
```

Outputs are date-specific. The supplied map/photo matching outputs remain explicitly the 1993 example. A date query does not manufacture an observation on that date.

## What remains before a faithful 3D scene

Photographs require ground control, registration/orthorectification and per-structure interpretation; frame-index corners are not suitable control points. Historic outlines, altered footprints, vanished buildings and roof heights still need extraction and identity resolution. Existing DTM photography is **2014–2015**, not 1993; hills may be broadly persistent, but quarrying, cut slopes, reclamation and shoreline changes cannot be assumed away. Present-day roof elevations are not historical heights.

The acquired DAP-L0 images are 3000px compressed 300 dpi photographs, not calibrated high-resolution photogrammetric scans. Precise height recovery needs stronger inputs and validation. No historical height intervals, complete obstacle surface, aviation-datum reconciliation or clearance-certified geometry have been produced. Unknown terrain/obstacle validity is not empty space. The uncertainty mask marks the entire local rectangle as **not certified**, not as obstructed or obstacle-free.

**Next unresolved work:** accurately register selected dated sheets/photos; digitize and resolve historical structures block by block, beginning with the visual-turn neighbourhood; obtain defensible heights and changed shoreline/earthwork geometry. These requirements are not waived. No ongoing background collector or automatic reconstruction is claimed.

## Verification and attribution

39 documentary regression tests and seven source-matching tests passed on the parent rerun. The complete repaired classifier changed zero existing classification fields for 342,195 objects at both tested dates. Source counts, IDs, file hashes, image decode checks, archive CRCs, positive overlap fractions and final cross-artifact counts were checked. Two independent code reviewers were used; one additionally performed an artifact acceptance pass. Review is evidence, not proof of complete historical coverage. Final report figures were visually inspected; the gallery's browser interactions were not tested in this parent turn.

Sources: **Lands Department and Buildings Department, Government of the Hong Kong Special Administrative Region**, [CSDI Building service](https://portal.csdi.gov.hk/server/rest/services/common/landsd_rcd_1637211194312_35158/FeatureServer), [HKMS aerial search](https://www.hkmapservice.gov.hk/OneStopSystem/map-search?product=OSSCatA), and official historical survey-sheet services recorded in `sheets/raw/*.source.json`. Original source terms and attribution requirements apply. Everything is local: no publication, purchase, peer-machine sync or aircraft-model/configuration change.
