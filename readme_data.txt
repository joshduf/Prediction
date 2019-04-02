Folders:

    csvs:
        
        2016_2017_combined.csv
            - doc,phone,ht,ht_pred,year,datetime,month,day,city,state,lat,long

        2016_2017_df.csv
            - id,age,call,email,ethnicity,url,location,phone,price_per_hour,tip,phone_2,...,
                 phone_104,ht,ht_all,base,city,state,country,population,latitude,longitude
        
        2016_partial_ht_content.csv
            - doc_id,raw_content_parsed,ht_all
        
        2017_partial_ht_content.csv
            - id,raw_content_parsed,ht_all

        2016_predictions.csv
            - id,ht_actual,ht_predicted
        
        2017_predictions.csv
            - id,ht_actual,ht_predicted

    
    model:
        
        2016_ids.csv
            - List of doc ids, in the same order as 2016_x.npy and 2016_y.npy

        2017_ids.csv
            - List of doc ids, in the same order as 2017_x.npy and 2017_y.npy

        2016_x.npy
            - Preprocessed numpy array representing 2016 raw content
            
        2017_x.npy
            - Preprocessed numpy array representing 2017 raw content
        
        2016_y.npy
            - Trafficking/not-trafficking results for 2016
        
        2017_y.npy
            - Trafficking/not-trafficking results for 2017
        
        2016_2017_model.h5
            - Saved model trained on 2016 and 2017 data
        
        2016_2017_model_results.txt
            - Training results for 2016_2017_model.h5

        2016_2017_accuracy.png
            - Graph of training results for 2016_2017_model.h5

    
    pickles:
        
        2016_2017_dedupe.pickle
            - id: phone
        
        2016_2017_id_ht.pickle
            - id: trafficking/not-trafficking from 2016_2017_df.csv
        
        2016_2017_movement.pickle
            - (city, (year, month, day)): (doc id, phone, lat, long)
        
        2016_2017_id_date.pickle
            - id: datetime object
        
        2016_2017_id_ht_pred.pickle
            - id: predicted trafficking/not-trafficking from evaluating model


    results:
        2016_2017_combined.csv
            - Backup of latest combined csv

        2016_2017_movement.pickle
            - Backup of latest movement pickle

    time: collection of tab separated id,date/time tsvs.

