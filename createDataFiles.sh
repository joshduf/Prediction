#!/bin/bash

cd scripts

python ./2016_2017_createDicts.py
python ./2016_2017_createCombined.py
python ./2016_2017_createMovement.py
python ./2016_2017_createLocDateStats.py
