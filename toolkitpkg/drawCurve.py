import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

CATEGORY = 'comment'
INPUT_FILE = f'./testing-data/{CATEGORY}.csv'
OUTPUT_FILE = f'./output/{CATEGORY}.png'

def main():
    df = pd.read_csv(INPUT_FILE)

    y_test, probas = df['actual'], df['predict']

    # Compute ROC curve and area the curve
    fpr, tpr, _ = roc_curve(y_test, probas)
    roc_auc = auc(fpr, tpr)
    print(f"Area under the ROC curve : {roc_auc}")

    # Plot ROC curve
    plt.clf()
    plt.plot(fpr, tpr, label=f'ROC curve (area={roc_auc:0.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")

    plt.show()
    plt.savefig(OUTPUT_FILE)


if __name__ == "__main__":
    main()