import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from myev import MyEV
from myuser import MyUser
from addingev import AddingEV
from evcompare import Compare
from details import Details
import os
import logging



# Setting up the environment for Jinja to work in as we construct a
# jinja2.Environment object.
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # URL that will contain a login or logout link
        # and also a string to represent this
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        datastore_message = "Below you will see the items that are currently stored in the datastore."
        myev = None


        # pull the current user from the Request
        user = users.get_current_user()

        # determine if we have a user logged in or not
        if user:
            url = users.create_logout_url(self.request.uri)
            login_status = "You are logged in."
            url_string = 'logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            #myuser = MyUser(email_address = user.email())
            myuser = myuser_key.get()


            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id = user.user_id())
                myuser.email_address = user.email()
                myuser.put()
        else:
            url = users.create_login_url(self.request.uri)
            login_status = "To Add a new EV, You need to login. Click on login above"
            url_string = 'login'

            # by providing self.request.uri we are asking to be redirected back
            # to the URL of the page represented by this class.

        query = MyEV.query()
        r = list(query.fetch())
        #print('data')
        #print(r)


        template_values = {
            'url' : url,
            'url_string' : url_string,
            'login_status' : login_status,
            'datastore_message' : datastore_message,
            'user' : user,
            'welcome' : welcome,
            'myev' : myev,
            'list':r
        }


            # pull the template file and ask jinja to render
            # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        #action = self.request.get('button')
        sq = MyEV.query().fetch(keys_only=True)
        datastore_message = 'Search results'

        #query = MyEV.query()
        #r = list(query.fetch())

        if self.request.get('button'):
            if self.request.get('q_name'):
                searchquery = MyEV.query(MyEV.name == self.request.get('q_name')).fetch(keys_only=True)
                sq=set(sq).intersection(searchquery)

            if self.request.get('q_manufacturer'):
                searchquery = MyEV.query(MyEV.manufacturer == self.request.get('q_manufacturer')).fetch(keys_only=True)
                sq=set(sq).intersection(searchquery)

            # If a user enters a query either lower or upper limit, the results
            # displays all that is saved in the datastore. It displays a result
            # specific to the query if both upper and lower limits are entered.
            if self.request.get('q_year') and self.request.get('q_yearMAX'):
                searchquery = MyEV.query(MyEV.year >= int(self.request.get('q_year'))).fetch(keys_only=True)
                sq=set(sq).intersection(searchquery)
                searchquery = MyEV.query(MyEV.year <= int(self.request.get('q_yearMAX'))).fetch(keys_only=True)
                sq=set(sq).intersection(searchquery)

            if self.request.get('q_batterysize') and self.request.get('q_batterysizeMAX'):
                searchquery = MyEV.query(MyEV.batterysize >= int(self.request.get('q_batterysize'))).fetch(keys_only=True)
                sq=set(sq).intersection(searchquery)
                searchquery = MyEV.query(MyEV.batterysize <= int(self.request.get('q_batterysizeMAX'))).fetch(keys_only=True)
                sq=set(sq).intersection(searchquery)

            if self.request.get('q_wltp') and self.request.get('q_wltpMAX'):
                searchquery = MyEV.query(MyEV.WLTPrange >= float(self.request.get('q_wltp'))).fetch(keys_only=True)
                sq=set(sq).intersection(searchquery)
                searchquery = MyEV.query(MyEV.WLTPrange <= float(self.request.get('q_wltpMAX'))).fetch(keys_only=True)
                sq=set(sq).intersection(searchquery)

            if self.request.get('q_cost') and self.request.get('q_costMAX'):
                searchquery = MyEV.query(MyEV.cost >= int(self.request.get('q_cost'))).fetch(keys_only=True)
                sq=set(sq).intersection(searchquery)
                searchquery = MyEV.query(MyEV.cost <= int(self.request.get('q_costMAX'))).fetch(keys_only=True)
                sq=set(sq).intersection(searchquery)

            if self.request.get('q_power') and self.request.get('q_powerMAX'):
                searchquery = MyEV.query(MyEV.power >= int(self.request.get('q_power'))).fetch(keys_only=True)
                sq=set(sq).intersection(searchquery)
                searchquery = MyEV.query(MyEV.power <= int(self.request.get('q_powerMAX'))).fetch(keys_only=True)
                sq=set(sq).intersection(searchquery)

            ro=ndb.get_multi(sq)

            '''
            if self.request.get('q_batterysize'):
                searchquery = sq.filter(MyEV.batterysize ==int(self.request.get('q_batterysize')))
            if self.request.get('q_wltp'):
                searchquery = sq.filter(MyEV.WLTPrange== float(self.request.get('q_wltp')))
            if self.request.get('q_cost'):
                searchquery = sq.filter(MyEV.cost == int(self.request.get('q_cost')))
            if self.request.get('q_power'):
                searchquery = sq.filter(MyEV.power == int(self.request.get('q_power')))

            # If nothing selected on the form, display the full EV list
            if searchquery==None:
                ro=list(sq.fetch())
                ev_string = 'No attribute selected. The EV names in the datastore are displayed below.'


            # Display a list of EVs that satisfy the query as a list of hyperlinks.
            else:
                ro=list(searchquery.fetch())
                ev_string = 'The EV names in the datastore based on the query are displayed below.'
            '''
            # URL that will contain a login or logout link
            # and also a string to represent this
            url = ''
            url_string = ''
            welcome = 'Welcome back'
            myev = None


            # pull the current user from the Request
            user = users.get_current_user()

            # determine if we have a user logged in or not
            if user:
                url = users.create_logout_url(self.request.uri)
                url_string = 'logout'

                myuser_key = ndb.Key('MyUser', user.user_id())
                #myuser = MyUser(email_address = user.email())
                myuser = myuser_key.get()


                if myuser == None:
                    welcome = 'Welcome to the application'
                    myuser = MyUser(id = user.user_id())
                    myuser.email_address = user.email()
                    myuser.put()
            else:
                url = users.create_login_url(self.request.uri)
                url_string = 'login'

            template_values = {
                'url' : url,
                'url_string' : url_string,
                'user' : user,
                'datastore_message': datastore_message,
                'welcome' : welcome,
                'myev' : myev,
                'list':ro
            }

            # pull the template file and ask jinja to render
            # it with the given template values
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/addingev', AddingEV),('/Details',Details),
    ('/evcompare', Compare )
], debug=True)
