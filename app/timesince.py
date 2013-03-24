# encoding: utf-8

from datetime import datetime

def timesince(dt, default=u"juuri nyt"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.

    From http://flask.pocoo.org/snippets/33/, translated to finnish.
    """

    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, u"vuosi", u"vuotta"),
        (diff.days / 30, u"kuukausi", u"kuukautta"),
        (diff.days / 7, u"viikko", u"viikkoa"),
        (diff.days, u"päivä", u"päivää"),
        (diff.seconds / 3600, u"tunti", u"tuntia"),
        (diff.seconds / 60, u"minuutti", u"minuuttia"),
        (diff.seconds, u"sekunti", u"sekuntia"),
    )

    for period, singular, plural in periods:
        if period:
            return u"%d %s sitten" % (period, singular if period == 1 else plural)

    return default
