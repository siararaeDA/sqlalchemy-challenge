import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify, render_template

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

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    # Found this option via Stack Overflow
    return render_template('routes.html')


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    mostRecent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    #print(mostRecent) - 08/23/2017
    firstDate = dt.datetime(2016, 8, 23)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= firstDate).\
            order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp = []
    for result in results:
        prcpDict = {}
        prcpDict['date'] = result[0]
        prcpDict['prcp'] = result[1]

        all_prcp.append(prcpDict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station, Station.name).all()

    session.close()

    stationList = []
    for result in results:
        stationList.append(result[1])

    return jsonify(stationList)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    sel = [Measurement.station, func.count(Measurement.station)]
    activityCounts = session.query(*sel).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    mostActive = activityCounts[0][0]
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == mostActive).\
                filter(Measurement.date >= '2016-08-23').all()

    session.close()

    tobsList = list(np.ravel(results))

    return jsonify(tobsList)
# @app.route("api/v1.0/<start>")
# @app.route("/api/v1.0/<start>/<end>")

if __name__ == '__main__':
    app.run(debug=True)