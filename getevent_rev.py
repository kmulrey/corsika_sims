import pycrtools as cr
from optparse import OptionParser
import psycopg2
import cPickle as pickle
import numpy as np
import ldf_db_rev as dbldf

# -----------
# Script to draw LDF from 2nd stage pipeline, total intensity as well as footprint, needs database specified"

# Parse commandline options
parser = OptionParser()
parser.add_option("-n", "--event", default = "0", help = "filename of database")
parser.add_option("-s", "--station", default = "CS002", help = "stationname")

(options, args) = parser.parse_args()


core_x, core_y , stname, positions, dist, x_err, signals, power11, power21, power41, rms, noisepower, time, lora_x, lora_y, lora_dens, az, elev, elev_lora, xyz_files = dbldf.GetLDF(options.event,options.station)


print xyz_files.shape
print positions.shape

#print powers
pickfile = 'info/info_{0}_{1}.dat'.format(options.event,options.station)
f = open(pickfile, 'w')

pickle.dump((core_x, core_y , stname, positions, dist, x_err, signals, power11, power21, power41, rms, noisepower, time, lora_x, lora_y, lora_dens, (450-az)/180.*np.pi, (90-elev)/180.*np.pi,(90-elev_lora)/180.*np.pi,xyz_files),f)

f.close()