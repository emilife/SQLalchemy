# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
station = Base.classes.station
measurement = Base.classes.measurement 
session = Session (engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    starting_date = "2016-08-23"
    precipitation = session.query(measurement.date,measurement.prcp).\
    filter(measurement.date > starting_date).all()
    session.close()
    pdate = {date: prcp for date, prcp in precipitation}
    return jsonify (pdate)

# /api/v2.0/stations
@app.route("/api/v1.0/stations")
def stations():
    st_count = session.query(func.count (station.station)).all()
    session.close()
    stations = list((np.ravel(st_count)))
    stations = stations[0]
    stations = str(stations)
    return jsonify(stations=stations)
    #list or dictionary 

@app.route("/api/v1.0/tobs")
def tob():
    starting_date = "2016-08-23"
    yeartemp = session.query(measurement.tobs).filter(measurement.date > starting_date).filter(measurement.station == "USC00519281").all()
    yeartemp_list = list((np.ravel(yeartemp)))

    session.close()
    return jsonify(yeartemp_list = yeartemp_list)

@app.route("/api/v1.0/temp/<start>")
def temp(start = None):
    start = start
    temp = session.query(func.min(measurement.tobs), func.max(measurement.tobs),func.avg(measurement.tobs)).\
    filter(measurement.date >=  start).filter(measurement.station == "USC00519281").all()
    temp = list((np.ravel(temp)))
    session.close()
    print(temp)
    return jsonify(temp = temp)

if __name__ == "__main__": 
    app.run(debug = True)
 


