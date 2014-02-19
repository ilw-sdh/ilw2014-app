from math import radians, sqrt, sin, cos, atan2
import json
import os
import csv

SEARCH_RADIUS = 20

iata_codes = {}
airports = {}
airports_by_country = {}

dir = os.path.dirname(__file__)

with open(os.path.join(dir, './../data/airports.dat'), 'r') as f:
    reader = csv.reader(f)
    for item in reader:

        if item[5] != '\N':
            airports[item[4]] = (float(item[6]), float(item[7]))
            if not (item[3] in airports_by_country):
                airports_by_country[item[3]] = {}
            airports_by_country[item[3]][item[4]] = airports[item[4]]
            iata_codes[item[4]] = item[1:4]


def geocalc(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon1 - lon2

    EARTH_R = 6372.8

    y = sqrt(
        (cos(lat2) * sin(dlon)) ** 2
        + (cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)) ** 2
        )
    x = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(dlon)
    c = atan2(y, x)
    return EARTH_R * c

def closest(lat, lon):
    result, dist = None, -1
    for k, v in airports.iteritems():
        d = geocalc(lat, lon, v[0], v[1])
        if not result or d < dist:
            result = k
            dist = d
    return result

def around(lat, lon):
    results = []
    for k, v in airports.iteritems():
        if geocalc(lat, lon, v[0], v[1]) < SEARCH_RADIUS:
            results.append(k)
    return results if len(results) > 0 else [closest(lat, lon)]

def around_by_country(country, lat, lon):
    if not (country in airports_by_country): return around(lat, lon)
    results = []
    for k, v in airports_by_country[country].iteritems():
        if geocalc(lat, lon, v[0], v[1]) < SEARCH_RADIUS:
            results.append(k)
    return results if len(results) > 0 else [closest(lat, lon)]

def iata_to_name(iata):
    return iata_codes[iata]

#print around(55.9500, -3.2000)