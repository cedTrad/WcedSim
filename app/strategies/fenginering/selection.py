from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import RFE, RFECV

def by_variance(threshold):
    selector = VarianceThreshold(threshold=threshold)


def by_model():
    selector = SelectFromModel(model)


def by_model_():
    selector = SelectFromModel(model)
