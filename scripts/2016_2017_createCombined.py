# Using dictionaries created by other scripts, creates a combined csv with the following format:
#     "doc", "phone", "ht", "ht_pred", "year", "datetime", "month", "day", "city", "state", "lat", "long"

import csv
import pickle
import processData

def createCombined(id_ht, id_ht_pred, id_datetime, id_phone):
    ID_INDEX = 0
    LONG_INDEX = -1
    LAT_INDEX = -2
    STATE_INDEX = -5
    CITY_INDEX = -6

    IN_PATH = "../csvs/2016_2017_df.csv"
    OUT_PATH = "../csvs/2016_2017_combined.csv"

    with open(IN_PATH, 'r') as datafile, open(OUT_PATH, 'w') as outfile:
        reader = csv.reader(datafile, delimiter=',')
        next(reader)

        writer = csv.writer(outfile, delimiter=',')
        outline = ["doc", "phone", "ht", "ht_pred", "datetime", "year", "month", "day", "city", "state", "lat", "long"]
        writer.writerow(outline)
            
        for line in reader:                
            doc = line[ID_INDEX].strip()
            long = line[LONG_INDEX].strip()
            lat = line[LAT_INDEX].strip()
            state = line[STATE_INDEX].strip()
            city = line[CITY_INDEX].strip()
            
            ht = id_ht.get(doc, "nan")
            ht_pred = id_ht_pred.get(doc, "nan")
            datetime = id_datetime.get(doc, "nan")
            phone = id_phone.get(doc, "nan")

            if datetime == "nan":
                year = "nan"
                month = "nan"
                day = "nan"
            else:
                year = datetime.year
                month = datetime.month
                day = datetime.day

            outline = [doc, phone, ht, ht_pred, datetime, year, month, day, city, state, lat, long]

            writer.writerow(outline)

id_ht = processData.getDedupe(PATH = "../pickles/2016_2017_id_ht.pickle")

id_ht_pred = processData.getDedupe(PATH = "../pickles/2016_2017_id_ht_pred.pickle")

id_datetime = processData.getDedupe(PATH = "../pickles/2016_2017_id_date.pickle")

id_phone = processData.getDedupe(PATH = "../pickles/2016_2017_dedupe.pickle")

createCombined(id_ht, id_ht_pred, id_datetime, id_phone)
