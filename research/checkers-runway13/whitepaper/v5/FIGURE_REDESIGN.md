# Figure redesign: Version 4 → Version 5

## Editorial decision

The figure system now follows the engineering investigation: **place → direction → forces → a complete landing → pavement consumed → historical reconstruction → wind → verification → the accident evidence**. The old count of sixteen figures is not a design constraint. The production plan specifies twelve main figures and two possible technical supplements; the final build manifest is the authoritative delivered inventory.

The design does not treat a new palette as a redesign. Five structural changes carry the visual argument:

- Actual archival photographs establish the airport, painted checkerboard and bay before any computed path appears.
- The 47° construction sits in an explicitly schematic geographic setting, with a runway symbol and source-map fragment. Its lines compare bearings; they do not reconstruct a route.
- The landing and runway figures give the airborne and ground phases a common physical setting, using the frozen numerical paths and distance definitions.
- The photogrammetry figure begins with corresponding features in real photographs, renders the actual accepted open mesh, and returns to a named map form. Missing geometry and limited control support are visible.
- Continuous-time verification receives an explanatory illustration; numerical cover bookkeeping is carried by the text and technical record.

## Complete V4-to-V5 mapping

| V4 figure | V5 destination | Editorial transformation |
|---|---|---|
| 01 Historical airport | 01_place | Dominant airport/city image with separate real Checkerboard and bay views; no panorama stitching or invented route. |
| 02 Approach geometry | 02_bearings | One geographic-relations composition with exact magnetic direction guides; generic procedure flowchart removed. |
| 03 Dated maps | 06_maps | A readable 1989 field, named external locators and three precisely matched 150 m-wide 1994 windows. |
| 04 Reconstruction | 07_stereo | Real image correspondences → accepted open three-dimensional surface → dated market identity, with control support alongside. |
| 05 Turn physics | 03_turn | Physical force balance and a turning arc carry the radius/time calculation; two interchangeable curve plots retired. |
| 06 Wind vectors | 08_wind | The same wind is decomposed in two changing flight directions; vectors are attached to physical orientation. |
| 07 Calm profiles | A1_profiles, with 04_landing | Full kinematics remain available, including the calm candidate's brief rise; the spatial scene carries the main narrative. |
| 08 Stopping | 05_runway | Disconnected bars become a continuous, common-scale runway allocation; stopping arithmetic remains exact. |
| 09 Complete calm | 04_landing | Empty coordinate cage replaced by a local runway scene; no historical city overlay or disguised height exaggeration. |
| 10 Certificate | 09_certificate | Adaptive-width diagnostic no longer stands in for the explanation; a stated analytic teaching example exposes the between-sample problem. |
| 11 Wind profiles | A1_profiles | All six wind quantities retained as aligned technical profiles, with explicit limits and phase division. |
| 12 Scenario comparison | 05_runway and A2_bounds | Physical distance allocation separated from mathematical optimality brackets; separate optimized scenarios remain distinct problems. |
| 13 Recorder | 10_recorder | Recorder-plot readings remain observation symbols with reading-sensitivity ranges; direct labels and restrained joining lines. |
| 14 Weather | 11_weather | Local sensor readings and annual station context retain separate clocks and evidence meanings. |
| 15 Rollout | 12_rollout | Narrative landmarks carry the speed/stopping comparison without implying equally spaced physical time. |
| 16 Evidence synthesis | Retired as a main-text figure | Generic evidence-status boxes removed. Their substantive observed/derived/assumed/certified/unidentified distinctions remain in scope, source and limitations text. |

The removal of V4 Figure 16 does not remove a scientific finding. It removes a repeated diagram of the report's own administrative structure.

## Historical figures: implemented design and source decisions

### 01_place

A36143 occupies the principal visual field because airport pavement, aircraft and surrounding streets are visible together. CN4581 shows the real painted checkerboard beside recreation grounds; CN4589 shows the runway's harbour end and Kowloon Bay. The smaller frames are independent source views, not a synthetic panorama. Labels point to visually inspected features, not surveyed coordinates.

Only display crops are applied. Full original bytes remain in `inputs/` and `inputs/historical/`. The October frames retain their 8 October 1993 date. A36143 retains the unresolved catalogue 2 November / apparent handwritten 3 November discrepancy. No metric scale or north-up orientation is inferred from these perspective scans.

