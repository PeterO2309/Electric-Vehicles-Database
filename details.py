
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from myev import MyEV
from myuser import MyUser
from addingev import AddingEV
from evcompare import Compare
from evreview import Review
import os
import logging

# Setting up the environment for Jinja to work in as we construct a
# jinja2.Environment object.
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Details(webapp2.RequestHandler):
    def get(self):

        # pull the current user from the Request
        user = users.get_current_user()

        # determine if we have a user logged in or not
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
        '''
        id =  self.request.get('d_id')
        myev_key = ndb.Key('MyEV', (id))
        myev = myev_key.get()
        '''

        name =self.request.get('name')
        manufacturer =self.request.get('manufacturer')
        year=int(self.request.get('year'))

        query = MyEV.query(ndb.AND(MyEV.name == name, MyEV.manufacturer == manufacturer, MyEV.year == year))
        r = (query.fetch())



        #query = MyEV.query()
        #r = list(query.fetch())

        logging.info("This is a debug message")
        print(r[0].reviews)
        reverse_reviews= list(reversed(r[0].reviews))
        for i in reverse_reviews:
            print(i.rating)
        print(r[0].year)

        logging.info("This is the end of the debug message")

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'list': r[0],
            'reviews': r[0].reviews,
            'reverse_reviews': reverse_reviews
        }


            # pull the template file and ask jinja to render
            # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('Details.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # pull the current user from the Request
        user = users.get_current_user()
        logging.info(self.request.get('button'))


        # determine if we have a user logged in or not
        if user and self.request.get('button') == 'Update_EV':
            id =  self.request.get('d_id')
            myev_key = ndb.Key('MyEV', int(id))
            myev = myev_key.get()

            new_name =  self.request.get('name')
            new_manufacturer = self.request.get('manufacturer')
            new_year = int(self.request.get('year'))


            if ((new_name == myev.name) and (new_manufacturer == myev.manufacturer) and (new_year == myev.year)):

                myev.name =  self.request.get('name')
                myev.manufacturer = self.request.get('manufacturer')
                myev.year = int(self.request.get('year'))
                myev.batterysize = int(self.request.get('batterysize'))
                myev.WLTPrange = float(self.request.get('wltp'))
                myev.cost = int(self.request.get('cost'))
                myev.power = int(self.request.get('power'))

            else:
                # Query that checks if ev with same manufacturer, name, and year
                # already exists in the datastore.
                query = MyEV.query(ndb.AND(MyEV.manufacturer == new_manufacturer, MyEV.name== new_name,  MyEV.year == new_year ))
                r = list(query.fetch())
                print("Testing Testing")
                print(query)
                if len(r) is not 0:
                    url_string = 'Name, manufacturer, and year cannot be the same'
                    #self.response.write('Name, manufacturer, and year cannot be the same')
                else:
                    myev.name =  self.request.get('name')
                    myev.manufacturer = self.request.get('manufacturer')
                    myev.year = int(self.request.get('year'))
                    myev.batterysize = int(self.request.get('batterysize'))
                    myev.WLTPrange = float(self.request.get('wltp'))
                    myev.cost = int(self.request.get('cost'))
                    myev.power = int(self.request.get('power'))

            myev.put()


            self.redirect('/')


        elif user and self.request.get('button') == 'Delete_EV':
            id =  self.request.get('d_id')
            myev_key = ndb.Key('MyEV', int(id))
            myev = myev_key.get()

            myev.key.delete()
            self.redirect('/')


        elif user and self.request.get('button') == 'Add_Review':
            id =  self.request.get('d_id')
            myev_key = ndb.Key('MyEV', int(id))
            myev = myev_key.get()

            rating_list = [] # Array list for storing the EV ratings
            average_rating = 0 # Assign value for the initial average rating
            rating_sum = 0 # Sums all the ratings in the list
            count = 0 # Counts the number of ratings in the list

            rating = int(self.request.get('rating'))
            textarea = self.request.get('textarea')

            new_review = Review(rating=rating, textarea = textarea)
            myev.reviews.append(new_review)
            print(new_review.textarea)

            for n in myev.reviews:
                rating_list.append(n.rating)

            rating_sum = sum(rating_list)
            count = len(rating_list)
            average_rating = float(rating_sum) / float(count)
            myev.avg_rating = float(format(average_rating, '.2f')) # formats the calculated average to 2 decimal places

            logging.info("This is a debug message")
            print(rating_list)
            print("average =", average_rating)
            print("average =", myev.avg_rating)
            print("count =", count)
            print("sum =", rating_sum)


            NAME = myev.name
            MAN = myev.manufacturer
            YEAR = myev.year

            print("Name =", NAME)
            print("Year =", YEAR)
            print("Manufacturer =", MAN)



            logging.info("end of debug message")

            myev.put()

            self.redirect("/")

            #self.redirect("/Details?name=NAME&manufacturer=MAN&year=YEAR")
            #self.redirect("/Details?name=Hyundai&manufacturer=igwe&year=12")


        elif user and self.request.get('button') == 'Cancel':
            self.redirect('/')

        else:
            self.redirect('/')
