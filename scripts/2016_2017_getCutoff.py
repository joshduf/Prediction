import numpy as np
import sklearn.metrics as metrics

y_val = np.load("../model/2016_2017_model_y_valid.npy")
preds = np.load("../model/2016_2017_model_y_valid_pred.npy")

fpr, tpr, thresholds = metrics.roc_curve(y_val,preds)

from tqdm import tqdm_notebook as tqdm
score = 'f1'
scorer = getattr(metrics, f'{score}_score')

score_ls = []
for ii, thres in tqdm(enumerate(thresholds), total=len(thresholds)):
    y_pred = np.where(preds>thres,1,0)
    # Apply desired utility function to y_preds, for example accuracy.
    score_ls.append(scorer(y_val, y_pred, pos_label=1))

roc_auc = metrics.roc_auc_score(y_val, preds)

max_score = max(score_ls)
max_index = score_ls.index(max_score)
max_score_thresh = thresholds[max_index]

from sklearn.metrics import classification_report
print(f'Max {score.upper()} Score: {np.round(max_score,2)}, Cutoff: {np.round(max_score_thresh,2)}')
print(f'Classifier ROC-AUC: {np.round(roc_auc,2)}')
preds_cut = preds>max_score_thresh
print(classification_report(y_val, preds_cut))
print(metrics.accuracy_score(y_val, preds_cut))

np.save("../model/2016_2017_model_cutoff.npy", np.round(max_score_thresh,2))
