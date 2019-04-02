# Data processing helper functions

import csv
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys

from keras import regularizers
from keras.layers import Activation, BatchNormalization, Conv1D, Dense, Dropout, Embedding, GlobalMaxPooling1D, MaxPooling1D
from keras.models import Sequential
from keras.preprocessing import sequence
from random import choices
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.utils import shuffle

# Creates dictionary of doc_id: dedupe_id
def createDedupe(DEDUPE_PATHS, ID_INDEX, DEDUPE_INDEX, DEDUPE_SAVE = "./pickles/dedupe.pickle"):
    dedupe_dict = {}
    
    for PATH in DEDUPE_PATHS:
        with open(PATH, 'r') as datafile:
            reader = csv.reader(datafile, delimiter=',')
            next(reader)

            for line in reader:
                doc = line[ID_INDEX]
                phone = line[DEDUPE_INDEX]
                dedupe_dict[doc] = phone

    with open(DEDUPE_SAVE, 'wb') as savefile:
        pickle.dump(dedupe_dict, savefile, pickle.HIGHEST_PROTOCOL)
    
    return dedupe_dict

# Retrieves dictionary of doc_id: dedupe_id
def getDedupe(PATH = "./pickles/dedupe.pickle"):
    with open(PATH, 'rb') as datafile:
        dedupe_dict = pickle.load(datafile)
    
    return dedupe_dict

# Creates and saves numpy arrays for evaluation
def createEvaluateArrays(PATHS, ID_INDEX, TEXT_INDEX, Y_INDEX, MAX_FIELD,
                         X_SAVE = "./model/x.npy", Y_SAVE = "./model/y.npy", ID_SAVE = "./model/ids.csv"):
        
    x, ids, y, total = loadEvaluate(PATHS, ID_INDEX, TEXT_INDEX, MAX_FIELD, Y_INDEX=Y_INDEX)

    (X, Y) = vectorize(x, y)
    
    writeIDs(ID_SAVE, ids)
    np.save(X_SAVE, X)
    np.save(Y_SAVE, Y)

# Saves csv of doc ids
def writeIDs(PATH, ids):
    with open(PATH, 'w') as datafile:
        writer = csv.writer(datafile, delimiter=',')
        writer.writerow(ids)

# Retrieves list of doc ids        
def getIDs(ID_PATH):
    with open(ID_PATH) as datafile:
        csv_reader = csv.reader(datafile, delimiter=',')
        line = next(csv_reader)
        ids = list(line)

    return ids

# Saves predictions to file
def writeData(ids, y, y_pred, SAVE = "./csvs/predictions.csv"):
    with open(SAVE, 'w') as datafile:
        writer = csv.writer(datafile, delimiter=',')
        writer.writerow(["id", "ht_actual", "ht_predicted"])

        for i in range(len(ids)):
            doc = ids[i]
            val = y[i]
            pred = y_pred[i][0]
            writer.writerow([doc, val, '%f' % pred])

# Loads positive and negative examples
def loadXY(PATHS, ID_INDEX, TEXT_INDEX, Y_INDEX, MAX_EXAMPLES, MAX_FIELD):
    csv.field_size_limit(sys.maxsize)

    x = []
    y = []
    pos = 0
    neg = 0
    phones = set()

    for PATH in PATHS:
        with open(PATH, 'r') as datafile:
            reader = csv.reader(datafile, delimiter=',')
            next(reader)
            
            for line in reader:
                doc = line[ID_INDEX]
                text = line[TEXT_INDEX]
                val = int(line[Y_INDEX])
                
                if neg >= MAX_EXAMPLES and pos >= MAX_EXAMPLES:
                    break

                if len(text) > MAX_FIELD:
                    continue
                
                if val == 1 and pos < MAX_EXAMPLES:
                    x.append(text)
                    y.append(val)
                    pos += 1
                elif val == 0 and neg < MAX_EXAMPLES:
                    x.append(text)
                    y.append(val)
                    neg += 1

    return x, y, pos, neg

