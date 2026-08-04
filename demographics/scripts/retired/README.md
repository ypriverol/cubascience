# Retired chart scripts

These predate the four-scenario model and the estimand rename. Several of them
write the SAME figure filenames as the live scripts, so which version shipped
depended on invocation order — that is how retired values (8.59, 22.7, a 2.2 M
waterfall total, "Model D") ended up rendered into published PDFs while the
LaTeX captions on the same page said something different.

They are kept for traceability and are excluded from the retired-value gate,
which scans only live chart scripts. Do not run them.

Live producers of the manuscript figures:

| figures | script |
|---|---|
| f1, f2, f3, f4, f5, f7, f11 (EN) | `charts_publication.py` |
| the same, ES                     | `charts_manuscript_es.py` |
| f14 (both languages)             | `charts_attributable.py` |
| f15 (both languages)             | `charts_migration.py` |
