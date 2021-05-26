
from flask import Flask, redirect, render_template, request, url_for
import requests
import json

app = Flask(__name__)
app.debug = True


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # Opening JSON file
        with open('/home/ddavis11/mysite/fips.json', 'r') as f:
            # Reading from json file
            fips_return = json.load(f)

        return render_template("main_page.html", fips_display=fips_return)

    # Get fips codes for states and territories
    with open('/home/ddavis11/mysite/fips.json', 'r') as f:
        fips_return = json.load(f)

    # Get selected state fips code from form
    selected_fips = request.form.get("states")

    # JSON file for testing
    # with open('/home/ddavis11/mysite/result.json', 'r') as f:
     #   request_return = json.load(f)

    return render_template("main_page.html", return_display=census_request(selected_fips), fips_display=fips_return)


def census_request(fips_selection=None):
    get_list = [
        "Aggregate_HH_INC_ACS_14_18",
        "Aggr_House_Value_ACS_14_18",
        "Owner_Occp_HU_ACS_14_18",
        "avg_Agg_House_Value_ACS_14_18",
        "Tot_Occp_Units_ACS_14_18",
        "pct_Owner_Occp_HU_ACS_14_18"
    ]

    get_string = "get=" + ",".join(get_list)

    if fips_selection:
        for_pred = "for=state:" + fips_selection
    else:
        for_pred = "for=state:*"

    base_url = "https://api.census.gov/data/2020/pdb/statecounty"
    end_point = base_url + "?" + get_string + "&" + for_pred

    res = requests.get(end_point)

    # check for valid request
    # print(f"status code: {res.status_code}")
    if res.status_code != 200:
        return "ERROR: API request unsuccessful."
    else:
        return res.json()
