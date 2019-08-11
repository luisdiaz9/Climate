import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
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
        f"/api/v1.0/2017-01-01<br/>"
        f"/api/v1.0/2017-01-01/2017-01-07<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Design a query to retrieve the last 12 months of precipitation data
    last1 = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # Calculate the date 1 year ago from the last data point in the database
    oldest1 = dt.datetime.strptime(last1[0], "%Y-%m-%d") - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    data1 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= oldest1).all()
    dictionary1=dict(data1)
    return jsonify(dictionary1)

@app.route("/api/v1.0/stations")
def stations(): 
    # List the stations
    most2=session.query(Measurement.station).group_by(Measurement.station).all()
    listJSON2 = list(np.ravel(most2))
    return jsonify(listJSON2)

@app.route("/api/v1.0/tobs")
def tobs(): 
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    last3 = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    oldest3 = dt.datetime.strptime(last3[0], "%Y-%m-%d") - dt.timedelta(days=365)
    data3 = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= oldest3).all()
    listJSON3 = list(data3)
    return jsonify(listJSON3)

@app.route("/api/v1.0/<start>")
def start(start=None):
    # Design a query to retrieve all dates above the starting date
    stats4 = session.query(Measurement.date,func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    listJSON4 = list(stats4)
    return jsonify(listJSON4)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    # Design a query to retrieve all dates between the starting and ending dates 
    stats5 = session.query(Measurement.date,func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    listJSON5 = list(stats5)
    return jsonify(listJSON5)        

if __name__ == '__main__':
    app.run(debug=True)