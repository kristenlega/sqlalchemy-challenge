import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Data base set up
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask set up
app = Flask(__name__)


# Routes

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate</br>"
        f"/api/v1.0/startdate/enddate<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Input the oldest date
    oldest_date = "2016-08-23"
    
    # Query
    precip_results = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date >= oldest_date).group_by(Measurement.date).all()

    session.close()

    # Convert into dictionary
    prcp_data = []
    for date, prcp in precip_results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = round(prcp,2)
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    results = session.query(Station.station).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    # all_dates = list(np.ravel(results))

    return jsonify(results)



@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Input the oldest date
    oldest_date = "2016-08-23"
    
    # Query
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= oldest_date).all()

    session.close()

    # Convert into dictionary
    tobs_data = []
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>")
def start_date(start):

    session = Session(engine)

    date_temps = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date>=start)

    session.close()

    temp_stats = []
    for tmin,tavg,tmax in date_temps:
        temp_dict = {}
        temp_dict["TMIN"] = tmin
        temp_dict["TAVG"] = tavg
        temp_dict["TMAX"] = tmax
        temp_stats.append(temp_dict)
    return jsonify(temp_stats)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

    session = Session(engine)

    date_temps = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date>=start, Measurement.date<=end)

    session.close()
    
    temp_stats = []
    for tmin,tavg,tmax in date_temps:
        temp_dict = {}
        temp_dict["TMIN"] = tmin
        temp_dict["TAVG"] = tavg
        temp_dict["TMAX"] = tmax
        temp_stats.append(temp_dict)
    return jsonify(temp_stats)


if __name__ == '__main__':
    app.run(debug=True)
