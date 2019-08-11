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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
        f"/api/v1.0/2017-01-01"
        f"/api/v1.0/2017-01-01/2017-01-07"
    )

    @app.route("/api/v1.0/precipitation")
    def precipitation():
        # Design a query to retrieve the last 12 months of precipitation data and plot the results
        last = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
        # Calculate the date 1 year ago from the last data point in the database
        oldest = dt.datetime.strptime(last[0], "%Y-%m-%d") - dt.timedelta(days=365)
        # Perform a query to retrieve the data and precipitation scores
        data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= oldest).all()
        dictionary=dict(data)
        return jsonify(dictionary)

    @app.route("/api/v1.0/stations")
    def stations(): 
        # List the stations
        most=session.query(Measurement.station).group_by(Measurement.station).all()
        listJSON = list(np.ravel(most))
        return jsonify(listJSON)

    @app.route("/api/v1.0/tobs")
    def tobs(): 
        # Design a query to retrieve the last 12 months of precipitation data and plot the results
        last = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
        oldest = dt.datetime.strptime(last[0], "%Y-%m-%d") - dt.timedelta(days=365)
        data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= oldest).all()
        listJSON = list(data)
        return jsonify(listJSON)

    @app.route("/api/v1.0/<start>")
    def start(start=None):
        stats = session.query(Measurement.date,func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
        listJSON = list(stats)
        return jsonify(listJSON)

    @app.route("/api/v1.0/<start>/<end>")
    def start_end(start=None, end=None):
        stats = session.query(Measurement.date,func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
        listJSON = list(stats)
        return jsonify(listJSON)        

if __name__ == '__main__':
    app.run(debug=True)