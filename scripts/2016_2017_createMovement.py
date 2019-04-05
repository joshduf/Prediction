# Using combined csv created by another script, creates a dictionary with the following format:
#     (city, (year, month, day)): (doc id, phone, lat, long)

from collections import defaultdict
import csv
import pickle

def getMovement(pred_value = 0.5):
    ID_INDEX = 0
    PHONE_INDEX = 1
    HT_INDEX = 2
    PRED_INDEX = 3
    YEAR_INDEX = 5
    MONTH_INDEX = 6
    DAY_INDEX = 7
    CITY_INDEX = 8
    STATE_INDEX = 9
    LAT_INDEX = 10
    LONG_INDEX = 11

    PATH = "../csvs/2016_2017_combined.csv"

    move_dict = defaultdict(list)
    move_dict_ht = defaultdict(list)
    move_dict_ht_all = defaultdict(list)
    entryExit_dict = defaultdict(dict)
    entryExit_dict_ht = defaultdict(dict)
    entryExit_dict_ht_all = defaultdict(dict)
    
    with open(PATH, 'r') as datafile:
        reader = csv.reader(datafile, delimiter=',')
        line = next(reader)

        for line in reader:
            doc = line[ID_INDEX]
            phone = line[PHONE_INDEX]
            ht = line[HT_INDEX]
            pred = float(line[PRED_INDEX])
            year = line[YEAR_INDEX]
            month = line[MONTH_INDEX]
            day = line[DAY_INDEX]
            city = line[CITY_INDEX]
            state = line[STATE_INDEX]
            lat = line[LAT_INDEX]
            long = line[LONG_INDEX]
            
            loc = (city, state)
            date = (year, month, day)

            key = (loc, date)
            value = (doc, phone, lat, long)
            
            move_dict[key].append(value)
            
            if ht != "nan":
                ht = int(ht)

            if ht == 1:
                move_dict_ht[key].append(value)

            if pred > pred_value or ht == 1:
                move_dict_ht_all[key].append(value)
            
            if phone == "nan" or year == "nan" or month == "nan" or day == "nan" or city == "NULL" or state == "NULL":
                continue

            if entryExit_dict.get(loc) == None or entryExit_dict[loc].get(phone) == None:
                entryExit_dict[loc][phone] = [date, date]
            elif date < entryExit_dict[loc][phone][0]:
                entryExit_dict[loc][phone][0] = date
            elif date > entryExit_dict[loc][phone][1]:
                entryExit_dict[loc][phone][1] = date

            if ht == 1:
                if entryExit_dict_ht.get(loc) == None or entryExit_dict_ht[loc].get(phone) == None:
                    entryExit_dict_ht[loc][phone] = [date, date]
                elif date < entryExit_dict_ht[loc][phone][0]:
                    entryExit_dict_ht[loc][phone][0] = date
                elif date > entryExit_dict_ht[loc][phone][1]:
                    entryExit_dict_ht[loc][phone][1] = date

            if pred > pred_value or ht == 1:
                if entryExit_dict_ht_all.get(loc) == None or entryExit_dict_ht_all[loc].get(phone) == None:
                    entryExit_dict_ht_all[loc][phone] = [date, date]
                elif date < entryExit_dict_ht_all[loc][phone][0]:
                    entryExit_dict_ht_all[loc][phone][0] = date
                elif date > entryExit_dict_ht_all[loc][phone][1]:
                    entryExit_dict_ht_all[loc][phone][1] = date

    return move_dict, move_dict_ht, move_dict_ht_all, entryExit_dict, entryExit_dict_ht, entryExit_dict_ht_all

def saveMovement(move_dict, SAVE):
    with open(SAVE, 'wb') as savefile:
        pickle.dump(move_dict, savefile, pickle.HIGHEST_PROTOCOL)

move_dict, move_dict_ht, move_dict_ht_all, entryExit_dict, entryExit_dict_ht, entryExit_dict_ht_all = getMovement(pred_value = 0.5)

saveMovement(move_dict, SAVE = "../pickles/2016_2017_movement.pickle")
saveMovement(move_dict_ht, SAVE = "../pickles/2016_2017_movement_ht.pickle")
saveMovement(move_dict_ht_all, SAVE = "../pickles/2016_2017_movement_ht_all.pickle")
saveMovement(entryExit_dict, SAVE = "../pickles/2016_2017_entryExit.pickle")
saveMovement(entryExit_dict_ht, SAVE = "../pickles/2016_2017_entryExit_ht.pickle")
saveMovement(entryExit_dict_ht_all, SAVE = "../pickles/2016_2017_entryExit_ht_all.pickle")
