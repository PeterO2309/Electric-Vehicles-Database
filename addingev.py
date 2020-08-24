import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

from myev import MyEV
from myuser import MyUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
 )

class AddingEV(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # URL that will contain a login or logout link
        # and also a string to represent this
        url = ''
        url_string = ''
        login_status = ''
        welcome = ''
        #myev = None


        # pull the current user from the Request
        user = users.get_current_user()

        # determine if we have a user logged in or not
        if user:
            login_status = "You are logged in."
            myuser_key = ndb.Key('MyUser', user.user_id())
            #myuser = MyUser(email_address = user.email())
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            myuser = myuser_key.get()


            if myuser == None:
                #welcome = 'Welcome to the application'
                myuser = MyUser(id = user.user_id())
                myuser.email_address = user.email()
                myuser.put()
        else:
            login_status = "To visit this page, You need to login."
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
            self.redirect('/')
            return
            #url = users.create_login_url(self.request.uri)
            #url_string = 'login'

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'login_status' : login_status,
            'user' : user,
            'welcome' : welcome
        }

        template = JINJA_ENVIRONMENT.get_template('addingev.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # pull the current user from the Request
        user = users.get_current_user()
        action = self.request.get('button')

        # Querying for the currently logged in user as we need the user id to
        # form the key to pull their data

        if user and action == 'ADD':

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            #myev_key = ndb.Key('MyEV', user.user_id())
            #myev = myev_key.get()

            '''
            newName = self.request.get('ev_name')
            newManufacturer = self.request.get('ev_manufacturer')
            newYear = int(self.request.get('ev_year'))
            newBatterysize = int(self.request.get('ev_batterysize'))
            newWLTP = float(self.request.get('ev_wltp'))
            newCost = int(self.request.get('ev_cost'))
            newPower = int(self.request.get('ev_power'))
            '''

            newEV = MyEV(
                         name = self.request.get('ev_name') ,
                         manufacturer = self.request.get('ev_manufacturer'),
                         year = int(self.request.get('ev_year')),
                         batterysize = int(self.request.get('ev_batterysize')),
                         WLTPrange = float(self.request.get('ev_wltp')),
                         cost = int(self.request.get('ev_cost')),
                         power = int(self.request.get('ev_power'))
                         )
            #newEV.put()
            #self.redirect('/')

            # Query that checks if ev with same manufacturer, name, and year
            # already exists in the datastore.
            query = MyEV.query(ndb.AND(MyEV.manufacturer == newEV.manufacturer, MyEV.name== newEV.name,  MyEV.year == newEV.year ))
            r = list(query.fetch())
            print("Testing Testing")
            print(query)
            if len(r) is not 0:
                url_string = 'Name, manufacturer, and year cannot be the same'
                #self.response.write('Name, manufacturer, and year cannot be the same')
            else:
                url_string  ="New EV added successfully"
                newEV.put()
            self.redirect('/')

        elif user and action == 'Cancel':
            self.redirect('/')


'''
        template_values = {
            'url_string' : url_string,
            'user' : user,
            'newEV' : MyEV
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))
'''
