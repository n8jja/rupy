"""

Author: Jeremy Bush
Project: Radio Utilities in Python (RUPy), GPS utility library
Version: 3
Date: 6/10/2021

"""

import os
import serial
import pynmeagps
import pyubx2
from geopy import distance


class Gps:
    def __init__(self, com, baud=9600, timeout=3):
        self.com_port = com
        self.baud_rate = baud
        self.timeout = timeout

    # Get current gridsquare from Winlink Express.
    # Should be changed to allow configuration of path and program i.e. Pat, etc.)
    def get_current_grid_square(self):
        filepath = os.path.join('C:\\', 'RMS Express', 'RMS Express.ini')
        with open(filepath, 'r') as file:
            lines = file.read().split('\n')
        # Convert each list into a list of its own
        current_gridsquare = lines[26]
        current_gridsquare = current_gridsquare.split('=')
        return current_gridsquare[1]

    # Convert GPS coordinates into grid square
    def convert_to_grid(self, lat, lon):
        # adjust lat/lon per maidenhead calculation formula.  Followed the steps from here:
        # https://ham.stackexchange.com/questions/221/how-can-one-convert-from-lat-long-to-grid-square
        # The idea for using strings for upper/lower case letter strings came from Walter Underwood (K6WRU) based on his
        # Python script @ https://gist.github.com/laemmy/71ec20fd5d50a478e852618d94c16a8b
        upper = 'ABCDEFGHIJKLMNOPQRSTUVWX'
        lower = 'abcdefghijklmnopqrstuvwx'

        lon += 180.0
        lat += 90.0

        # get remainder for sub square calculation.
        lon_remainder = (lon - int(lon / 2) * 2) * 60
        lat_remainder = (lat - int(lat)) * 60

        # Perform the actual calculation and return
        return upper[int(lon / 20)] + upper[int(lat / 10)] + str(int((lon / 2) % 10)) + str(int(lat % 10)) + \
               lower[int(lon_remainder / 5)] + lower[int(lat_remainder / 2.5)]

    def convert_to_latlong(self, gridsquare):
        upper = 'ABCDEFGHIJKLMNOPQRSTUVWX'
        lower = 'abcdefghijklmnopqrstuvwx'

        gridsquare = list(gridsquare)
        lat = round(((float(upper.index(gridsquare[1]))) * 10) + float(gridsquare[3]) + (
                    ((lower.index(gridsquare[5].lower())) / 24) + (1 / 48) - 90.0), 6)
        lon = round(((float(upper.index(gridsquare[0])) * 20) + (float(gridsquare[2]) * 2) + (
                    float(lower.index(gridsquare[4].lower()) / 12) + (1 / 24))) - 180, 6)

        return lat, lon

    def get_geo_distance(self, user_station, foreign_station):
        return distance.distance(self.convert_to_latlong(user_station), self.convert_to_latlong(foreign_station)).miles


# The NmeaGPS class is created in order to connect to and utilize NMEA compatible GPS devices.
class NmeaGPS(Gps):
    def __init__(self, com):
        super().__init__(com)
        self.stream = serial.Serial(self.com_port, self.baud_rate, self.timeout)
        self.nmr = pynmeagps.NMEAReader(self.stream)

    # Read GPS coordinates from the GPS unit
    def get_gps_coordinates(self):
        # Open serial connection to the unit.  COM port may be different depending on each system.  Default is COM7

        (raw_data, parsed_data) = self.nmr.read()  # raw_data is not used, but is required or error will result.
        return [round(parsed_data.lat, 6), round(parsed_data.lon, 6)]

    # provide a live stream of raw NMEA GPS sentences.  Can be used for updating position on a map, etc.
    def gps_stream(self):
        (raw_data, parsed_data) = self.nmr.read()
        # There may be more code required...this may not read the GPS sentence specifically.
        return raw_data


# The UbloxGPS class is used to represent U-Blox GPS units.  Available data is  not the same
# as NMEA compatible GPS units.
class UbloxGPS(Gps):
    def __init__(self, com):
        super().__init__(com)


