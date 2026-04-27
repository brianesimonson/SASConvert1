# Running converted Claims programs

## Primary entry point
Run the converted program CLI:

```bash
python -m claims_python.run_claims \
  --program manual-change \
  --input-dir ./input_data \
  --output-dir ./output_data \
  --pyear 2026
```

## What this currently runs
Currently implemented end-to-end:
- `Claims Programs/Manual Change for Claims Data Cleaning.sas`

Converted macro flow executed:
1. `manual_raw_data_change_error_mr`
2. `manual_raw_data_change_error_dp`
3. `manual_raw_data_change_claim`
4. `manual_data_change`
5. `pop_totals_manual_change`
6. `pop_totals_manual_change_nodup`

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

## Notes
- The repository also contains structure-mirrored modules for all provided SAS files under `claims_python/converted_structure/`.
- Remaining complex estimator/rate macros are still being ported and will be wired into this CLI as completed.
