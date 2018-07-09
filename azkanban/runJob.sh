#!/bin/bash

cd /project/path/
source venv/bin/activate

python $1 $2

deactivate
