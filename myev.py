from google.appengine.ext import ndb
from evreview import Review


class MyEV(ndb.Model):
    # name of the EV
    name = ndb.StringProperty()
    manufacturer = ndb.StringProperty()
    year = ndb.IntegerProperty()
    batterysize = ndb.IntegerProperty()
    WLTPrange = ndb.FloatProperty()
    cost = ndb.IntegerProperty()
    power = ndb.IntegerProperty()
    reviews = ndb.StructuredProperty(Review, repeated = True)

    avg_rating = ndb.FloatProperty()
