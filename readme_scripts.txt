processData.py
- Data processing helper functions.

2016_preprocessModel.py
- Creates and saves numpy vectors for model from 2016 data.
- Warning: this takes a full day to run.

2017_preprocessModel.py
- Creates and saves numpy vectors for model from 2017 data.
- Warning: this takes a full day to run.

2016_evaluateModel.py
- Evaluates 2016 data using saved model.

2017_evaluateModel.py
- Evaluates 2017 data using saved model.

2016_2017_trainModel.py
- Trains model.
- As written trains on both 2016 and 2017 data.
- Can be adjusted to train on 2016 and test on 2017. Directions are in script.

2016_2017_createDicts.py
- Creates dictionaries to lookup doc data by id.
- Warning: createTimeDict takes a full day to run.

2016_2017_createCombined.py
- Using dictionaries created by createDicts.py, creates a combined csv with the following format:
-     "doc", "phone", "ht", "ht_pred", "year", "datetime", "month", "day", "city", "state", "lat", "long"

2016_2017_createMovement.py
- Using combined csv created by 2016_2017_createCombined.py, creates a dictionary with the following format:
-     (city, (year, month, day)): (doc id, phone, lat, long)
