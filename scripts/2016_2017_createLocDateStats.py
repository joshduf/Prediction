# Using combined csv and entryExit_dict created by other scripts, creates a csv with the following format:
#     "city", "state", "year", "month", "day", "non_ht_ads", "ht_ads", "entries", "exits"

from collections import defaultdict
import csv
import pickle
import processData
import sys

def getStats(entryExit_dict, pred_value = 0.5):
    HT_INDEX = 2
    PRED_INDEX = 3
    YEAR_INDEX = 5
    MONTH_INDEX = 6
    DAY_INDEX = 7
    CITY_INDEX = 8
    STATE_INDEX = 9
    
    AD_INDEX = 0
    AD_HT_INDEX = 1
    ENTER_INDEX = 2
    EXIT_INDEX = 3
    SAMEDAY_INDEX = 4

    ENTERDATE_INDEX = 0
    EXITDATE_INDEX = 1

    PATH = "../csvs/2016_2017_combined.csv"

    stats_dict_ht = defaultdict(list)
    stats_dict_ht_all = defaultdict(list)
    
    with open(PATH, 'r') as datafile:
        reader = csv.reader(datafile, delimiter=',')
        line = next(reader)

        for line in reader:
            ht = line[HT_INDEX]
            pred = float(line[PRED_INDEX])
            year = line[YEAR_INDEX]
            month = line[MONTH_INDEX]
            day = line[DAY_INDEX]
            city = line[CITY_INDEX]
            state = line[STATE_INDEX]
            
            loc = (city, state)
            date = (year, month, day)

            key = (loc, date)

            if year == "nan" or month == "nan" or day == "nan" or city == "NULL" or state == "NULL":
                continue
                
            if ht != "nan":
                ht = int(ht)
                
            if stats_dict_ht.get(key) == None:
                stats_dict_ht[key] = [0, 0, 0, 0, 0]

            if stats_dict_ht_all.get(key) == None:
                stats_dict_ht_all[key] = [0, 0, 0, 0, 0]
            
            if ht == 1:
                stats_dict_ht[key][AD_HT_INDEX] += 1
            else:
                stats_dict_ht[key][AD_INDEX] += 1

            if pred > pred_value or ht == 1:
                stats_dict_ht_all[key][AD_HT_INDEX] += 1
            else:
                stats_dict_ht_all[key][AD_INDEX] += 1
    
    for loc, phone_dates_dict in entryExit_dict.items():
        for dates in phone_dates_dict.values():
            entryDate = dates[ENTERDATE_INDEX]
            enterKey = (loc, entryDate)
            stats_dict_ht[enterKey][ENTER_INDEX] += 1
            stats_dict_ht_all[enterKey][ENTER_INDEX] += 1

            exitDate = dates[EXITDATE_INDEX]
            exitKey = (loc, exitDate)
            stats_dict_ht[exitKey][EXIT_INDEX] += 1
            stats_dict_ht_all[exitKey][EXIT_INDEX] += 1
            
            if entryDate == exitDate:
                sameKey = enterKey
                stats_dict_ht[sameKey][SAMEDAY_INDEX] += 1
                stats_dict_ht_all[sameKey][SAMEDAY_INDEX] += 1
                        
    return stats_dict_ht, stats_dict_ht_all

def saveStats(stats_dict, PATH):
    AD_INDEX = 0
    AD_HT_INDEX = 1
    ENTER_INDEX = 2
    EXIT_INDEX = 3
    SAMEDAY_INDEX = 4

    LOC_INDEX = 0
    DATE_INDEX = 1
    
    CITY_INDEX = 0
    STATE_INDEX = 1
    
    YEAR_INDEX = 0
    MONTH_INDEX = 1
    DAY_INDEX = 2
    
    with open(PATH, 'w') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        outline = ["city", "state", "year", "month", "day", "non_ht_ads", "ht_ads", "entries", "exits", "enter_exit_same_day"]
        writer.writerow(outline)
            
        for key, value in stats_dict.items():
            loc = key[LOC_INDEX]
            city = loc[CITY_INDEX]
            state = loc[STATE_INDEX]

            date = key[DATE_INDEX]
            year = date[YEAR_INDEX]
            month = date[MONTH_INDEX]
            day = date[DAY_INDEX]
            
            non_ht_ads = value[AD_INDEX]
            ht_ads = value[AD_HT_INDEX]
            entries = value[ENTER_INDEX]
            exits = value[EXIT_INDEX]
            sameday = value[SAMEDAY_INDEX]

            outline = [city, state, year, month, day, non_ht_ads, ht_ads, entries, exits, sameday]

            writer.writerow(outline)
            
if len(sys.argv) == 2:
    pred_value = float(sys.argv[1])
else:
    pred_value = 0.5

entryExit_dict = processData.getDedupe(PATH = "../pickles/2016_2017_entryExit.pickle")

stats_dict_ht, stats_dict_ht_all = getStats(entryExit_dict, pred_value = pred_value)

saveStats(stats_dict_ht, PATH = "../csvs/2016_2017_locDate_stats_ht.csv")
saveStats(stats_dict_ht_all, PATH = "../csvs/2016_2017_locDate_stats_ht_all.csv")
