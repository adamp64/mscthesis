import os
import pandas as pd
from thesis import helper
from thesis import data
from thesis import predictor
from thesis import evaluation as ev

spec = dict()
spec['name'] = os.path.basename(__file__).split('.')[0]

# --------- general configuration ----------
spec['horizons'] = ["1:2"]
spec['folds'] = helper.random_fold2(1)
spec['past_data'] = (1, pd.offsets.Day(1))
spec['errors'] = [ev.error_squared, ev.error_absolute]

# -------- job configuration -----------
weather_data = data.Data.prefetch_data2()
spec['jobs'] = [
    {
        'name': 'time',
        'data': {
            'fun': data.data_wind,
            'extra': {
                'raw_data': weather_data
            }
        },
        'predictor': {
            'fun': predictor.predictor_greedy
        }
    },
    {
        'name': 'persistence',
        'data': {
            'fun': data.data_horizon,
            'extra': {
                'output_feature': 'WindSpd_{Avg}',
                "input_feature": None,
                "l": 1,
                "time_as_feature": False,
                "scale_x": False,
                "scale_y": False,
                "raw_data": weather_data
            }
        },
        'predictor': {
            'fun': predictor.predictor_persistence
        }
    }
]

# -------- end configuration ----------