import numpy as np
from optparse import OptionParser
import os
import cPickle
import os.path


path = 'jobs/'
files_all = os.listdir(path)

files = [i for i in files_all if i.endswith('coreas.sh')]

shFile=open('jobs/run_jobs.sh','w')

shFile.write('#! /bin/bash \n')
shFile.write('#SBATCH --time=15-00:00:00\n')
shFile.write('#SBATCH --output=/vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/output/ \n')


for e in np.arange(len(files)):

    shFile.write('sbatch -p long {0}\n'.format(files[e]))

shFile.close()








