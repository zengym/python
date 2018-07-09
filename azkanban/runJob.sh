#!/bin/bash

cd /home/foura/python/userprofile
source venv/bin/activate

python $1 $2

deactivate
