# Claims-only conversion scope

Per request, conversion is now scoped to **Claims** programs/macros only.

## Included SAS directories
- `Claims Programs/`
- `Global Macros/` (only macros used by Claims rate calculations)
- `Reconcile Macro/` (used by Claims Step 1)
- `Master Program/` (used only as dependency reference)

## Excluded for now
- Eligibility and other program trees not present in the provided source snapshot.

## Python conversion artifacts added
- `claims_python/precision.py`: global numeric precision/rounding policy (`Decimal`, precision default 28).
- `claims_python/master_claims.py`: claims-only runner and input source validation.
- `claims_python/claims_macros.py`: function equivalents for every discovered Claims-side SAS macro entry point.

## Precision policy
- Integer counters/keys: `int64`
- Monetary + estimator intermediates: `Decimal(prec=28)`
- Deterministic rounding: `ROUND_HALF_EVEN`
