from flask import Flask, render_template, request, send_from_directory
from geopy.geocoders import Nominatim
import os
from flask_mysqldb import MySQL
import re
from Methods.file_functions import FileFunctions, DBOps

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = "enforcement_records"

mysql = MySQL(app)

"""
filename = 'Code Enforcements in last 30 days_230318_222706.txt'
addressRegex = "\s\d{1,6}\s[^(0-9)]*"
city = "Waterford"
state = "Michigan"
"""
filename = 'FOIAEdit.csv'
addressRegex = "*"
city = "Westland"
state = "Michigan"

"""
Step 1: Upload file
"""

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload():

    if request.method == 'POST':

        # Get the list of files from webpage
        files = request.files.getlist("file")

        # Get address format and city
        addressRegex = request.form.get("addressFormat")
        city = request.form.get("cityName")
        state = request.form.get("stateName")

        # Iterate for each file in the files List, and Save them
        for file in files:
            file.save(file.filename)
            filename = file.filename

        return "<h1>Files uploaded. Go back and view records.</h1>"

    return render_template('upload.html')

@app.route('/records', methods=['POST', 'GET'])
def records():
    """
    badRecords = []


    # Parse the data with regex, upload to database
    #records = FileFunctions.parseData(filename, addressRegex)
    records = FileFunctions.addressData(filename)
    FileFunctions.stripAddresses(records)
    FileFunctions.uploadData(mysql, records)

    glocator = Nominatim(user_agent="Kyles_addresses")
    zips = DBOps.googleExport(glocator, records, city, state)



    return render_template('records.html', records=zips, badRecords=badRecords, writeCSV=FileFunctions.writeCSV(zips))
    """
    records = FileFunctions.addressData(filename)
    glocator = Nominatim(user_agent="Kyles_addresses")
    zips = DBOps.googleExport(glocator, records, city, state)
    badRecords = []

    for entries in zips:
        if "None" in entries or "NOT FOUND" in entries:
            badRecords.append(entries)
            zips.remove(entries)

    return render_template('records.html', records=zips, badRecords=badRecords, writeCSV=FileFunctions.writeCSV(zips))


if __name__ == "__main__":
    app.run(debug=True)