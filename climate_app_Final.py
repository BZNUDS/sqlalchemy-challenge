# 1. Import Flask and add other
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import distinct
# create engine to hawaii.sqlite (BZ had to add Resources/)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Create our session (link) from Python to the DB
# Create a session
session = Session(engine)

# reflect an existing database into a new model
# Declare a Base using `automap_base()`
Base = automap_base()

# reflect the tables
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
# Print all of the classes mapped to the Base
Base.classes.keys() 

# Save references to each table
# Assign the measurement class to a variable called `Measurement`
# Assign the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station


# 2. Create an app
app = Flask(__name__)

# Declare Global variables
M=Measurement
S=Station

# 3. Define static routes
@app.route("/")
def index():
    return (
        f"Welcome to my SQLAlchemy Climate App Homepage.<br>"
        f"Avaialble routes:<br/>"
        f"/api/v1.0/precipitation  Converts the query results to a dictionary using date as the key and prcp as the value. Returns JSON representation of the dictionary.<br/>" 
        f"/api/v1.0/stations  Returns a JSON list of stations from the dataset.<br/>"
        f"/api/v1.0/tobs  Queries the dates and temperature observations of the most active station for the last year of data. Returns a JSON list of the TOBS for the previous year.<br/>"
        f"/api/v1.0/<start>  Returns a JSON list of the TMIN, TAVG, and TMAX Temperatures for all dates greater than and equal to the start date.<br/>"
        f"/api/v1.0/<start>/<end>  Returns a JSON list of the TMIN, TAVG, and TMAX Temperatures for the dates between the start and end date inclusive.<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query all of the percepitations 
    results = session.query(M.date, M.prcp).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    date_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Percipitation"] = prcp
        date_prcp.append(prcp_dict)

    return jsonify(date_prcp)



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query all stations
    print()
    print(f'Entering stations')
    print()

    results = session.query(S.station).all()
    print(f'Station results: {results}')
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    # Queries the dates and temperature observations of the most active station for the last year of data. 
    # Returns a JSON list of the TOBS for the previous year.
    # Special tahnks to TA Mohammad Hamza for helping student Ryan T with his homework during office hours
    # as I was also strug;ling with the @app.route logic/code
    # Re-using what we already determined/reported in climate_starter_Final.ipynb
    # min_date is the date 12 months prior to last date in our data
    min_date = '2016-08-23'
    #most_active is the most active station  
    most_active = 'USC00519281'
    temps_for_12 = []
    
    print()
    print(f'Entering tobs')
    print()
    results = session.query(M.date, M.tobs, M.station).\
        filter(M.date >= min_date).\
        filter(M.station == most_active).\
        order_by(M.date).all()
    session.close()

    # Save the query results as a Pandas DataFrame
    station_counts_df = pd.DataFrame(results['Date'], results['Temperature'])
    station_counts_df.set_index('Date', inplace=True)

    return jsonify(station_counts_df)


@app.route("/api/v1.0/<start>")
def start():
    name = "Can't use the Start word twice"
    location = "Tien Shan"

    return f"My name is {name}, and I live in {location}."


@app.route("/api/v1.0/<start>/<end>")
def start_end():
    name = "Can't use the S word twice???"
    location = "Tien Shan"

    return f"My name is {name}, and I live in {location}."


# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)