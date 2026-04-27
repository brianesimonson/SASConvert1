# SAS → Python conversion bootstrap

## What was done
- Extracted `PERM Programs - Claims.zip` into the repository so each SAS source file is now available as plain text.
- Confirmed the orchestration entry point is `Master Program/Master Program Forecasting Rates.sas` and that it `%include`s dependent programs/macros.

## Recommended precision strategy for reproducibility
To match SAS numeric behavior while preserving high-fidelity estimates/CI calculations:

1. **Identifiers / integer counters**
   - Use `int64` (`numpy.int64` / pandas nullable `Int64`) for counts, claim lines, and denominators that are integer-valued.
   - Avoid float storage for IDs and categorical keys.

2. **Monetary amounts and weighted sums**
   - Use `decimal.Decimal` with **at least 28 digits** precision (`getcontext().prec = 28`) for staged calculations where cancellation can occur.
   - Persist final outputs as `float64` only at export boundaries if required by downstream tools.

3. **Rates, standard errors, confidence intervals**
   - Compute intermediate variance terms in `Decimal` (or `numpy.float128` when available) and only convert to `float64` for final reporting.
   - For confidence intervals, keep a reproducible quantile policy (e.g., normal `z=1.96` unless SAS program applies a different method).

4. **Rounding policy**
   - Use explicit rounding modes (`ROUND_HALF_EVEN`) and fixed decimal places per metric to match SAS report formatting.
   - Never rely on implicit binary float rounding for published metrics.

## Suggested conversion order
1. Master driver orchestration in Python.
2. Reconcile macros.
3. Claims cleaning macros.
4. Estimator macros (`combined ratio estimator`, `double_ratio_estimator`).
5. QC/export scripts.

## Notes
- The current repository snapshot only contains Claims + Global/Reconcile/Master pieces from the provided zip. The master program references additional folders that are not present in this zip (Eligibility, Rolling, Overall, Interim, Key Tables). Those folders are needed for full end-to-end conversion.
