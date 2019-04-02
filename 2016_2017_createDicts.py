# Creates dictionaries to lookup doc data by doc ID.
# Warning: createTimeDict takes a full day to run.

import csv
import dask.dataframe as dd
from dateutil import parser
import pickle
import processData

def try_parse(text):
    try:
        parsed = parser.parse(text)
        
        return parsed

    except:

        return "nan"

def createTimeDict():
    TIME_PATH = "./time/*.tsv"
    TIME_SAVE = "./pickles/id_date.pickle"
    
    df = dd.read_csv(TIME_PATH, delimiter='\t', error_bad_lines=False, header=None, names=['ID', 'Date'],
                     encoding='utf8', quoting=csv.QUOTE_NONE)
    pdf = df.compute(error_bad_lines=False, warn_bad_lines=True)
    pdf['Date'] = pdf['Date'].apply(try_parse)
    pdf_dict = pdf.set_index('ID').to_dict()['Date']
    
    with open(TIME_SAVE, 'wb') as savefile:
        pickle.dump(pdf_dict, savefile, pickle.HIGHEST_PROTOCOL)
    
    return pdf_dict

dedupe_dict = processData.createDedupe(DEDUPE_PATHS = ["./csvs/2016_2017_df.csv"],
                                       ID_INDEX=0, DEDUPE_INDEX=9, DEDUPE_SAVE = "./pickles/2016_2017_dedupe.pickle")

id_ht = processData.createDedupe(DEDUPE_PATHS = ["./csvs/2016_predictions.csv", "./csvs/2017_predictions.csv"],
                                 ID_INDEX=0, DEDUPE_INDEX=1, DEDUPE_SAVE = "./pickles/2016_2017_id_ht.pickle")

id_ht_pred = processData.createDedupe(DEDUPE_PATHS = ["./csvs/2016_predictions.csv", "./csvs/2017_predictions.csv"],
                                      ID_INDEX=0, DEDUPE_INDEX=2, DEDUPE_SAVE = "./pickles/2016_2017_id_ht_pred.pickle")

id_time = createTimeDict()
