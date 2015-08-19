#!/bin/bash
#
# hostInfo.sh ver 0.0.1
#
# Since the old, free version of maxminds' database has some info that
# the new version has not, it might be a good idea to query it also
# (using geoiplookup). Also, resolving the hostname of a given ip
# would be nice. This script does all this. If you have geoiplookup
# installed, it will query both the "normal" (Country) DB as well as
# the City Edition (if it is located in /usr/share/GeoIP).
# If you have host installed, host <ip> will also be called, which
# should reveal the hostname(s) for the given IP.
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

cityEdition="/usr/share/GeoIP/GeoLiteCity.dat"

unset geoiplookupAvailable
unset cityEditionAvailable
geoiplookup -h &> /dev/null
if [ $? -eq 0 ]; then
  geoiplookupAvailable=true
  [ -f $cityEdition ] && cityEditionAvailable=true
fi
echo "geoiplookupAvailable=$geoiplookupAvailable"

unset hostAvailable
host localhost &> /dev/null
[ $? -eq 0 ] && hostAvailable=true
echo "hostAvailable=$hostAvailable"

for host in $*; do
  if [[ $host =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
    ip=$host
    host=""
  else
    ip=`dig +short $host | tail -n1`
    host="$host "
  fi

  geoIP2.py $ip
  [ $geoiplookupAvailable ] && geoiplookup $ip
  [ $cityEditionAvailable ] && geoiplookup -f $cityEdition $ip
  [ $hostAvailable ] && host $ip
  echo "(End of info on host ${host}with ip: $ip)"
done
