processData.py
- Collection of helper functions.

2016_preprocessModel.py
- Turns all 2016 examples into numpy arrays and saves them.

2017_preprocessModel.py
- Turns all 2017 examples into numpy arrays and saves them.

2016_2017_trainModel.py
- Trains and saves model on 2016 and 2017 data. Saves predictions as numpy arrays.

2016_evaluateModel.py
- Uses model from trainModel and numpy arrays from 2016_preprocessModel.py. Saves numpy arrays of predictions on all examples.

2017_evaluateModel.py
- Uses model from trainModel and numpy arrays from 2017_preprocessModel.py. Saves numpy arrays of predictions on all examples.

2016_2017_createDicts.py
- Creates dictionaries of:
  - id: phone
  - id: ht ground truth
  - id: ht predictions.
- Can create dictionary of id: time but currently commented out. This dictionary takes all day to create.
- Uses supplied cutoff value if provided. Otherwise uses 

2016_2017_createCombined.py
- Creates combined csv of ["doc", "phone", "ht", "ht_pred", "datetime", "year", "month", "day", "city", "state", "lat", "long"]

2016_2017_createMovement.py
- Creates dictionaries of:
  - For all examples - (loc, date): (doc, phone, lat, long)
  - For examples with ground truth label - (loc, date): (doc, phone, lat, long)
  - For examples with either ground truth or predicted positive - (loc, date): (doc, phone, lat, long)
  - For all examples - [loc][phone]: [date, date]
  - For examples with ground truth label - [loc][phone]: [date, date]
  - For examples with either ground truth or predicted positive - [loc][phone]: [date, date]

2016_2017_createLocDateStats.py
- Creates csv of:
  - For examples with ground truth label:
    - ["city", "state", "year", "month", "day", "non_ht_ads", "ht_ads", "entries", "exits", "enter_exit_same_day"]
  - For examples with either ground truth or predicted positive:
    - ["city", "state", "year", "month", "day", "non_ht_ads", "ht_ads", "entries", "exits", "enter_exit_same_day"]
