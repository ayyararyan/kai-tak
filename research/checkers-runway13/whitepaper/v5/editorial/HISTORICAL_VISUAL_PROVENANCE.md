# Historical visual sources and display transformations

Prepared 13 October 2026 for V5. This supplements, and does not replace, the root rights/provenance record.

## Ownership and source terms

Original aerial photographs and survey-map linework: **Lands Department, Government of the Hong Kong Special Administrative Region; CSDI Portal; DATA.GOV.HK**. Government/relevant source organisations retain intellectual-property ownership. Open-data reuse is subject to the source terms with attribution; source material is supplied as-is, without endorsement. This task does not select a new blanket licence or generalize open DAP-L0 permission to paid aerial products. Existing inspected terms: [DATA.GOV.HK](https://data.gov.hk/en/terms-and-conditions), [CSDI](https://portal.csdi.gov.hk/csdi-webpage/doc/TNC).

V5's added material comes from the previously acquired archive, not newly synthesized historical images. `inputs/historical/SOURCE_MANIFEST.json` records source-relative repository paths, source-manifest checksums, source metadata, snapshot hashes and byte sizes. Original V4 input files were preserved.

## Photo dates and scope

| Frame | V5 use | Source date / qualification |
|---|---|---|
| A36143 | Airport/city view; right stereo crop | Catalogue 2 November 1993; handwritten frame label appears 3 November. Discrepancy remains unresolved. |
| A36142 | Left stereo crop | Catalogue 2 November 1993; inspected border agrees. Pair reconstruction remains the accepted existing analysis, not a newly asserted resolution of A36143's date. |
| CN4581 / product CN04581 | Actual Checkerboard Hill | 8 October 1993, visible painted checkerboard in the original colour frame. Does not establish every structure's state on 4 November. |
| CN4589 / product CN04589 | Runway harbour end and bay | 8 October 1993; original colour frame, not an accident image. |

An older archive observation note says A36143's dates agree. The visible border and V4 record disagree with that sentence; it was not imported. Full unmodified source images remain available. Figure crops, leader endpoints and display geometry are in the figure-generation script and per-figure records.

## Survey maps

October 1989 and July 1994 versions of 11-NE-11A are the original V4 registered crops. Both cover E 837500–838250, N 821000–821600 in Hong Kong 1980 Grid (EPSG:2326), at 0.25 m raster spacing. The metadata preserve original archive hashes and pixel-edge/centre transforms. Geographic north and magnetic north are not silently equated: the map figure labels **Grid N**; the direction-construction figure labels **Magnetic N** and explicitly uses a nonregistered schematic.

Named locators use retained `historical_faces.geojson` seed metadata. A seed identifies a map form, not a surveyed roof point, proven identity across dates or physical obstacle volume.

## Accepted reconstruction

The PLY copied into V5 matches the V4 HANDOFF hash `49866bd77fd74a04f8ba18e8a734d05ee169b2ddd9bc7d74b6039800869a8323`. It is an open triangle surface with 155,891 vertices, 225,371 faces and reported 86,061 boundary edges. No earlier invalidated predecessor is used.

- Horizontal coordinates: diagnostic EPSG:2326 alignment through the retained map-control transformation.
- Vertical coordinates: fitted local park/road plane, not HKPD or height above each building's own ground.
- Appearance: source-derived grayscale values with disclosed linear print contrast and mild directional lighting.
- Topology: unchanged, with transparent/white gaps; no invented architectural solids.
- Camera: orthonormal equal-metre projection, above-scene view, no vertical exaggeration.
- Named tracks: 26 and 1135 correspond to the retained manually interpreted market roof features; both are outside the map-control hull. Their height values are conditional source-report estimates, not independently validated roof heights.
- Plan support: exact `support_polygon_hk1980` from retained `registration.json`, the same polygon used by the accepted stereo scripts; 3,780 of 171,307 dense points lie inside.

## Geographic context is not geographic registration

`02_bearings` uses approximate catalogue acquisition anchors only to establish broad relative place. Its map fragment, hill locator, runway symbol and common bearing origin do not form a surveyed chart. All exact displayed angles come from the retained CAD factual bearing transcription. No accident-report page raster, chart scan or photograph is redistributed by the new illustrations.

## Changes that were explicitly avoided

No generative historical scenery, photo stitching, estimated roof completion, hidden gap fill, modern-building substitution, registered synthetic flight overlay, airport-width inference from photographs, source-date reconciliation by appearance, or new aircraft/obstacle clearance result was introduced.
