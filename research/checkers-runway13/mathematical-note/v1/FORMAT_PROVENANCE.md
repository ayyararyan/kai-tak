# V5 format fidelity

The actual published V5 files RFS.cls, rfs-workingpaper.sty, rfs.bst, crop.sty and crop.cfg are reused byte-for-byte, with original notices. Their hashes are bound in FORMAT_SOURCE_MANIFEST.json. Metadata is overridden in main.tex, not by a replacement template.

Preserved: RFS article architecture, Times12pt body, NewTX mathematics,14.4pt normal baseline,182.52×274.92mm page trim,373.2TeX-point text width, title/author/abstract/running headers, theorem/proof styling, continuous equation numbering, captions and author-year bibliography. The title page identifies an independent research note/version/date, without journal branding, affiliation, DOI or acceptance date.

The reference PDF was inspected with Poppler pdffonts before production: embedded Times-Roman/Bold/Italic and NewTXMI confirmed. Final PDF fonts/page rectangles are checked separately in qa/fonts.txt and qa/document_checks.json. Visible regular body font sizes are compared in qa/format-comparison.json. Every rendered page receives visual review recorded separately.

No proprietary installable fonts are bundled. The recorded clean build reuses the host licensed fonts/TeX; other hosts may have different glyph metrics or pagination. The editable sources remain portable through documented PATH/XELATEX/BIBTEX configuration.
