import numpy as np
from optparse import OptionParser
import os
import cPickle
import os.path
import pycrtools as cr
from pycrtools import crdatabase as crdb
from pycrtools.tasks import Task



#working_path='/vol/astro3/lofar/sim/kmulrey/calibration/final/compare/power_comparison/'

parser = OptionParser()
parser.add_option('-i', '--list_id', type='int', help='list ID', default=0)
(options, args) = parser.parse_args()

list_id=int(options.list_id)

sim_list_file=open('xmax_dataset_nop_bias_1e17_1e18.txt','r')
list1=np.genfromtxt(sim_list_file,usecols=(0))


nEvents=len(list1)

ldf_fit_energy=np.zeros([nEvents])
ldf_fit_energy_particle=np.zeros([nEvents])
lora_energy=np.zeros([nEvents])
lora_elevation=np.zeros([nEvents])

dbManager = crdb.CRDatabase(host='coma00.science.ru.nl', user='crdb', password='crdb', dbname='crdb')
db = dbManager.db


for i in np.arange(15):
    event_id=int(list1[i])
    print event_id

    try:
        event = crdb.Event(db = db, id = event_id)

        ldf_fit_energy[i]=event["ldf_fit_energy"]
        ldf_fit_energy_particle[i]=event["ldf_fit_energy_particle"]
        lora_elevation[i]=(90-event["lora_elevation"])*np.pi/180.0
        lora_energy[i]=event["lora_energy"]

    except:
        print '...... no data'

outfile_name='db_energy_info.dat'

analysis_info={'ldf_fit_energy':ldf_fit_energy,'ldf_fit_energy_particle':ldf_fit_energy_particle,'lora_energy':lora_energy,'lora_elevation':lora_elevation}

fout=open(outfile_name,'w')
cPickle.dump(analysis_info,fout)
fout.close()



