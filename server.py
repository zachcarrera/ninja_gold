import random
import datetime
from flask import Flask, render_template, redirect, session, request

app = Flask(__name__)

app.secret_key = "password"


# index route
@app.route("/")
def index():
    # if money is not in session create it and set it to zero
    if "money" not in session:
        session["money"] = 0
    
    # if activity is not in session then create it and make it an empty list
    if "activity" not in session:
        session["activity"] = []

    return render_template("index.html")


# process_money route
@app.route("/process_money", methods=["POST"])
def process_money():

    # if the reset button is pressed then clear the session
    if "reset" in request.form:
        session.clear()
        return redirect("/")

    # current date and time formatted into a string
    time_stamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S %p")

    # logic to get the random number based off of the "building" key value pair
    if request.form["building"] == "farm":
        new_num = random.randint(10, 20)
    elif request.form["building"] == "cave":
        new_num = random.randint(5, 10)
    elif request.form["building"] == "house":
        new_num = random.randint(2, 5)
    elif request.form["building"] == "casino":
        new_num = random.randint(-50, 50)

    session["money"] += new_num


    # format the activity_string based on if new_num is positive or negative
    if new_num >= 0:
        activity_string = f"<p class='text-success mb-0'>Earned {new_num} golds from the {request.form['building']}! ({time_stamp})</p>"
    else:
        activity_string = f"<p class='text-danger mb-0'>Entered a casino and lost {new_num * -1} golds... Ouch... ({time_stamp})</p>"

    # add activity_string to the end of session["activity"]
    session["activity"].append(activity_string)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)