from decimal import ROUND_HALF_EVEN, getcontext


def configure_decimal(precision: int = 28) -> None:
    """Set global Decimal behavior for reproducible SAS-like calculations."""
    ctx = getcontext()
    ctx.prec = precision
    ctx.rounding = ROUND_HALF_EVEN
