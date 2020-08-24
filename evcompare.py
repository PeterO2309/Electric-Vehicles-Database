import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from myev import MyEV
from myuser import MyUser
import os
import logging

# Setting up the environment for Jinja to work in as we construct a
# jinja2.Environment object.
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Compare(webapp2.RequestHandler):
    def get(self):
        url = ''
        url_string = ''

        # pull the current user from the Request
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        evquery = MyEV.query()

        print(" helloworld ")

        #print(evquery)

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'list':evquery
        }

        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('evcompare.html')
        self.response.write(template.render(template_values))



    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        evquery = MyEV.query()

        url = ''
        url_string = ''

        # pull the current user from the Request
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'


        if  self.request.get('button') == 'COMPARE':
            checked = self.request.get_all('checked_name')

            if(len(checked) >= 2):
                checked_ev_list = []


                checked_ev_year_list = []
                checked_ev_batterysize_list = []
                checked_ev_wltp_list = []
                checked_ev_cost_list = []
                checked_ev_power_list = []

                checked_rating_list = []

                '''
                checked_ev_year_maxlist = []
                checked_ev_batterysize_maxlist = []
                checked_ev_wltp_maxlist = []
                checked_ev_cost_maxlist = []
                checked_ev_power_maxlist = []
                '''





                message = "Attributes of the Selected EVs"

                #max_year = max_batterysize = max_wltp = max_cost = max_power = 0
                #min_year = min_batterysize = min_wltp = min_cost = min_power = 2147483647 #Largest positive integer


                for n in checked:
                    checked_key = ndb.Key('MyEV', int(n))
                    checked_obj = checked_key.get()
                    checked_ev_list.append(checked_obj)

                    checked_ev_year_list.append(checked_obj.year)
                    checked_ev_batterysize_list.append(checked_obj.batterysize)
                    checked_ev_wltp_list.append(checked_obj.WLTPrange)
                    checked_ev_cost_list.append(checked_obj.cost)
                    checked_ev_power_list.append(checked_obj.power)

                    checked_rating_list.append(checked_obj.avg_rating)

                    '''
                    checked_ev_year_maxlist.append(checked_obj.year)
                    checked_ev_batterysize_maxlist.append(checked_obj.batterysize)
                    checked_ev_wltp_maxlist.append(checked_obj.WLTPrange)
                    checked_ev_cost_maxlist.append(checked_obj.cost)
                    checked_ev_power_maxlist.append(checked_obj.power)
                    '''



                    '''
                    if (checked_obj.year > max_year):
                        max_year = checked_obj.year
                    if (checked_obj.batterysize > max_batterysize):
                        max_batterysize = checked_obj.batterysize
                    if (checked_obj.WLTPrange > max_wltp):
                        max_wltp = checked_obj.WLTPrange
                    if (checked_obj.cost > max_cost):
                        max_cost = checked_obj.cost
                    if (checked_obj.power > max_power):
                        max_power = checked_obj.power


                    if (checked_obj.year < min_year):
                        min_year = checked_obj.year
                    if (checked_obj.batterysize  < min_batterysize ):
                        min_batterysize  = checked_obj.batterysize
                    if (checked_obj.WLTPrange < min_wltp):
                        min_wltp = checked_obj.WLTPrange
                    if (checked_obj.cost < min_cost):
                        min_cost = checked_obj.cost
                    if (checked_obj.power < min_power):
                        min_power = checked_obj.power
                        #logging.info('This returns the min cost')
                        #print(min_cost)

                    '''
                    '''
                    logging.info('This is a debug message')
                    print(checked_obj.name)
                    print(checked_obj.cost)
                    '''


                min_year = min(checked_ev_year_list)
                min_batterysize = min(checked_ev_batterysize_list)
                min_wltp = min(checked_ev_wltp_list)
                min_cost = min(checked_ev_cost_list)
                min_power = min(checked_ev_power_list)
                min_rating = min(checked_rating_list)


                max_year = max(checked_ev_year_list)
                max_batterysize = max(checked_ev_batterysize_list)
                max_wltp = max(checked_ev_wltp_list)
                max_cost = max(checked_ev_cost_list)
                max_power = max(checked_ev_power_list)
                max_rating = max(checked_rating_list)



                logging.info('This is a debug message for checked_ev_cost_minlist')
                print("Minyear =",min_year)
                print("Maxyear =",max_year)
                print("min_batterysize =",min_batterysize)
                print("max_batterysize =",max_batterysize)
                print("min_wltp =",min_wltp)
                print("max_wltp =",max_wltp)
                print("Mincost =",min_cost)
                print("Maxcost =",max_cost)
                print("min_power =",min_power)
                print("max_power =",max_power)
                print("max_rating =",max_rating)
                print("min_rating =",min_rating)




                template_values = {
                    'url' : url,
                    'url_string' : url_string,
                    'message' : message,
                    'checked_ev_list':checked_ev_list,
                    'list': evquery,
                    'max_year' : max_year,
                    'max_batterysize' : max_batterysize,
                    'max_wltp' : max_wltp,
                    'max_cost' : max_cost,
                    'max_power' : max_power,
                    'min_year' : min_year,
                    'min_batterysize' : min_batterysize,
                    'min_wltp' : min_wltp,
                    'min_cost' : min_cost,
                    'min_power' : min_power,
                    'max_rating' : max_rating,
                    'min_rating' : min_rating
                }

            else:
                checked_ev_list = ''
                message = "Select two or more EVs to compare."
                #self.redirect('/evcompare')

                template_values = {
                    'url' : url,
                    'url_string' : url_string,
                    'message' : message,
                    'checked_ev_list':checked_ev_list,
                    'list': evquery
                }

            # pull the template file and ask jinja to render
            # it with the given template values
            template = JINJA_ENVIRONMENT.get_template('evcompare.html')
            #template = JINJA_ENVIRONMENT.get_template('Details.html?button=Add_Review&name=myev.name&manufacturer=myev.manufacturer&year=myev.year')

            self.response.write(template.render(template_values))
