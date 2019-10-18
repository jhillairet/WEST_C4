# -*- coding: utf-8 -*-
"""
Remote IMAS get

Pass this script the following arguments in a JSON like format:

python save_from_imas.py '{"pulse":55500, "ids_name":"ece", "paths": ["t_e_central.data", "time"]}'

"""
import imas_west
from numpy import savez
import sys
import json

arg = json.loads(sys.argv[1])

imas_obj_fname ='tmp_imas_data.npz'

print(f"Getting IMAS IDS {arg['ids_name']}...")
ids = imas_west.get(int(arg['pulse']), arg['ids_name'])

data = []
for path in arg['paths']:
    print(f"Getting IMAS data {path}...")
    data.append(eval(f"ids.{path}"))

print(f'Saving IMAS object into: {imas_obj_fname}...')
savez(imas_obj_fname, data=data)
