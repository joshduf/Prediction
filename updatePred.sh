#!/bin/bash

cd scripts
date
python ./2016_2017_createMovement.py $1
date
python ./2016_2017_createLocDateStats.py $1
date
