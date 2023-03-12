
import functools

#Our webapp libraries
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, Response)
from werkzeug.security import check_password_hash, generate_password_hash
from EE_CafeWeb.db import get_db
from EE_CafeWeb.home import login_required

#Our os 
import os
import io
import json

#We will use both the sdk and api for Cisco Meraki this is the library SDK
import requests
import asyncio
from requests_oauthlib import OAuth1Session
import meraki


# For drawing visualizatins directly with python
from matplotlib.backends.backend_agg import FigureCanvasAgg as figc
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

os.environ.get('XCiscoMerakiAPIKey')

normal_config = {}
network_dict = {}
device_dict = {}

blueprint_dash = Blueprint('dashboard', __name__, url_prefix='/dashboard')

class NoRebuildAuthSession(Session):
 def rebuild_auth(self, prepared_request, response):
   '''
   No code here means requests will always preserve the Authorization header when redirected.
   Be careful not to leak your credentials to untrusted hosts!
   '''

@blueprint_dash.route('/', methods=('GET', 'POST'))
@login_required
def dashboard():
    if g.user is not None:
        if request.method == "GET":
            return render_template('dashboard/dashboard.html')
        elif request.method == "POST":
            return render_template('dashboard/dashboard.html')
        else:
            #return render_template('auth.login'), 405, {'Content-Type': 'application/json'}
            return render_template('dashboard/dashboard.html')
    else:
        #return render_template('auth.login')
        #only use login less dash under testing conditions.
        return render_template('dashboard/dashboard.html')

#taken from documentation Change to return response values and not print them.
@blueprint_dash.route('/meraki_user_authorize', methods=('GET', 'POST'))
@login_required
def meraki_user_authorize():
    try:
        session = NoRebuildAuthSession()
        API_KEY = X-Cisco-Meraki-API-Key
        response = session.get('https://api.meraki.com/api/v1/organizations/', headers={'Authorization': f'Bearer {API_KEY}'})
        print(response.json()) 
        return render_template('dashboard/dashboard.html', personal_auth=transfer_dict)
    except Exception as error:
        return render_template('dashboard/dashboard.html', personal_auth=error)   
 
#taken from documentation Change to return response values and not print them.
@blueprint_dash.route('/meraki_user_authorize', methods=('GET', 'POST'))
@login_required
def meraki_user_authorize():
    try:
        dashboard = meraki.DashboardAPI(API_KEY)
        response = dashboard.organizations.getOrganizations()
        print(response) 
        return render_template('dashboard/dashboard.html', personal_auth=transfer_dict)
    except Exception as error:
        return render_template('dashboard/dashboard.html', personal_auth=error)   
 
 #API URL options
 # /createOrganization
 # /networks
 # /devices
 # /health
 # /trafficAnalysis      

@blueprint_dash.route('/active_friends', methods=('GET', 'POST'))
@login_required
def active_devices():
    #Junk data for testing right now.
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    test_fig = Figure()
    axis = test_fig.add_subplot(1, 1, 1)
    xs = [1, 2, 3, 4, 5, 6, 7, 8, 9 ,10]
    ys = [3, 3, 3.35, 3.15, 3, 3.15, 3, 3.25, 3, 3.15]
    axis.plot(xs, ys)
    output = io.BytesIO()
    figc(test_fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')    


@blueprint_dash.route('/networks', methods=('GET', 'POST'))
#@login_required
def networks():
async def devices(aiomeraki: meraki.aio.AsyncDashboardAPI, org):
    try:
        networks = await aiomeraki.clients.getOrganizationNetworks(
            org["id"]
        )
    except meraki.AsyncAPIError as eM:
        return eM
    except Exception as e:
        return e
    else:
        if clients:
            #update dashboard on webpage.
            return networks
    return org["id"], None

@blueprint_dash.route('/devices', methods=('GET', 'POST'))
#@login_required
async def devices(aiomeraki: meraki.aio.AsyncDashboardAPI, network):
    try:
        clients = await aiomeraki.clients.getNetworkClients(
            network["id"],
            timespan=60*60*24
            perPage=1000,
            total_pages="all",
        )
    except meraki.AsyncAPIError as eM:
        return eM
    except Exception as e:
        return e
    else:
        if clients:
            #update dashboard on webpage.
            return network["name"], field_names
    return network["name"], None


@blueprint_dash.route('/bandwidth_perc', methods=('GET', 'POST'))
#@login_required
def meals():
    pass

@blueprint_dash.route('/total_data', methods=('GET', 'POST'))
#@login_required
def market():
    pass


#@blueprint_dash.route('/webex_active', methods=('GET', 'POST'))
#def webex_active():
#    pass

