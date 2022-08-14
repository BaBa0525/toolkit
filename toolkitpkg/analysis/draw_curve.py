import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import precision_recall_curve


def draw_roc(inputFile: str, label: str = 'ROC curve'):
    df = pd.read_csv(inputFile)

    y_test, probas = df['actual'], df['predict']

    # Compute ROC curve and area the curve
    fpr, tpr, _ = roc_curve(y_test, probas)
    roc_auc = auc(fpr, tpr)

    # Plot ROC curve
    plt.plot(fpr, tpr, marker='.', label=f'{label} (auc={roc_auc:0.2f})')
    plt.plot([0, 1], [0, 1], linestyle='--', label='No skill')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")


def draw_pr(inputFile: str, label: str = 'PR curve', no_skill_label: str = 'No skill'):
    df = pd.read_csv(inputFile)

    y_test, probas = df['actual'], df['predict']

    precision, recall, _ = precision_recall_curve(y_test, probas)
    no_skill = len(y_test[y_test==1]) / len(y_test)

    plt.plot(recall, precision, marker='.', label=label)
    plt.plot([0, 1], [no_skill, no_skill], linestyle='--', label=no_skill_label)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc="lower right")

