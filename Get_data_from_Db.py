import matplotlib
#matplotlib.use('Agg')
import pycrtools as cr
from optparse import OptionParser
import numpy as np
from pycrtools import crdatabase as crdb
from pycrtools.tasks import Task
import psycopg2
import sys
import cPickle

use_events=np.genfromtxt(open('cr_physics_new'))

print 'number of events on list:  {0}'.format(len(use_events))
Task.task_write_parfiles = False


# Options
parser = OptionParser()

parser.add_option("--host", default='coma00.science.ru.nl', help="PostgreSQL host.")
parser.add_option("--user", default='crdb', help="PostgreSQL user.")
parser.add_option("--password", default='crdb', help="PostgreSQL password.")
parser.add_option("--dbname", default='crdb', help="PostgreSQL dbname.")
#parser.add_option("-e","--event", default=81409140, help="Taking a look at LDF")


(options, args) = parser.parse_args()



# Connecting to database
conn = psycopg2.connect(host=options.host, user=options.user, password=options.password, dbname=options.dbname)

c = conn.cursor()
station='CS002'

#AND (s.stationname='{1}')

for i in use_events:
    ev=int(i)
    print ev
    # Collecting LOFAR data of event
    
    c.execute("""SELECT  pp.crp_integrated_pulse_power,pp.crp_integrated_noise_power, s.stationname  FROM
    events AS e
    INNER JOIN eventparameters AS ep ON (e.eventID=ep.eventID)
    INNER JOIN event_datafile AS ed ON (e.eventID=ed.eventID)
    INNER JOIN datafile_station AS ds ON (ed.datafileID=ds.datafileID)
    INNER JOIN station_polarization as sp ON (ds.stationID=sp.stationID)
    INNER JOIN polarizations as p ON (sp.polarizationID=p.polarizationID)
    INNER JOIN polarizationparameters as pp ON (sp.polarizationID=pp.polarizationID)
    INNER JOIN stations as s ON (ds.stationID=s.stationID)
    WHERE (e.eventID='{0}' AND e.antennaset= 'LBA_OUTER' AND (s.status='GOOD') AND (p.direction ='xyz')) """.format(ev))


    power = []
    noise = []
    stations = []
    nStations=0
    for h in c.fetchall():

        powe = crdb.unpickle_parameter(h[0])
        noi = crdb.unpickle_parameter(h[1])
        station = h[2]

        power.append(powe)
        noise.append(noi)
        stations.append(station)
        print '   - {0}'.format(station)
        nStations=nStations+1
    
    if nStations>1:
        results=open('power/power_'+str(ev)+'.p','w')
        info={'stations':stations,'power':power,'noise':noise}
        cPickle.dump(info,results)
        results.close()


#power = np.vstack(power)
#noise = np.vstack(noise)
'''
results2 = open('energy_snr.txt','w')

'''







