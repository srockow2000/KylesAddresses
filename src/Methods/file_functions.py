from flask import Flask, render_template, request, send_from_directory
from geopy.geocoders import Nominatim
import os
from flask_mysqldb import MySQL
import re
import csv

class FileFunctions():
    def parseData(filename, pattern):
        f = open(filename)
        addresses = []

        for line in f:
            x = re.findall(pattern, line)

            if len(x) != 0 and x not in addresses:
                addresses.append(x)
                print(x)

        return addresses

    def addressData(filename):
        f = open(filename)
        addresses = []

        for line in f:
            addresses.append(line)

        return addresses

    def uploadData(mysql, addresses):

        i = 0
        cur = mysql.connection.cursor()
        sql = "INSERT INTO only_addresses (address) VALUES (%s)"

        for i in range(0, len(addresses) - 1):
            cur.execute(sql, addresses[i])

        mysql.connection.commit()

    def stripAddresses(addresses):
        i = 0

        for i in range(0, len(addresses) - 1):
            str(addresses[i]).strip("'[]")

    def writeCSV(records):
        with open('records.csv', mode='w') as record_file:
            record_writer = csv.writer(record_file)

            for record in records:
                record_writer.writerow(record)


class DBOps():
    def getAddresses(filename, pattern):
        f = open(filename)
        test = []
        addresses = []

        for line in f:
            test.append(line)

        patternMANUAL = "/\s\d{1,6}\+\s\+[A-Z]*\+\s*[A-Z]*/gm"

        for val in test:
            x = re.search(pattern, val)
            addresses.append(x)

        return addresses

    def googleExport(glocator, record, city, state):
        exportArray = []

        for address_rows in record:
            rows = str(address_rows).lstrip().rstrip().strip("[]'")

            try:
                full_address = glocator.geocode(rows + ", " + city + ", " + state)
                split_address = str(full_address).split(',')
                zip = split_address[len(split_address) -2]


                final_address = rows + ", " + city + ", " + zip
                #final_address = zip
                exportArray.append(final_address)

            except:
                exportArray.append("NOT FOUND: " + str(rows))
        return exportArray

    def showAddresses(mysql):
        cur = mysql.connection.cursor()

        records = cur.execute("SELECT * FROM records")
        geolocator = Nominatim(user_agent="KylesAddresses")

        if records > 0:
            recordDetails = cur.fetchall()
            google_addresses = DBOps.googleExport(geolocator, recordDetails)

            for count in range(0, 8):
                cur.execute("UPDATE records SET address_link = '" +
                            google_addresses[count] +
                            "' WHERE category='MONROVIA'")
                mysql.connection.commit()

                # "' WHERE address_parcel_number LIKE '%" + google_addresses[count] + "%'")
                print(google_addresses[count])
                count += 1