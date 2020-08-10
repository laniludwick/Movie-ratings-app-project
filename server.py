"""Server for movie ratings app."""

from flask import Flask, request, flash, session, redirect, render_template
from model import connect_to_db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!

@app.route("/")
def show_homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route("/movies")
def show_all_movies():
    """Show list of movies."""

    movies = crud.get_movies()

    return render_template('all_movies.html', movies = movies)


@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show movie details."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)


@app.route("/users")
def show_all_users():
    """Show list of users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)


@app.route("/users", methods = ["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    #If email already exists in the system, block user from re-registering.
    if crud.get_user_by_email(email): 
        flash("Sorry, that user already exists. Please try again.")

    #Otherwise, allow user to register for an account with that email address.
    else:
        user = crud.create_user(email, password)
        flash("Successfully registered a new account!")

    return redirect("/")


@app.route("/login")
def process_login():

    email = request.args.get("email")
    password = request.args.get("password")

    #Check if possword matches with the stored user's password:
    
    print("email:", email)
    print("password:",password)

    try: 
        user = crud.get_user_by_email(email)

        print("user:", user)
        
        print("user.password:", user.password)
    

        if password == user.password:
            session["logged_in_user"] = user.user_id
            print("session:", session)
            flash("Login successful!")

        else: 
            flash("Sorry, failed login attempt. Please try again.")

    except:
        flash("Sorry, no user found. Please try again.")


    return redirect("/")


# try: 
#         user = customers.get_by_email(email)
        
#     # - if a Customer with that email was found, check the provided password
#     #   against the stored one
#     # - if they match, store the user's email in the session, flash a success
#     #   message and redirect the user to the "/melons" route
#         if password ==user.password:
#             session["logged_in_customer_email"] = email 
#             flash("Login successful!")
#             return redirect("/melons")

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show user details."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html",user=user)




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

