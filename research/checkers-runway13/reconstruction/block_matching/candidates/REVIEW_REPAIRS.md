# Candidate-screen repair report

## Accepted findings and changes

| Finding | Repair | Evidence |
|---|---|---|
| B1: palette indices could be interpreted as brightness | Fail closed on palette/RGB/non-uint8 or nodata/masked input. Current 94 sources successfully pass the grayscale guard. | Reordered/binary palette, nodata and genuine-grayscale fixtures; parent's separate 227-source audit is `../reviews/palette_audit.json`. |
| B7: coverage clipping could manufacture closed-region proof | Every selected region touching coverage or raster boundary forces an explicit truncated-region review status; it cannot be strong proof. | Open-plane/clipped-coverage fixture and genuinely enclosed control; full-run strong-proof check. |
| B8: geographic bbox was not actual sheet core | Use the actual source index polygon transformed to EPSG:2326, including exact intersection filtering. No bbox substitution or extra fitted alignment. | Four-edge inside/outside fixture; source-index hash; independent all-template query reconciliation. |
| B9: pixel-centre contours shrink narrow objects | Polygonize raster cell edges, retain ink holes and narrow/diagonal components; no simplification or dropped complex contours. | Rectangle area/bounds, one-cell-wide and holed/diagonal fixtures; every region's grid and round-trip area checked against pixel area. |
| Additional archive-binding finding | Compare actual source archive SHA256 against acquisition receipt before opening ZIP or analyzing pixels. | Tampered archive rejected before ZIP decoding; all 94 editions rerun with this guard. |

The original package, scripts, reports and exports are preserved under
`invalidated/pre_B1_B7_B8_B9/`, marked **invalidated**. No original source archive or
parent specification/ledger was modified. `invalidated_frozen_archive_manifest.json`
binds the preserved files. All 508 non-log entries match the old manifest; its parent
validation stdout log had been hashed while empty and subsequently filled. Current
manifests exclude log streams to avoid that self-output hashing problem.

## Full rerun and changes

All **94 editions / 93 sheet locations** were rerun with the final hash-guarded extractor.

| Screen class | Revised source-template rows |
|---|---:|
| Strong, still unverified | 10,955 |
| Ambiguous content | 7,055 |
| Explicitly truncated selected region | 234 |
| Low-support screen rejection | 2,936 |
| Template clipped at sheet edge | 2,621 |
| Total | 23,801 |

Compared with the preserved 23,835-row run:

- **34 rows** disappear from this sheet query because they lie outside the actual index
  polygon; all had previously been edge-clipped. Their source records remain preserved.
- **237 shared rows** change status; **23,564** retain their status.
- **234** now explicitly expose a truncated selected map region: 155 formerly ambiguous,
  78 formerly low-support and one formerly strong. This is a review-status change, not
  evidence that any structure existed or was absent.
- **Three** shared templates become edge-clipped under the actual polygon, including
  one formerly strong. Thus two former strong-screen candidates lose that category.
- **10 shared rows** change numerical best-region IoU. No new template IDs are introduced.

The corrected cell-edge exporter retains **61,893 unclassified map regions**, of which
**49,045** have no modern IoU≥0.25 correspondence. The old exporter retained 37,771:
the increase includes narrow and complex components previously lost during centre-contour
conversion. It is **not** an increase in verified historical buildings or a demolished
building census. No export-topology repair was needed after this corrected run.

`changed_classifications.csv` records every changed/removed row; the aggregate transition
matrix is `review_repair_comparison.json`. Individual old/new region IDs are not stable
identities and must not be used as historical building identifiers across extraction versions.

## Verification and remaining limits

The 10 focused regression tests pass and are bound to the final extractor hash in
`regression_results.json`. Full artifact/area/source/rank/date-null and classification
acceptance is recorded in `validation.json`; integrity is recorded in `manifest.json`.

**Historical geometry, identity and height acceptance remain zero in this candidate lane.**
These repairs improve a reproducible screen and its geometry accounting, not the completeness
or physical accuracy of the historical reconstruction. Broad visual review, actual identity
resolution and historical height evidence remain required in the parent reconstruction.
