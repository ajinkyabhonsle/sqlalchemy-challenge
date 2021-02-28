#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import datetime as dt


# In[ ]:


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# In[ ]:


engine = create_engine("sqlite:///hawaii.sqlite")


# In[ ]:


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)


# In[ ]:


# Save references to each table
ms = Base.classes.measurement
st = Base.classes.station

session = Session(engine)

#Flask setup
app = Flask(__name__)

#Route endpoints
@app.route("/")
def welcome():
    return (
            f"Welcome to the Hawaii Climate API!! <br/>"
            f"Available Routes:  <br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/temp/start/end"
            
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    previous_year = dt.date(2017,8,23) - dt.timedelta(days = 365) 
    
    precipitaton = session.query(ms.date, ms.prcp).    filter(ms.date >= previous_year).all()
    
    precip = {date: prcp for date, prcp in precipitation }
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    result_set = session.query(st.station).all()
    
    stations = list(np.ravel(result_set))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    previous_year = dt.date(2017,8,23) - dt.timedelta(days = 365) 
    
    result_set = session.query(ms.tobs).    filter(ms.station == 'USC00519281').    filter(ms.date >= previous_year).all()
    
    temps = list(np.ravel(result_set))
    return jsonify(temps)

if __name__ == '__main__':
    app.run()

