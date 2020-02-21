import numpy as np
from optparse import OptionParser
import os
import cPickle
import os.path

events=np.genfromtxt(open('sim_event_list.txt','r')).astype(int)
fname='best_sim_files.txt'
with open(fname) as f:
    
    content = f.read().splitlines()

runnumbers=[]
events_from_files=[]

for i in np.arange(len(content)):
    runnumbers.append(content[i].split()[2])
    events_from_files.append(content[i].split()[0])


if len(events)!=len(runnumbers):
    print 'problem with file lengths'


for e in np.arange(len(events)):
    #for e in np.arange(1):

    if int(events[e])!=int(events_from_files[e]):
        print 'mismatched events'
        continue
    
    event=events[e]
    
    shFile=open('jobs/run'+str(event)+'_coreas.sh','w')

    shFile.write('#! /bin/bash \n')
    shFile.write('#SBATCH --time=15-00:00:00\n')
    #shFile.write('#SBATCH --output=/vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/output/ \n')
    shFile.write('export RUNNR={0} \n'.format(runnumbers[e]))
    shFile.write('export EVTNR={0} \n'.format(events_from_files[e]))
    
    shFile.write('export LOFARSOFT=/vol/optcoma/pycrtools/ \n')
    shFile.write('source $LOFARSOFT/setenv.sh \n')
    shFile.write('export LC_ALL=en_US.UTF-8 \n')
    shFile.write('export LANG=en_US.UTF-8 \n')
    
    shFile.write('export FLUPRO=/vol/optcoma/cr-simulations/fluka64 \n')
    shFile.write('cd /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/make_sims/ \n')
    shFile.write('rm -rf /scratch/kmulrey/$EVTNR/$RUNNR \n')
    shFile.write('mkdir -p /scratch/kmulrey/$EVTNR/$RUNNR \n')
    shFile.write('chmod -R 770 /scratch/kmulrey \n')
    shFile.write('mkdir /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/ \n')
    shFile.write('python makeSteering.py -n $EVTNR -d /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/ \n')
    shFile.write('cp /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/make_sims/SIM.reas /scratch/kmulrey/$EVTNR/$RUNNR/SIM$RUNNR.reas \n')
    shFile.write('cp /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/SIM$RUNNR.list /scratch/kmulrey/$EVTNR/$RUNNR/SIM$RUNNR.list \n')
    shFile.write('cp /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/RUN$RUNNR.inp /scratch/kmulrey/$EVTNR/$RUNNR/RUN$RUNNR.inp \n')
    shFile.write('cd /vol/optcoma/cr-simulations/corsika_production/run \n')
    shFile.write('./corsika76300Linux_QGSII_fluka_thin_conex_coreas < /scratch/kmulrey/$EVTNR/$RUNNR/RUN$RUNNR.inp \n')
    shFile.write('cd /scratch/kmulrey/$EVTNR/$RUNNR \n')
    shFile.write('ls \n')



    shFile.write('mv RUN$RUNNR.inp /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/RUN$RUNNR.inp \n')
    shFile.write('mv *.long /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/ \n')
    shFile.write('mv SIM$RUNNR.reas /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/SIM$RUNNR.reas \n')
    shFile.write('mv SIM$RUNNR.list /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/SIM$RUNNR.list \n')
    shFile.write('mv * /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR \n')
    shFile.write('rm -rf /scratch/kmulrey/$EVTNR/$RUNNR/* \n')





    shFile.close()











