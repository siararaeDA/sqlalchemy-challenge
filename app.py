import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/countries<br/>"
        f"/billing"
    )


@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all countries. Note there may be dupes - why?"""
    # Query all passengers
    results = session.query(Invoices.BillingCountry).all()

    session.close()

    # Convert list of tuples into normal list
    all_countries = list(np.ravel(results))

    return jsonify(all_countries)

@app.route("/api/v1.0/stations")
@app.route("/api/v1.0/tobs")
@app.route("api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")