from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
@app.route("/")
def home():
    return redirect("/login")

DATA_FILE = "lockers_data.json"

# ---------- JSON Functions ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# ---------- Login ----------
# ---------- Login ----------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        print(username, password)   # temporary check

        if username == "admin" and password == "1234":
            return redirect("/dashboard")
        else:
            return "Invalid Username or Password"

    return render_template("login.html")
username = request.form["username"]
password = request.form["password"]

print("USERNAME:", username)
print("PASSWORD:", password)

# ---------- Dashboard ----------
@app.route("/dashboard")
def dashboard():

    lockers = load_data()

    total = len(lockers)

    available = sum(1 for locker in lockers if locker["status"] == "Available")

    occupied = total - available

    return render_template(
        "dashboard.html",
        total=total,
        available=available,
        occupied=occupied
    )


# ---------- Add Locker ----------
@app.route("/add_locker", methods=["GET", "POST"])
def add_locker():

    if request.method == "POST":

        locker_id = request.form["locker_id"]
        size = request.form["size"]

        lockers = load_data()

        lockers.append({
            "locker_id": locker_id,
            "size": size,
            "status": "Available",
            "customer": "",
            "allotted_on": ""
        })

        save_data(lockers)

        return redirect("/view_lockers")

    return render_template("add_locker.html")


# ---------- View Lockers ----------
@app.route("/view_lockers")
def view_lockers():
    lockers = load_data()
    return render_template("view_lockers.html", lockers=lockers)

@app.route("/allocate", methods=["GET", "POST"])
def allocate():

    if request.method == "POST":

        locker_id = request.form["locker_id"]
        customer = request.form["customer"]
        date = request.form["date"]

        lockers = load_data()

        for locker in lockers:

            if locker["locker_id"] == locker_id:

                locker["customer"] = customer
                locker["status"] = "Occupied"
                locker["allotted_on"] = date

        save_data(lockers)

        return redirect("/view_lockers")

    return render_template("allocate.html")

@app.route("/search", methods=["GET","POST"])
def search():

    result = None

    if request.method == "POST":

        customer = request.form["customer"]

        lockers = load_data()

        for locker in lockers:

            if locker["customer"].lower() == customer.lower():
                result = locker
                break

    return render_template("search.html", result=result)

@app.route("/release", methods=["GET", "POST"])
def release():

    if request.method == "POST":

        locker_id = request.form["locker_id"]

        lockers = load_data()

        for locker in lockers:

            if locker["locker_id"] == locker_id:

                locker["status"] = "Available"
                locker["customer"] = ""
                locker["allotted_on"] = ""

        save_data(lockers)

        return redirect("/view_lockers")

    return render_template("release.html")

@app.route("/logout")
def logout():
    return redirect("/login")

@app.route("/reports")
def reports():

    lockers = load_data()

    total = len(lockers)

    available = sum(
        1 for locker in lockers
        if locker["status"] == "Available"
    )

    occupied = total - available

    return render_template(
        "reports.html",
        lockers=lockers,
        total=total,
        available=available,
        occupied=occupied
    )

# ---------- Run ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
