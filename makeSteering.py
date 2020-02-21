import numpy as np
from optparse import OptionParser
import os
import cPickle
import os.path
import matplotlib.pyplot as plt
import scipy.interpolate as intp
from scipy.interpolate import interp1d
from matplotlib import cm

#event_no=118956923   # outer
#event_no=160673071  # outer
#event_no=66011236   # inner
#event_no=92380604   # outer


#event_no=95228015


parser = OptionParser()
parser.add_option('-n', '--event', default ='95228015', help = 'event number')
parser.add_option('-d', '--dir', default ='.', help = 'output directory')

(options, args) = parser.parse_args()

event_no=str(options.event)
out_directory=str(options.dir)

fname='station_info/stations_'+event_no+'.txt'

with open(fname) as f:
    stations = f.read().splitlines()

sim_file=open('/vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/make_sims/best_sim_files.txt')

file_path=''
best_sim=''

##### find path to relevant input file

with sim_file as f:
    for line in f:
        content = line.split()
        if content[0]==str(event_no):
            file_path=content[1]
            best_sim=content[2]

# temp
#file_path=''


##### change user and directory and make new input file

inputname=file_path+'steering/'+'RUN'+best_sim+'.inp'


inpfile=open(inputname)
#inpfile=open('RUN000023.inp')

new_inp=open(out_directory+'RUN'+best_sim+'.inp','w')
new_scratch='/scratch/kmulrey/'+str(event_no)+'/'+best_sim+'/'

with inpfile as f:
    for line in f:
        content = line.strip()#.split()
        parts=content.split()
        if parts[0]=='USER':
            newline='USER   kmulrey'
            new_inp.write(newline)
            new_inp.write('\n')
        elif parts[0]=='DIRECT':
            newline=new_scratch
            new_inp.write('DIRECT  ')
            new_inp.write(newline)
            new_inp.write('\n')
        
        else:
            new_inp.write(content)
            new_inp.write('\n')

new_inp.close()


################## find core info from fit

fitfile=open('/vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/make_sims/CR_event_info.txt')
info=np.genfromtxt(fitfile)
fitfile.close()

event_number=info.T[0].astype(int)

index=event_number.tolist().index(int(event_no))

core_x_fit=info[index][2]
core_y_fit=info[index][3]


print '{0}  {1}'.format(core_x_fit,core_y_fit)
#### find antenna positions

simfile=open(out_directory+'/SIM'+best_sim+'.list','w')

for s in np.arange(len(stations)):
    
    station_name=stations[s]


    dbFile=open('info/info_'+str(int(event_no))+'_'+station_name+'.dat')

    core_x, core_y , stname, positions_station, dist, x_err, signals, power11, power21, power41, rms, noisepower, time, lora_x, lora_y, lora_dens, azimuth, elevation, elevation_lora, files=cPickle.load(dbFile)
    dbFile.close()

    ##### make SIM.list file


    #antenna_dir='/Users/kmulrey/LOFAR/calibration/cal_final/data/sims/corsika/antenna_positions/'


    new_x=100.0*(positions_station.T[1]-core_y_fit)
    new_y=-100.0*(positions_station.T[0]-core_x_fit)
    new_z=760.0
    for j in np.arange(len(new_x)):
        if j%2==0:
            name=station_name+'_'+str(j+1)
            simfile.write('AntennaPosition = {0} {1} 760.0 {2}\n'.format(new_x[j], new_y[j], name))


simfile.close()



