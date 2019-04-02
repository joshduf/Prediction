# Trains model.
# As written trains on both 2016 and 2017 data.
# Can be used to train on 2016 and test on 2017 by removing 2017 data from readDataDedupe
#     and uncommenting lines to create the test set using different files

import numpy as np
import processData

dedupe_dict = processData.getDedupe(PATH = "./pickles/2016_2017_dedupe.pickle")

MAX_EXAMPLES = np.sum(np.load("./model/2016_y.npy")) + np.sum(np.load("./model/2017_y.npy"))

(x_train, y_train), (x_valid, y_valid), (x_test, y_test) = processData.readDataDedupe(PATHS = ["./csvs/2016_partial_ht_content.csv",
                                                                                               "./csvs/2017_partial_ht_content.csv"],
                                                                                      ID_INDEX = 0, TEXT_INDEX = 1,
                                                                                      Y_INDEX = 2, TRAIN_SPLIT = 0.9,
                                                                                      MAX_EXAMPLES = MAX_EXAMPLES,
                                                                                      MAX_FIELD = 2000,
                                                                                      dedupe_dict = dedupe_dict)

# To create test set using different files
#MAX_EXAMPLES = np.sum(np.load("./model/2017_y.npy"))

#x_valid = np.concatenate((x_valid, x_test), axis=0)
#y_valid = np.concatenate((y_valid, y_test))

#(x_test, y_test) = processData.readData(PATHS = ["./csvs/2017_partial_ht_content.csv"], ID_INDEX = 0, TEXT_INDEX = 1, Y_INDEX = 2,
#                                        MAX_EXAMPLES = MAX_EXAMPLES, MAX_FIELD = 2000)

model = processData.createModel(x_train, x_valid, x_test)

model, history, score, acc = processData.runModel(model, x_train, y_train, x_valid, y_valid, x_test, y_test,
                                                  save_name="./model/2016_2017_model.h5")

print("History: ", history.history)
print("Test lost:", score)
print("Test accuracy:", acc)

processData.getPlot(history, save_name = "./model/2016_2017_accuracy.png")

y_pred = model.predict(x_test)

cm, precision, recall, f1 = processData.getConfusion(y_test, y_pred, val = 0.5)

print("Confusion matrix:")
print(cm)
print()
print("Precision: " + str(precision))
print("Recall: " + str(recall))
print("F1: " + str(f1))
