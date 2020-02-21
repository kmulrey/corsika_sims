#! /bin/bash

export LOFARSOFT=/vol/optcoma/pycrtools/
source $LOFARSOFT/setenv.sh

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

python getCR_events_coma.py -n 48361669 -s CS003
python getCR_events_coma.py -n 98812643 -s CS003
python getCR_events_coma.py -n 118956923 -s CS003
python getCR_events_coma.py -n 123314680 -s CS003
python getCR_events_coma.py -n 87301753 -s CS003
python getCR_events_coma.py -n 66011236 -s CS003
python getCR_events_coma.py -n 92380604 -s CS003
python getCR_events_coma.py -n 95166806 -s CS003
python getCR_events_coma.py -n 95228015 -s CS003




