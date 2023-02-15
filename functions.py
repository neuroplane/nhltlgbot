import datetime as dt


def date_two_weeks(days):
    iso_past_date = dt.datetime.fromisoformat(str(dt.datetime.date(dt.datetime.now() - dt.timedelta(days)))).strftime('%Y-%m-%d')
    return iso_past_date
