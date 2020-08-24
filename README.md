# Electric-Vehicles-Database

This is a PaaS application which will be a database or Electric Vehicles. Developed using Python Webapp2 framework 
and deployed using the Google App Engine/Google Datastore.

In this application: 

-users are able to login and logout.
-users are able to add and update cars that are in the database. They are able to perform comparisons of multiple cars 
 in the database.
 

*TASK COMPLETED*

- Write the shell of an application that has a working login/logout
service.
- Add in a datastore object to represent an EV it should have attributes
to represent. name, manufacturer, year, battery size (Kwh), WLTP range
(Km), cost, power (Kw).

- Add in a seperate page for adding an ev to the database. EV with same manufacturer, name, and year
cannot be added and accessible to only a logged in user 

- Add in a form for querying the EV database. it should be able to
filter on all attributes.
- Attributes that are string based should have a single input string
- Attributes that are numerical should specify a range with upper
and lower limit (limits included in search) and accessible regardless of login status.
- If nothing selected on the form then show full EV list

- When a hyperlink has been clicked go to a seperate page showing the
information of that EV.
- Add the ability to edit that EV.
– Add the ability to delete that EV.
– Editing and deleting should only be available to a logged in user.

- On a seperate page add in a comparison feature.
– This should take 2 or more EVs and display all of their attributes
side by size. if 0 or 1 EVs is selected, no comparison is
triggered.
– For all attributes show green for highest value and red for lowest.
do the opposite for cost.
– Names should still be a hyperlink that leads to the information
of that EV.

- Add in the ability for a logged in user to submit a review of an EV
including a text field (limited to 1,000 characters) and a rating out
of 10.
- The reviews should be visible to all users even if logged out.

- On the information page for an EV this should show the average
score of all reviews.
- On the information page for an EV the reviews should be shown in
reverse chronological order.
- On the comparison page for EVs the average score should be added
in and highlighted green if highest and red if lowest.
