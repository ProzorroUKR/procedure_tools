import datetime

from procedure_tools.utils.date import fix_datetime, get_now, parse_date

DEFAULT_ACCELERATION = 1


def from_date(
    date: str | datetime.datetime,
    acceleration: float = DEFAULT_ACCELERATION,
    client_timedelta: datetime.timedelta | None = None,
    **kwargs: float,
) -> datetime.datetime:
    if isinstance(date, str):
        date = parse_date(date)
    if client_timedelta:
        date = fix_datetime(date, client_timedelta)
    td = datetime.timedelta(**kwargs)
    if acceleration:
        td /= acceleration
    return date + td


def from_now(
    acceleration: float = DEFAULT_ACCELERATION,
    client_timedelta: datetime.timedelta | None = None,
    **kwargs: float,
) -> datetime.datetime:
    return from_date(
        get_now(),
        acceleration=acceleration,
        client_timedelta=client_timedelta,
        **kwargs,
    )


def from_date_iso(
    date: str | datetime.datetime,
    acceleration: float = DEFAULT_ACCELERATION,
    client_timedelta: datetime.timedelta | None = None,
    **kwargs: float,
) -> str:
    return from_date(
        date,
        acceleration=acceleration,
        client_timedelta=client_timedelta,
        **kwargs,
    ).isoformat()


def from_now_iso(
    acceleration: float = DEFAULT_ACCELERATION,
    client_timedelta: datetime.timedelta | None = None,
    **kwargs: float,
) -> str:
    return from_now(
        acceleration=acceleration,
        client_timedelta=client_timedelta,
        **kwargs,
    ).isoformat()
