from google.appengine.ext import ndb

class Review(ndb.Model):
    textarea = ndb.StringProperty()
    rating = ndb.IntegerProperty()
