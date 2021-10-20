import datetime


def myconverter(o):
    if isinstance(o, datetime.date):
        return o.isoformat()
