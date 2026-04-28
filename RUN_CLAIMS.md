# Running converted Claims programs

## If you want the **SAS Master Program equivalent**
Run this command:

```bash
python -m claims_python.master_claims \
  --repo-root . \
  --input-dir ./input_data \
  --output-dir ./output_data \
  --pyear 2026 \
  --precision 28
```

This is the top-level Python entrypoint equivalent to running the Claims portion of:
- `Master Program/Master Program Forecasting Rates.sas`

It will:
1. validate required Claims SAS sources exist,
2. run currently-native converted flow (`Manual Change for Claims Data Cleaning`),
3. capture transpiled calls for Step 1/Step 2,
4. write `master_claims_run_summary.json` under `--output-dir`.

## Program-specific entrypoint (manual-change only)
You can also run only the manual-change program directly:

```bash
python -m claims_python.run_claims \
  --program manual-change \
  --input-dir ./input_data \
  --output-dir ./output_data \
  --pyear 2026
```

## Expected input CSV files in `--input-dir`
- `MR.csv`
- `DP.csv`
- `full_data.csv`
- `poptotals_temp.csv`

## Output files in `--output-dir`
- `MR.cleaned.csv`
- `DP.cleaned.csv`
- `full_data.cleaned.csv`
- `poptotals_temp.cleaned.csv`
- `master_claims_run_summary.json` (when running `claims_python.master_claims`)

## Notes
- The repository contains structure-mirrored modules for all provided SAS files under `claims_python/converted_structure/`.
- Remaining complex estimator/rate macros are transpiled and traceable, and are being replaced with native Python execution incrementally.
