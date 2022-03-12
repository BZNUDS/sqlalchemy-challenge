# 1. Import Flask
from flask import Flask


# 2. Create an app
app = Flask(__name__)


# 3. Define static routes
@app.route("/")
def index():
    return (
        f"Welcome to my SQLAlchemy Climate App Homepage. Avaialble routes:<br/>"
        f"   /api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )


@app.route("/about")
def about():
    name = "Peleke"
    location = "Tien Shan"

    return f"My name is {name}, and I live in {location}."


@app.route("/contact")
def contact():
    email = "peleke@example.com"

    return f"Questions? Comments? Complaints? Shoot an email to {email}."


# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
