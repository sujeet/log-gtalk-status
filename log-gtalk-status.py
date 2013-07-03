import webapp2
from GtalkStatus import GtalkStatus

from google.appengine.api import xmpp, mail
from google.appengine.ext import db


class SubscriptionHandler (webapp2.RequestHandler):
    """Add the user to bot's roster.'"""
    def post(self):
        sender = self.request.get('from').split('/')[0]
        roster.add_contact(sender)

class StatusLogger (webapp2.RequestHandler):
    """
    Check if the status is different from last five unique statuses.
    If unique, store the status in the database (of last five unique statuses)
    Also, send a mail containing the status.
    """
    def post(self):
        user_email = self.request.get('from').split('/')[0]
        status = self.request.get('status')
        query = GtalkStatus.all()
        query.filter ('email_id = ', user_email)
        query.filter ('status_message = ', status)

        duplicate = query.get()

        if duplicate == None :
            # This status message isn't in database, must be new
            # Let's send it and save it.

            # Don't store more than 100 status messages per user
            # Delete the oldest one in case the limit is exceeded.
            query = GtalkStatus.all()
            query.filter ('email_id = ', user_email)
            query.order ('time_stamp')
            if query.count () >= 100:
                oldest = query.get ()
                db.delete (oldest)

            # Save this status in database
            gtalk_status = GtalkStatus (
                email_id = user_email,
                status_message = status
                )
            gtalk_status.put()

            # Send the status as mail
            mail.send_mail (
                sender="Status Logger <no-reply@log-gtalk-status.appspotmail.com>",
                to = user_email,
                subject = "Re: Gtalk status update",
                body = status
                )

application = webapp2.WSGIApplication([

        ('/_ah/xmpp/presence/subscribe', SubscriptionHandler),
        ('/_ah/xmpp/presence/available/', StatusLogger),

        ], debug=True)
