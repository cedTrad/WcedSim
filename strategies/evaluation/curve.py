
import numpy as np
import pandas as pd
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt

def learningCurve(model, X, y, cv, score):
    N, train_score, val_score = learning_curve(model, X, y,
                                           cv = cv, scoring = score,
                                           train_sizes = np.linspace(0.1, 1, 10))
    
    train_scores_mean = train_score.mean(axis = 1)
    train_scores_std = train_score.std(axis = 1)
    
    val_scores_mean = val_score.mean(axis = 1)
    val_scores_std = val_score.std(axis = 1)
    
    plt.figure(figsize = (18, 10))
    
    lw = 2
    plt.semilogx(
        N, train_scores_mean, label="Training score", color="darkorange", lw=lw
    )
    plt.fill_between(
        N,
        train_scores_mean - train_scores_std,
        train_scores_mean + train_scores_std,
        alpha=0.2,
        color="darkorange",
        lw=lw,
    )
    plt.semilogx(
        N, val_scores_mean, label="Cross-validation score", color="navy", lw=lw
    )
    plt.fill_between(
        N,
        val_scores_mean - val_scores_std,
        val_scores_mean + val_scores_std,
        alpha=0.2,
        color="navy",
        lw=lw,
    )
    plt.legend(loc="best")
    plt.show()
    
    return N, train_score, val_score
