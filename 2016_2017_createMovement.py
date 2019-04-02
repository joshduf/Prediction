# Using combined csv created by another script, creates a dictionary with the following format:
#     (city, (year, month, day)): (doc id, phone, lat, long)

from collections import defaultdict
import csv
import pickle

def getMovement():
    ID_INDEX = 0
    PHONE_INDEX = 1
    YEAR_INDEX = 5
    MONTH_INDEX = 6
    DAY_INDEX = 7
    CITY_INDEX = 8
    LAT_INDEX = 10
    LONG_INDEX = 11

    PATH = "./csvs/2016_2017_combined.csv"

    move_dict = defaultdict(list)
    
    with open(PATH, 'r') as datafile:
        reader = csv.reader(datafile, delimiter=',')
        line = next(reader)

        for line in reader:            
            doc = line[ID_INDEX]
            phone = line[PHONE_INDEX]
            year = line[YEAR_INDEX]
            month = line[MONTH_INDEX]
            day = line[DAY_INDEX]
            city = line[CITY_INDEX]
            lat = line[LAT_INDEX]
            long = line[LONG_INDEX]

            key = (city, (year, month, day))
            value = (doc, phone, lat, long)

            move_dict[key].append(value)
    
    return move_dict

def saveMovement(move_dict):
    SAVE = "./pickles/2016_2017_movement.pickle"
        
    with open(SAVE, 'wb') as savefile:
        pickle.dump(move_dict, savefile, pickle.HIGHEST_PROTOCOL)

move_dict = getMovement()

saveMovement(move_dict)