# Loads positive and negative examples
def loadXYDedupe(PATHS, ID_INDEX, TEXT_INDEX, Y_INDEX, MAX_EXAMPLES, MAX_FIELD, TRAIN_SPLIT, dedupe_dict):
    csv.field_size_limit(sys.maxsize)

    x_train = []
    x_valid = []
    x_test = []
    y_train = []
    y_valid = []
    y_test = []
    dedupe_train = set()
    dedupe_valid = set()
    dedupe_test = set()
    pos = 0
    neg = 0

    for PATH in PATHS:
        with open(PATH, 'r') as datafile:
            reader = csv.reader(datafile, delimiter=',')
            next(reader)
            
            for line in reader:
                doc = line[ID_INDEX]
                text = line[TEXT_INDEX]
                val = int(line[Y_INDEX])
                dedupe_id = dedupe_dict.get(doc, "nan")
                
                population = ["train", "valid", "test"]
                VALID_SPLIT = (1 - TRAIN_SPLIT)/2
                TEST_SPLIT = (1 - TRAIN_SPLIT)/2
                weights = [TRAIN_SPLIT, VALID_SPLIT, TEST_SPLIT]
                choice = choices(population, weights)[0]

                if neg >= MAX_EXAMPLES and pos >= MAX_EXAMPLES:
                    break
                    
                if val == 0 and neg >= MAX_EXAMPLES:
                    continue

                if val == 1 and pos >= MAX_EXAMPLES:
                    continue

                if len(text) > MAX_FIELD:
                    continue
                    
                if val == 0:
                    neg += 1
                else:
                    pos += 1

                if dedupe_id in dedupe_train:
                    x_train.append(text)
                    y_train.append(val)
                elif dedupe_id in dedupe_valid:
                    x_valid.append(text)
                    y_valid.append(val)
                elif dedupe_id in dedupe_test:
                    x_test.append(text)
                    y_test.append(val)
                elif choice == "train":
                    x_train.append(text)
                    y_train.append(val)
                    if dedupe_id != "nan":
                        dedupe_train.add(dedupe_id)
                elif choice == "valid":
                    x_valid.append(text)
                    y_valid.append(val)
                    if dedupe_id != "nan":
                        dedupe_valid.add(dedupe_id)
                else:
                    x_test.append(text)
                    y_test.append(val)
                    if dedupe_id != "nan":
                        dedupe_test.add(dedupe_id)

    return x_train, y_train, x_valid, y_valid, x_test, y_test, pos, neg

# Loads examples to evaluate
def loadEvaluate(PATHS, ID_INDEX, TEXT_INDEX, MAX_FIELD, Y_INDEX):
    csv.field_size_limit(sys.maxsize)

    x = []
    ids = []
    y = []
    total = 0
    
    for PATH in PATHS:
        with open(PATH, 'r') as datafile:
            reader = csv.reader(datafile, delimiter=',')
            next(reader)

            for line in reader:                
                text = line[TEXT_INDEX]
                doc = line[ID_INDEX]

                if len(text) > MAX_FIELD:
                    text = text[:MAX_FIELD]

                x.append(text)
                ids.append(doc)
                
                total += 1
                
    X = pad(x, MAX_FIELD)
    Y = y

    return X, ids, Y, total

# Takes positive and negative examples and creates input and output vectors
def readData(PATHS, ID_INDEX, TEXT_INDEX, Y_INDEX, MAX_EXAMPLES, MAX_FIELD):
    x, y, pos, neg = loadXY(PATHS, ID_INDEX, TEXT_INDEX, Y_INDEX, MAX_EXAMPLES, MAX_FIELD)

    print('Pos size: ' + str(pos))
    print('Neg size: ' + str(neg))

    (X, Y) = vectorize(pad(x, MAX_FIELD), y)
    
    return X, Y

