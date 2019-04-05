# Evaluates 2016 data using saved model.

import numpy as np
import processData
import csv

from keras.models import load_model

x = np.load("../model/2016_x.npy")

y = np.load("../model/2016_y.npy")

ids = processData.getIDs(ID_PATH = "../model/2016_ids.csv")

model = load_model("../model/2016_2017_model.h5")

y_pred = model.predict(x)

processData.writeData(ids, y, y_pred, SAVE = "../csvs/2016_predictions.csv")

cm, precision, recall, f1 = processData.getConfusion(y, y_pred, val = 0.5)

print("Confusion matrix:")
print(cm)
print()
print("Precision: " + str(precision))
print("Recall: " + str(recall))
print("F1: " + str(f1))

np.save("../model/2016_y_pred.npy", y_pred)
