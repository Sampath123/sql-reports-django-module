# sql-reports-django-module

#Write SQL, it will generate the report.


#Quick start
#-----------

#1. Paste sqlreports app in your project src folder and 
# Add "sqlreports" to your INSTALLED_APPS setting as::


#        INSTALLED_APPS = (
#                ...
#                'sqlreports',
#            )


#2. Include the polls URLconf in your project urls.py like this::

#    url(r'^sql-reports/', include('sqlreports.urls')),


#3. Run `python manage.py migrate` to create the reports models.

#                OR 

# If you have installed south then do bin/django schemamigration sqlreports --initial to generate migration file for sqlreports model

# and then run migration as bin/django migrate sqlreports

# Create report by writing your sql queries with optional parameters using admin screen sql reports and hit the url " sql-reports " to get all the queries and get report on clicking on particular report.


