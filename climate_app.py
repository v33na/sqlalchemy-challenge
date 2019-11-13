from flask import Flask, jsonify
import os
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from sqlalchemy import MetaData, inspect

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table stations and measurements
Station = Base.classes.station
Measurement = Base.classes.measurement
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")

def Home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"Returns dates and temperature from the last year. <br><br>"
        f"/api/v1.0/stations<br/>"
        f"Returns a json list of stations. <br><br>"
        f"/api/v1.0/tobs<br/>"
        f"Returns list of Temperature Observations(tobs) for previous year. <br><br>"
        f"/api/v1.0/yyyy-mm-dd<br/>"   
        f"Return a JSON list of min temp,avg temp,max temp for all dates greater and = to the start date.<br><br>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
        f"Return a json list of min temp,avg temp,max temp for a given start-end range.<br><br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """Convert the query results to a Dictionary using date as the key and prcp as the value"""
    """Return the JSON representation of your dictionar"""
    #    # Query all precipitation
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-24", Measurement.date <= "2017-08-23").all()
    session.close()    
    # creates JSONified list
    precipitation_list = [results]

    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a JSON list of stations from the dataset"""
    
    # Query all stations
    results = session.query(Station.name, Station.station, Station.elevation).all()
    session.close()
        
    # creates JSONified list of dictionaries
    station_list = []
    for result in results:
        row = {}
        row['name'] = result[0]
        row['station'] = result[1]
        row['elevation'] = result[2]
        station_list.append(row)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    
    # Query all passengers
    results = session.query(Station.name, Measurement.date, Measurement.tobs).all()
    session.close()
        
    # creates JSONified list of dictionaries
    tobs_list = []
    for result in results:
        row = {}
        row['Station'] = result[0]
        row['Date'] = result[1]
        row['Temperature'] = result[2]
        tobs_list.append(row)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<date>/")
def start(date):
    session = Session(engine)
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for all dates greater than and equal to the start date."""
    
    # Query all tables
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= date).all()
    session.close()   
    # creates JSONified list of start date dictionaries
    start_list = []
    for result in results:
        row = {}
        row["Start Date"] = date
        row["End Date"] = '2017-08-23'
        row["Average Temperature"] = float(result[0])
        row["Max Temperature"] = float(result[1])
        row["Min Temperature"] = float(result[2])
        start_list.append(row)
    return jsonify(start_list)

@app.route("/api/v1.0/<start_date>/<end_date>/")
def start_end(start_date, end_date):
    session = Session(engine)
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for all dates greater than and equal to the start date."""
    # Query all tables
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    session.close()
    # creates JSONified list of start date dictionaries
    start_list = []
    for result in results:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Average Temperature"] = float(result[0])
        row["Max Temperature"] = float(result[1])
        row["Min Temperature"] = float(result[2])
        start_list.append(row)
    return jsonify(start_list)


if __name__ == '__main__':
    app.run(debug=True)
