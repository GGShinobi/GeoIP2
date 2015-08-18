#! /usr/bin/python
# vim: set fileencoding=utf-8 :
#
# geoIP2.py ver 0.0.1
#
# This script can be used to query the maxmind GeoIP2 City database 
# (usually found in '/usr/share/GeoIP/GeoLite2-City.mmdb').
#
# If you don't have the database you can download it from here:
# http://dev.maxmind.com/geoip/geoip2/geolite2/
#
# The script requires maxminds' "GeoIP2-python" to be installed on the system.
# You can install it with the following command:
#
#  $ pip install geoip2
#
# When installed correctly, you can open a python console by typing
#
#  $ python
#
# and then check if you can use geoip2 by typing:
#
# >>> import geoip2.database
#
# if this yields an error, geoip2 has not been correctly installed!
# On my system, I also had to make the installed files world-readable in order
# to be able to use them. I did so by changing into the installation directory:
#
#  $ cd /usr/local/lib/python2.7/dist-packages/
#
# and doing:
#
#  $ sudo find . -type d -exec chmod go+x+r '{}' +
#  $ sudo find . -type f -exec chmod go+r '{}' +
#
# At the moment, the script tries to print the information in only 3 of the
# supported languages, namely in: english (en), german (de) and japanese (ja).
#
# A future release (if it comes) will allow the user to specify the languages
# via command line options. :) And maybe more.
#
#
#
#   Copyright © 2015 GGShinobi (GGShinobi@googlemail.com)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import geoip2.database
import sys, getopt


def main(argv):
  database = '/usr/share/GeoIP/GeoLite2-City.mmdb'
  helptext = 'geoIP2.py [-f <database-file>] [-h] [-d] [ip-list]'
  # languages = {'en', 'de', 'ja'}
  debug = False
  ipStart = 1
  try:
    opts, args = getopt.getopt(argv,"hf:d",["help","file=", "debug"])
  except getopt.GetoptError:
    print helptext
    sys.exit(2)
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      print helptext
      sys.exit()
    elif opt in ("-f", "--file"):
      database = arg
      print 'using database:', database
      ipStart += 1
    elif opt in ("-d", "--debug"):
      debug = True
      print '[debug mode]'
      ipStart += 1

  # This creates a Reader object. You should use the same object
  # across multiple requests as creation of it is expensive.
  try:
    reader = geoip2.database.Reader(database)
    for i in range(ipStart,len(sys.argv)):
      print "============================================"
      print "GeoIP2 Info on:", sys.argv[i]
      print "============================================"
      try:
        cityInfo = reader.city(sys.argv[i])
        # print "City:", cityInfo.city.name, "/", cityInfo.city.names['de'], "/", cityInfo.city.names['ja']
        # some entries don't have other languages, so we need to check and only attempt to print them if they do:
        cityNames = ""
        if 'de' in cityInfo.city.names:
          cityNames += "/ " + cityInfo.city.names['de']
        if 'ja' in cityInfo.city.names:
          cityNames += " / " + cityInfo.city.names['ja']
        # even City Name can be empty! :-o So don't use "+"-operator here:
        print "City:", cityInfo.city.name, cityNames
        # print "City: %s / %s / %s" % (cityInfo.city.name, cityInfo.city.names['de'], cityInfo.city.names['ja']) # alternate way
        print "Postal Code:", cityInfo.postal.code
        msic = "" # (m)ost_(s)pecific.(i)so_(c)ode might be empty, so check:
        if (cityInfo.subdivisions.most_specific.iso_code != None):
          msic += " (" + cityInfo.subdivisions.most_specific.iso_code + ")"
        print "State:", cityInfo.subdivisions.most_specific.name, msic
        subDivCount = len(cityInfo.subdivisions)
        if (subDivCount > 0):
          print "Subdivisions:"
        for k in range(0, subDivCount):
          iso_code = ""
          if (cityInfo.subdivisions.most_specific.iso_code != None):
            iso_code += "(" + cityInfo.subdivisions[k].iso_code + ")"
          subdivisionInfo = "  -> " + cityInfo.subdivisions[k].names['en'] + iso_code
          if 'de' in cityInfo.subdivisions[k].names:
            subdivisionInfo += " / " + cityInfo.subdivisions[k].names['de']
          if 'ja' in cityInfo.subdivisions[k].names:
            subdivisionInfo += " / " + cityInfo.subdivisions[k].names['ja']
          print subdivisionInfo
        print "Country:", cityInfo.country.name, "(" + cityInfo.country.iso_code + ") /", cityInfo.country.names['de'], "/", cityInfo.country.names['ja']
        print "Continent:", cityInfo.continent.name, "/", cityInfo.continent.names['de'], "/", cityInfo.continent.names['ja']
        print "Coordinates:", cityInfo.location.latitude, "N", cityInfo.location.longitude, "E"
        print "Time Zone:", cityInfo.location.time_zone
        print "Registered Country:", cityInfo.registered_country.name, "(",cityInfo.registered_country.iso_code,")"
        # print cityInfo
      except:
        exIn = sys.exc_info()
        for j in range(0, len(exIn)):
          print exIn[j]
        if debug: raise
  except:
    exIn = sys.exc_info()
    for j in range(0, len(exIn)):
      print exIn[j]
    if debug: raise
  finally:
    try:
      reader.close()
    except:
     pass


if __name__ == "__main__":
   main(sys.argv[1:])