# Same as readData but dedupes based on supplied dictionary
def readDataDedupe(PATHS, ID_INDEX, TEXT_INDEX, Y_INDEX, TRAIN_SPLIT, MAX_EXAMPLES, MAX_FIELD, dedupe_dict):
    x_train, y_train, x_valid, y_valid, x_test, y_test, pos, neg = loadXYDedupe(PATHS, ID_INDEX, TEXT_INDEX, Y_INDEX,
                                                                                MAX_EXAMPLES, MAX_FIELD, TRAIN_SPLIT, dedupe_dict)

    print('Pos size: ' + str(pos))
    print('Neg size: ' + str(neg))
    print('Train size: ' + str(len(y_train)))
    print('Valid size: ' + str(len(y_valid)))
    print('Test size: ' + str(len(y_test)))

    (X_train, Y_train) = vectorize(pad(x_train, MAX_FIELD), y_train)
    (X_valid, Y_valid) = vectorize(pad(x_valid, MAX_FIELD), y_valid)
    (X_test, Y_test) = vectorize(pad(x_test, MAX_FIELD), y_test)

    return (X_train, Y_train), (X_valid, Y_valid), (X_test, Y_test)

# Pads all examples to the length of the longest
def pad(data, size):
    padded = [row.ljust(size, ">") for row in data]
    
    return padded

# Turns character vector into vector of character indexes
def vectorize(x, y):
    Y = np.array(y)
    X = np.array([[ord(letter) for letter in line] for line in x])
    
    return (X, Y)

# Splits data into test and train sections
def splitData(X, Y, SPLITSIZE):
    X, Y = shuffle(X, Y)

    x_train = X[:SPLITSIZE]
    x_test = X[SPLITSIZE:]

    y_train = Y[:SPLITSIZE]
    y_test = Y[SPLITSIZE:]
    
    return (x_train, y_train), (x_test, y_test)

# Creates temporal CNN
def createModel(x_train, x_valid, x_test):
    max_features = max(np.amax(x_train), np.amax(x_valid), np.amax(x_test)) + 1
    embedding_size = 8
    maxlen = len(x_train[0])

    kernel_size = 8
    filters = 64
    pool_size = 4
    dense_layers = 128
    
    model = Sequential()

    model.add(Embedding(max_features, embedding_size, input_length=maxlen))

    model.add(Conv1D(filters, kernel_size*4, padding='valid', strides=1, kernel_regularizer=regularizers.l2(0.01)))
    model.add(BatchNormalization())
    model.add(Dropout(0.4))
    model.add(Activation('relu'))
    model.add(MaxPooling1D(pool_size=pool_size))

    model.add(Conv1D(filters, kernel_size*2, padding='valid', strides=1, kernel_regularizer=regularizers.l2(0.01)))
    model.add(BatchNormalization())
    model.add(Dropout(0.4))
    model.add(Activation('relu'))
    model.add(MaxPooling1D(pool_size=pool_size))

    model.add(Conv1D(filters, kernel_size, padding='valid', strides=1, kernel_regularizer=regularizers.l2(0.01)))
    model.add(BatchNormalization())
    model.add(Dropout(0.4))
    model.add(Activation('relu'))
    model.add(MaxPooling1D(pool_size=pool_size))

    model.add(GlobalMaxPooling1D())

    model.add(Dense(dense_layers, kernel_regularizer=regularizers.l2(0.01)))

    model.add(Dropout(0.4))
    model.add(Activation('relu'))

    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model

# Fits, tests, and saves model
def runModel(model, x_train, y_train, x_valid, y_valid, x_test, y_test, save_name='./model/model.h5'):
    batch_size = 32
    epochs = 3
    
    history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=(x_valid, y_valid))
    score, acc = model.evaluate(x_test, y_test, batch_size=batch_size)
    
    model.save(save_name)
    
    return model, history, score, acc

# Returns confusion matrix
def getConfusion(y_test, y_pred, val = 0.5):
    y_pred_binary = (y_pred > val)
    cm = confusion_matrix(y_test, y_pred_binary)

    tp = cm[1][1]
    tn = cm[0][0]
    fp = cm[0][1]
    fn = cm[1][0]
    
    precision = tp/(tp + fp)
    recall = tp/(tp + fn)
    f1 = (precision*recall)/(precision + recall)

    return cm, precision, recall, f1

# Given history from model, plots accuracy
def getPlot(history, save_name = './model/accuracy.png'):
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validate'], loc='upper left')
    plt.savefig(save_name)
