Work in progress. Research project to identify human trafficking from online ads using temporal CNN and detect movement patterns by human traffickers.

Folders:
    csvs
    - All csv data files.

    model
    - Saved model
    - All saved numpy arrays.
    - 2016_ids.csv, 2017_ids.csv.
    
    notebooks
    - Used for testing.
    
    pickles
    - All saved dictionaries.

    scripts
    - All files run by bash scripts below.

    time
    - Csvs of ["id", "time"]

Files:
    preprocessModel.sh
    - Turns all examples into numpy arrays and saves them.
    - Takes a full day to run.

    trainModel.sh
    - Trains and saves model. Saves predictions as numpy arrays.
    - Takes 2 hours to run.

    evaluateModel.sh
    - Uses model from trainModel and numpy arrays from preprocessModel. Saves numpy arrays of predictions on all examples.
    - Takes 3 hours to run.

    createDataFiles.sh
    - Uses predictions from evaluateModel and creates csvs and pickles.
    - Takes cutoff value as argument, if none supplied python script chooses value.
    - Takes 2 hours to run.

    updatePred.sh
    - Recreates movement pickle and location/date stats using cutoff as argument.
    - Takes 20 minutes to run.