### 02_bearings

A genuine 1989 survey-map fragment supplies the urban setting. A runway symbol and Checkerboard locator communicate broad place relations; **they are not spatially registered to that fragment**. The diagram explicitly calls itself schematic. The source acquisition anchors only support approximate relative geography.

The constructed rays share magnetic north: 088° for the IGS direction and 135° for the runway. Their exact difference is 47°. The dashed intersection is a geometric construction, not a historical turn point; no curved historical or synthetic aircraft path is inserted. A visual-segment annotation preserves the distinction between instrument guidance and visual alignment.

### 06_maps

The main map retains the complete 750 × 600 m V4 registered crop from the October 1989 edition of sheet 11-NE-11A. Fine leaders name Shing Tung House, the Regal Airport Hotel and Kowloon City Market. Copper rectangles identify the exact later-edition detail windows.

The July 1994 windows use **the same pixel rectangles in the same registered grid**, each 600 source pixels = 150 m wide. They have equal physical display dimensions. The main field includes a correctly derived 100 m scale bar and grid-north arrow. Raster spacing is 0.25 m; no cartographic accuracy bound is inferred. The images reveal mapped forms at their own edition dates, not unchanged 1993 building heights or identities.

### 07_stereo

Two real source-photo crops mark the retained manually interpreted tracks: R, municipal-market roof feature (track 26); S, rooftop service structure (track 1135); and G, paved-path junction (track 788). The geometry is not a newly fitted reconstruction.

The oblique visual loads **155,891 vertices and 225,371 triangles from the exact accepted PLY**. Triangle topology stays unchanged. There is no remeshing, gap filling, wall extrusion, capping, vertical exaggeration or negative-height clamping. An orthonormal camera basis gives equal metre scale in all directions, with the camera above the scene and positive screen-up response to height. Surface contrast combines original pixel luminance with mild normal-based illumination; this changes display tone, not any coordinate.

The support inset uses the exact polygon used in the settled reconstruction. The 3,780 / 171,307 count describes the full retained dense cloud, not the display subsample. The named roof features lie outside that hull; the figure says so and the script checks their stored flags. Conditional heights 10.77 m and 19.20 m are rounded displays of the existing sparse-report values relative to the fitted park/road plane. They are neither HKPD elevations nor measured building height above local ground.

## Reproduction and publication output

Shared art direction is implemented in `scripts/figure_style.py`; historical composition in `scripts/historical_figures.py`. Each master produces:

- `figures/NAME.pdf`: vector-first manuscript file, with raster only for source imagery/dense geometry.
- `figures/NAME.svg`: editable vector/text composition with embedded image material where needed.
- `figures/NAME.png`: 190 dpi screen rendering.
- `presentation/NAME.png`: 600 dpi presentation export from the same master.
- `qa/figure-records/NAME.json`: exact inputs, hashes, geometry/display decisions and output hash.

Run `python scripts/historical_figures.py --prototypes` for the three historical prototypes; run without that switch for the complete four-figure historical lane. The scientific figures use their separate documented producer. No source photograph, map or accepted scientific data file is rewritten by the figure scripts.

## Inspection and production gate

The historical figures were inspected as rendered 190 dpi outputs and compact PDF previews, not only by reading the code. The parent additionally inspected 01_place, 02_bearings and corrected 07_stereo and accepted the prototype gate before 06_maps was built. Repairs included removing awkward blank space and thick text outlines, rebuilding the initial isolated bearing fan, correcting the oblique camera's up-vector sign, strengthening mesh contrast and displaying the roof features' outside-hull status.

**Final integrated-suite/page inspection:** final PDF pages 13–28 pass this visual reviewer’s inspection. Changed pages 17–18 were freshly viewed in build `328f848d805df1e5bac5fd6aff6f28363112bea3acd9a5fcb71c33ec16842939`; the other 14 pages match previously individually inspected pages by exact RGB-pixel hashes. All reported paragraph interruptions, the orphan coefficient heading and the table-label wrap are verified fixed. No pending finding remains in this range. Receipt and hashes: `qa/visual-review-13-26.json`; parent/editorial coverage of the remaining pages belongs to the final visual-verification record.
