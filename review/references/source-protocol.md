# Source acquisition and verification protocol

## Bounded acquisition protocol

0. **Local tree first.** Search the workspace before any external query: sibling
   review folders (a parallel review of the same authors or their earlier paper
   may already hold the package — an upstream construction package is itself a
   source), the operator's inbox and download folders, any local reference library,
   and archived storage. A source
   logged `BLOCKED` while a copy sits elsewhere in the tree is a self-inflicted
   gap. *(Worked case: an upstream package logged BLOCKED on
   the repository's 403 while it sat unzipped in a sibling review folder,
   fetched hours earlier.)*
1. Replication deposit and supplement.
2. Exact-title web search with author, year, issuing body, series, volume, and
   page/table identifiers.
3. Variant-title and predecessor/successor issuing-body searches.
4. Relevant digitized collections and institutional repositories.
5. Web archives for dead cited URLs.
6. Union catalogues and national-library catalogues for physical holdings.
7. Requester/operator access, interlibrary delivery, or authorized paid access.
   Unattended, log tier 7 as the request the operator must make, record the
   source `BLOCKED — operator access`, and continue; the rows resting on it stay
   `INTERIM` until the operator answers.

For each applicable tier, log the query or catalogue route, collection/filter,
date, and result. One failed search is not an acquisition pass. Complete the
applicable tiers before recording the source `BLOCKED` in `source-coverage.csv` —
claim rows resting on it then carry `unverified-here` (rule 7: a limit on the
review, not a finding); do not claim that a
source is globally unobtainable and do not let repeated speculative searching
become a completion condition. Record why skipped tiers are inapplicable.

Every acquired source the review quotes is dumped with `pdftotext` into
`review/extracts/`; the quote checks read only those dumps.

**Keep every other record of the paper's own data.** A file found during any
search that may hold the paper's observations or results in another form —
on an author's or co-author's website, OSF, Dataverse, a lab page, or in a later
pooled, meta-analysis or replication file — is saved under `lit/data/`, with
its URL, fetch date and hash beside it, and listed in the acquisition record.
This applies even when it falls outside the brief that found it. Never discard
such a file unread, and never delete one. It is a second record of the same
observations: the data audit matches it to the deposit row by row and diffs
every matched cell (code-and-data, data audit). *(Worked case: an acquisition
worker found a spreadsheet on the author's site, almost the same size as the
deposited data, and deleted it unread as outside its brief. It was the
author's own later compilation of the same participants plus two outside
replications.)*

## Source identity record

For every acquired item, record:

- full title;
- author or issuing body;
- edition, volume, series, issue, and vintage;
- publisher or archive;
- date;
- relevant printed pages, table captions, or native record identifiers;
- evidence that this is the exact stated source;
- file hash or persistent identifier;
- access location and date;
- PDF-page-to-printed-page mapping where applicable.

Do not infer identity from the filename.

## Observation-level comparison fields

Each comparison row should include:

- variable and observation key;
- selection stratum: random, leverage, or claim-critical;
- file value and units;
- source value and units;
- file date and source reference date;
- source page/table/record;
- visual adjudication status;
- discrepancy class;
- proposed explanation;
- final local verdict.

## Checksum-constrained transcription

When a printed table has column, section, or grand totals:

1. Render the page at sufficient resolution to read digits.
2. Transcribe relevant raw cells from the image.
3. Preserve printed totals verbatim in separate marked rows or fields.
4. Recompute sums and require exact reconciliation where the source arithmetic
   is internally consistent.
5. If one digit is ambiguous, use the checksum as evidence. If several digits
   are ambiguous, the checksum can be underdetermined; use an independent
   reprint or image source.
6. Leave validation assertions in the consuming script.

Never replace a printed total with a computed value. If source arithmetic
itself fails, record that as a source property after ruling out transcription
error.

## Quotations and page citations

When the audit quotes a construction claim:

1. Match the citation to the identified document.
2. Locate each quotation segment using normalized text search.
3. Confirm wording against the page image.
4. Cite the printed page, not merely the PDF index.
5. Record any ellipsis or editorial insertion.

Text extraction is a locator. The page image or native record is the final
adjudication surface.

## Processing-scale request

When full verification is unusually large, provide:

- number of pages, tables, records, and variables;
- pilot sample and pilot accuracy;
- proposed OCR, vision, transcription, and validation method;
- expected compute time, manual time, and paid cost;
- smallest defensible random-plus-leverage sample;
- what additional coverage would change the available verdict.
