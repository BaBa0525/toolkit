import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.metrics import precision_recall_curve, average_precision_score


def draw_roc(inputFile: str, label: str = "ROC curve"):
    df = pd.read_csv(inputFile)

    y_true, y_pred = df["actual"], df["predict"]

    # Compute ROC curve and area the curve
    fpr, tpr, _ = roc_curve(y_true, y_pred)
    roc_auc = roc_auc_score(y_true, y_pred)

    # Plot ROC curve
    plt.plot(fpr, tpr, marker=".", label=f"{label} (auc={roc_auc:0.2f})")
    plt.plot([0, 1], [0, 1], linestyle="--", label="No skill")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Receiver operating characteristic")


def draw_pr(inputFile: str, label: str = "PR curve", noSkillLabel: str = "No skill"):
    df = pd.read_csv(inputFile)

    y_true, y_pred = df["actual"], df["predict"]

    precision, recall, _ = precision_recall_curve(y_true, y_pred)
    ap = average_precision_score(y_true, y_pred)
    no_skill = len(y_true[y_true == 1]) / len(y_true)

    plt.plot(recall, precision, marker=".", label=f"{label} (ap={ap:0.2f})")
    plt.plot([0, 1], [no_skill, no_skill], linestyle="--", label=noSkillLabel)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision-Recall Curve")


def draw_f1(inputFile: str, label: str):
    df = pd.read_csv(inputFile)

    y_test, probas = df["actual"], df["predict"]

    precision, recall, threshold = precision_recall_curve(y_test, probas)

    numerator = 2 * precision * recall
    denom = precision + recall

    f1_scores = np.divide(
        numerator, denom, out=np.zeros_like(denom), where=(denom != 0)
    )

    index = np.argmax(f1_scores)
    highest_score = f1_scores[index]
    best_threshold = threshold[index]

    plt.plot(threshold, f1_scores[:-1], marker=".", label=label)
    plt.plot(
        [best_threshold, best_threshold],
        [0, 1],
        linestyle="--",
        label=f"thres={best_threshold:.3f} score={highest_score:.3f}",
    )

    plt.xlabel("Threshold")
    plt.ylabel("F1-Score")
    plt.title("F1-Score by Threshold")
