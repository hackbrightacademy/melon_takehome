# Melon Reservation Scheduler

## Description

This project allows you to make and manage melon tasting reservations. 🍉

[Project Requirements](https://docs.google.com/document/d/1g5WMLwezVuGCNnZBafREobcDDst8PgxElGPHfk7EgRI/edit)

## Justification

I chose to use Flask because it is a lightweight web framework that is flexible and simple to implement. I used postgreSQL because it's a commonly used relational database and makes a good choice since every reservation has a consistent format. SQLAlchemy allowed me to incorporate these two technologies using Python. I used Jinja to programmatically generate HTML and AJAX to handle retrieving available reservations from the database so that the page does not need to reload after the user submits their query.

## Reflection

In addition to fulfilling the requirements, I also added delete functionality which also includes an AJAX request so when users delete reservations they will immediately be removed from the page. I also ensured that my web app is responsive to different screen sizes.

Given more time, I would incorporate a User table that would have a relationship with the Reservation table. With a User table, I could have a password field which would allow me to enable authentication. I would use the Python hashlib library with salt to encrypt the password.

I would also like to add unit tests that test that a particular time does not show up in the list of available times when it's already booked. I added error handling for if a user goes to the /reservations URL if the user is not in session, which could occur with other routes as well. However, since the user is unable to navigate to these routes without being in session (unless they manually enter the URL) I did not include error handling there.

## Installation

To run Melon Reservation Schedule on your local machine:

1. Clone this repository.

2. Navigate into the repository on your machine and create and activate a virtual environment.

   ```
   python3 -m venv env
   source env/bin/activate
   ```

3. Install the dependencies

   ```
   pip3 install -r requirements.txt
   ```

4. Create the database (this assumes you have Postgres installed and running). You can name the database
   anything but you need to refer to the correct name in the next step.

   ```
   createdb reservations
   ```

5. Export the 2 environment variables, APP_SECRET_KEY and DATABASE_URL, needed for the application.

   You can set APP_SECRET_KEY to any string.

   DATABASE_URL should refer to the location of the database you created in the previous step.

   If you prefer, you can put these lines in a file, secrets.sh and
   then source that file with `source secrets.sh`.

   ```
   export APP_SECRET_KEY='some_secret'
   export DATABASE_URL='postgres:///reservations'
   ```

6. Seed the database (optional)

   ```
   python3 seed.py
   ```

7. Run the application

   ```
   python3 server.py
   ```

You can now navigate to 'localhost:5000/' to access Melon Tasting Scheduler.

Note that when running the application in the future, only step 5 and 7 are needed unless
you have dropped your database or updated its schema.

## Deployment

The application is deployed using Heroku.

To deploy, run `git push heroku main` (you will need to set up Heroku access first).

The deployed application can be found at https://melon-takehome.herokuapp.com/.
