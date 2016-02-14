import os
from datetime import datetime
from requests import get
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')
sl_api_key_realtime_dep = os.environ['SL_API_KEY_REALTIMEDEP']
@app.route('/')
def index():
    bandhv = get("https://api.sl.se/api2/realtimedepartures.json?key=" + sl_api_key_realtime_dep +
                 "&siteid=1867&timewindow=60").json()
    svedm = get("https://api.sl.se/api2/realtimedepartures.json?key=" + sl_api_key_realtime_dep +
                 "&siteid=9165&timewindow=60").json()
    bandhv_next = []
    svedm_next = []
    for bus in bandhv[u'ResponseData'][u'Buses']:
        if bus[u'JourneyDirection']==1:
            bandhv_next.append(bus[u'DisplayTime'])
    for metro in svedm[u'ResponseData'][u'Metros']:
        if metro[u'JourneyDirection']==1:
            svedm_next.append(metro[u'DisplayTime'])
    print svedm_next

    return render_template('index.html', bandhv_next=bandhv_next, svedm_next=svedm_next)

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"

if __name__ == '__main__':
    app.run()
