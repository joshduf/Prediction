# Creates and saves numpy vectors for model.
# Warning: this takes a full day to run.

import processData

processData.createEvaluateArrays(PATHS = ["../csvs/2017_partial_ht_content.csv"],  ID_INDEX = 0,
                                 TEXT_INDEX = 1, Y_INDEX = 2, MAX_FIELD = 2000,
                                 X_SAVE = "../model/2017_x.npy", Y_SAVE = "../model/2017_y.npy", ID_SAVE = "../model/2017_ids.csv")
