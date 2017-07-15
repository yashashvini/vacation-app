__author__ = 'hemalatha_ganireddy'
from flask import Flask
app = Flask(__name__)
import os.path
import sys
import json
import datetime
# try:
#     import apiai
# except ImportError:
#     sys.path.append(
#         os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
#     )
#     import apiai
# # CLIENT_ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
# client_access_token = '8bd3b6024a8e461f8e4e63c181882295'


@app.route("/")
def basic():
    long_weekends = {"Independence Day": "TUESDAY, JULY,2017",
    "LABOR DAY":"MONDAY, SEPTEMBER 4, 2017 ",
    "COLUMBUS DAY":"MONDAY, OCTOBER 9, 2017",
    "VETERANS DAY":"FRIDAY, NOVEMBER 10, 2017",
    "THANKSGIVING DAY":"THURSDAY, NOVEMBER 23, 2017",
    "MONDAY, DECEMBER 25, 2017":"CHRISTMAS DAY"}
    vacations_by_month = {"January": ["Caribbean","Australia","Shetland Islands","Scotland","Northern lights in Norway",
                                     "Mexico (Puerto Escondido for something lively, Mazunte, San Agustinillo and Zipolite for something a little quieter)"," Brazil",
                                     " Ethiopia", "Scotland", "Norway", "France", "Switzerland", "Austria", "The West Indies and the Caribbean", "the Dominican Republic", "South Africa"],
                          "February": ["Buenos Aires", "Argentina", "Africa", "Egypt", "South Africa", "Hawaii"],
                          "March" : ["Italy", "Asia", "America", "Cuba", "Argentina", "the Maldives"],
                          "April" : ["Crete", "Malta", "Baleric Islands", "Africa", "Amsterdam, America, Turkey, the Philippines, Japan, Australia."],
                          "May" : ["Europe,the Philippines, the Bahamas, Mexico, Australia"],
                          "June" : ["Europe", "Namibia", "Brazil", "The Caribbean", "Canada", "Cuba"],
                          "July" : ["Australia", "Europe", "Indonesia", "Peru", "Bolivia", "America"],
                          "August" : ["Europe", "South Africa", "Peru and Tibet"],
                          "September" : ["Portugal", "Croatia", "Africa", "America", "China", "Japan"],
                          "October" : ["India", "Calcutta", "Turkey", "Cyprus", "Africa", "Egypt", "South Africa", "America", "Argentina", "Japan", "Venice"],
                          "November" : ["New Zealand", "Hawaii", "Aspen", "Germany", "America", "South America", "Morocco", "Belize", "Hong Kong"],
                          "December" : ["Mexico", "Belize", "Skiing Destinations", "the Caribbean", "Cambodia", "Australia", "Iceland"]
                          }
    current_date = str(datetime.datetime.now())
    month_list = ["January","February","March","April","May","June","July","September","October","November","December"]
    if(current_date[5:6] == '0'):
        month = current_date[6:7]
    else:
        month = current_date[5:7]
    month = month_list[int(month) - 1]
    print month
    holiday_occasion = "None"
    holiday_date = "None"
    for key, value in long_weekends.iteritems():
        if(month.upper() in value ):
            holiday_occasion = key
            holiday_date = value
            break
    vacation = vacations_by_month[month]
    return [holiday_occasion,holiday_date,vacation]




if __name__ == '__main__':
    basic()
    app.run()
