from google.appengine.ext import db

class GtalkStatus (db.Model):
    email_id = db.StringProperty (required = True)
    status_message = db.StringProperty (required = True)
    time_stamp = db.DateTimeProperty (auto_now_add = True)
