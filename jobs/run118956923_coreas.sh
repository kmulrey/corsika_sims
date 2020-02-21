#! /bin/bash 
#SBATCH --time=15-00:00:00
export RUNNR=000028 
export EVTNR=118956923 
export LOFARSOFT=/vol/optcoma/pycrtools/ 
source $LOFARSOFT/setenv.sh 
export LC_ALL=en_US.UTF-8 
export LANG=en_US.UTF-8 
export FLUPRO=/vol/optcoma/cr-simulations/fluka64 
cd /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/make_sims/ 
rm -rf /scratch/kmulrey/$EVTNR/$RUNNR 
mkdir -p /scratch/kmulrey/$EVTNR/$RUNNR 
chmod -R 770 /scratch/kmulrey 
mkdir /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/ 
python makeSteering.py -n $EVTNR -d /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/ 
cp /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/make_sims/SIM.reas /scratch/kmulrey/$EVTNR/$RUNNR/SIM$RUNNR.reas 
cp /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/SIM$RUNNR.list /scratch/kmulrey/$EVTNR/$RUNNR/SIM$RUNNR.list 
cp /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/RUN$RUNNR.inp /scratch/kmulrey/$EVTNR/$RUNNR/RUN$RUNNR.inp 
cd /vol/optcoma/cr-simulations/corsika_production/run 
./corsika76300Linux_QGSII_fluka_thin_conex_coreas < /scratch/kmulrey/$EVTNR/$RUNNR/RUN$RUNNR.inp 
cd /scratch/kmulrey/$EVTNR/$RUNNR 
ls 
mv RUN$RUNNR.inp /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/RUN$RUNNR.inp 
mv *.long /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/ 
mv SIM$RUNNR.reas /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/SIM$RUNNR.reas 
mv SIM$RUNNR.list /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR/SIM$RUNNR.list 
mv * /vol/astro3/lofar/sim/kmulrey/calibration/final/compare/sims/corsika/$EVTNR 
rm -rf /scratch/kmulrey/$EVTNR/$RUNNR/* 
