from datetime import datetime, timedelta

from dateutil import parser, tz

DATE_HEADER_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"

TZ = tz.gettz("Europe/Kiev")


def get_now() -> datetime:
    return datetime.now(TZ)


def get_utcnow() -> datetime:
    return datetime.now(tz.tzutc())


def fix_datetime(dt: datetime, delta: timedelta) -> datetime:
    return dt + delta


def parse_date_header(header: str) -> datetime:
    return datetime.strptime(
        header,
        DATE_HEADER_FORMAT,
    ).replace(tzinfo=tz.tzutc())


def parse_date(datetime_str: str) -> datetime:
    return parser.parse(datetime_str)


def client_timedelta_string(client_timedelta: timedelta) -> str:
    total_seconds = client_timedelta.total_seconds()
    if total_seconds > 1:
        return f"{int(total_seconds)} seconds"
    return f"{int(total_seconds * 1000)} milliseconds"
