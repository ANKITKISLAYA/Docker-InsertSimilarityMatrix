# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 11:03:17 2020

@author: Ankit
"""

import flask
from flask import request, jsonify, url_for
import pandas as pd
from InsertRecSys import InsertRecSys

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask import Flask, render_template
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)


sentry_sdk.init(
    dsn="https://d4f55392a9aa4f78a816e498c88fb5c3@sentry.io/1873356",
    integrations=[FlaskIntegration()]
)


@app.route('/insertmatrix')
def insertmatrix():
    df1 = InsertRecSys().read()
    df2 = InsertRecSys().ExtractItemid(df1)
    df3 = InsertRecSys().Clean(df2)
    df4 = InsertRecSys().AddRating(df3)
    df5 = InsertRecSys().RenameColumns(df4)
    ltup = InsertRecSys().CosineSimilarityMatrix(df5)
    finalfreq = InsertRecSys().finalfreq(ltup)

    SimMat = ltup[0]
    lv = list(finalfreq.values())
    lc = list(finalfreq.keys())
    SimMat1 = lv * SimMat
    df_final = pd.DataFrame(SimMat1, columns = lc , index = lc)
    df_columns = df_final.columns.astype(str)
    lcolumn = list(df_columns)
    df1 = pd.DataFrame(df_final.values , columns = lcolumn , index = lcolumn)
    df1.reset_index(inplace=True,drop = True)
    lcolumn = [int(i) for i in lcolumn]
    df1.insert(0,"itemid",lcolumn)
    
    InsertRecSys().insertdata(df1)
    
    return ("Data Inserted")



if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0", debug=False)











