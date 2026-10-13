# Figure rights, provenance and unresolved source details

Original text, code and scientific plots: Aryan Ayyar, 2026. No new blanket open-source licence is chosen by this task. Repository NOTICE remains in force.

## Historical imagery and derived geometry (figures 1, 3, 4)

Source: **Lands Department, Government of the Hong Kong Special Administrative Region; CSDI Portal; DATA.GOV.HK**. Government and relevant organisations retain intellectual-property ownership. Data are provided as-is, without warranty or endorsement. The analytical annotations and interpretations are the author's, not the Government's.

- [DATA.GOV.HK terms](https://data.gov.hk/en/terms-and-conditions), version 1.2, 26 May 2025: inspected 13 October 2026, permits reproduction/distribution with source attribution and ownership acknowledgement under the stated conditions.
- [CSDI terms](https://portal.csdi.gov.hk/csdi-webpage/doc/TNC): inspected 13 October 2026, section 3 permits reproduction/distribution with Government/CSDI source attribution and ownership acknowledgement under the stated conditions.
- [Digital Aerial Photo open-data collection](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-development-hkms-digital-aerial-photo): A36143 DAP-L0 (300 dpi open-data acquisition), catalogue date 2 November 1993. The handwritten scan label appears to say 3 November; unresolved, disclosed in manuscript. This permission is not generalized to paid aerial products.
- [Old Survey Sheets](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-old-survey-sheets): sheet 11-NE-11A October 1989 and July 1994. Retained registered crops are derived from official open-data archives. Original archive hashes and affine/CRS metadata accompany them. 0.25 m raster spacing is not positional accuracy.
- Stereo plot inputs are unchanged every-fifth-row numerical derivatives of the settled A36142/A36143 reconstruction. Their numerical/hash lineage remains in the V2 manifest. Heights relative to a fitted local plane are not HKPD or building height above local ground.

`inputs/provenance.json`, `evidence_manifest.json`, `SOURCE_MANIFEST.json` and `qa/figure_provenance.json` supply the exact file/hash chain. Source files are not cosmetically altered; figures add labels and plot transformations in reproducible code. The aerial is displayed in grayscale, in its original scan orientation, with no invented flight-track overlay.

## Accident-report evidence (figures 2, 13–15)

Hong Kong Civil Aviation Department, Aircraft Accident Report 1/95, August 1995. Bibliography links the retained archived original. Figures use independently plotted factual directions, manual numerical readings and factual weather/rollout tables; they do not reproduce report scan pages, photographs or graph rasters. Manual reading sensitivity is not sensor error or a probability interval. The complete report and overlays remain excluded because redistribution permission is not established.

## Weather (figure 14)

NOAA, National Centers for Environmental Information, Integrated Surface Database, station 450070–99999, 1993. Derived subset uses the declared flags and selection, not an invented sample. NOAA/NCEI attribution retained. Original archive and decoder remain in the wider repository/release; the compact manuscript input retains the plot-relevant fields.

## All other figures

Original mathematical diagrams and plots derived from frozen project numerical inputs or explicitly stated elementary equations. No third-party photograph, stock graphic, generative artwork or supposed expert endorsement is introduced. `qa/figure_provenance.json` maps every figure to its inputs and meaning. The cover repeats figure 9, not a seventeenth scientific figure.
