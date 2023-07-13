from sklearn import metrics

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

from sklearn.metrics import roc_curve
from sklearn.metrics import RocCurveDisplay

from sklearn.metrics import precision_recall_curve
from sklearn.metrics import PrecisionRecallDisplay
import matplotlib.pyplot as plt


class Evaluation:
    
    """ 
    Confusion matrix
    Accuracy
    Precision_recall
    F1-score
    Specificity
    AUC
    ROC
    """
    
    def __init__(self, y_true, y_pred, proba_pred):
        self.y_true = y_true
        self.y_pred = y_pred
        self.proba_pred = proba_pred
    
    def metrics(self):
        accuracy = metrics.accuracy_score(self.y_true, self.y_pred)
        f1 = metrics.f1_score(self.y_true, self.y_pred)
        precision = metrics.precision_score(self.y_true, self.y_pred)
        recall =  metrics.recall_score(self.y_true, self.y_pred)
        auc = metrics.roc_auc_score(self.y_true, self.proba_pred)
        print(f' Accuracy : {accuracy:.2f} \n f1 : {f1:.2f} \n precision : {precision:.2f} \n recall : {recall:.2f} \n AUC : {auc:.2f} ')
    
    def report(self):
        cm = confusion_matrix(self.y_true, self.y_pred)
        cm_n = confusion_matrix(self.y_true, self.y_pred, normalize = 'true')
        
        print(classification_report(self.y_true, self.y_pred))
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 8))
        ConfusionMatrixDisplay(cm).plot(ax = ax1)
        ConfusionMatrixDisplay(cm_n).plot(ax = ax2)

    def roc(self):
        fpr, tpr, seuils = roc_curve(y_true = self.y_true, y_score = self.proba_pred)
        roc_display = RocCurveDisplay(fpr = fpr, tpr = tpr)
        return roc_display
        

    def precision_recall(self):
        prec, recall, _ = precision_recall_curve(y_true = self.y_true, probas_pred = self.proba_pred)
        pr_display = PrecisionRecallDisplay(precision = prec, recall = recall)
        return pr_display
        
        
    def roc_pr(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 8))
        roc_display = self.roc()
        pr_display = self.precision_recall()
        roc_display.plot(ax = ax1)
        pr_display.plot(ax = ax2)
    
    def show(self):
        self.report()
        self.roc_pr()
        