# thisWay: a PaaS Heroku implemented Django Application

thisWay is an application running on a Heroku PaaS Django structured application. The app takes 
advantage of Google Cloud APIs, particularily google-cloud-vision, google-cloud-storage, and the
google-cloud-directions functionality of googlemaps. It also uses google smtp notification service.

It uses these four API functions in unison to allow for users to enter their email, an image of a
landmark, and a start point defined through text. The API implementation then takes all of this submitted
data and returns first a computer vision produced recognition of what and where the landmark is, followed
by driving directions to the landmark from the provided start point. It also sends an email to the user's
prvided email address containing these directions, and saves all previously searched landmarks by other 
users for reference upon return to the site. 

Functions implementing landmark recognition computer vision are detailed in /thisWayDesign/findLandmark.py
Functions implementing direction definition are detailed in /thisWayDesign/getDirections.py
Functionality of smtp interaction is detailed in /thisWayDesign/views.py within the processSubmission method
Functionality of landmark storage memory is implemented in /thisWayDesign/views.py within the updateStorage method

## Running Locally

In order to run this application locally, simply clone the repository to any given machine with Heroku
and Python3 installed. Upon navigating to the source directory, a user simply must ensure all of the 
requirements detailed in requirements.txt are synchronized within their local Python installation, should 
any errors occur in the installation of the requirements packages. Python errors will tell you if 
anything is missing. 

Heroku config environment variables are provided here and synced to your local machine for ease of 
installation and running. To run in a Linux environment with Heroku installed, run:

```sh
$ git clone https://github.com/UOITEngineering3/assignment2winter2019-bradyjibanez
$ cd assignment2winter2019-bradyjibanez
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py collectstatic
$ heroku local
```

Your app will run on [localhost:5000](http://localhost:5000/).

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#prepare-the-app) - PaaS provider for Django installations, configuration, and distribution
* [gunicorn](https://gunicorn.org/) - Synchoronous Python wsgi/Http request responding server. Configured and maintained by Heroku and the Procfile (or for windows, Procfile.windows) detailed here. 

## Authors

* **Brady Ibanez** - *Cloud based implementation and app functionality* 
