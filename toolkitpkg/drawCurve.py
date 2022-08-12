import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import precision_recall_curve

INDEX = 0
CATEGORIES = ['border', 'comment', 'external']

CATEGORY = CATEGORIES[INDEX]
INPUT_FILE = f'./testing-data/{CATEGORY}.csv'
OUTPUT_ROC = f'./output/{CATEGORY}-roc.png'
OUTPUT_PR = f'./output/{CATEGORY}-pr.png'

def drawROC(inputFile: str, outputFile: str):
    df = pd.read_csv(inputFile)

    y_test, probas = df['actual'], df['predict']

    # Compute ROC curve and area the curve
    fpr, tpr, _ = roc_curve(y_test, probas)
    roc_auc = auc(fpr, tpr)
    print(f"Area under the ROC curve : {roc_auc}")

    # Plot ROC curve
    plt.clf()
    plt.plot(fpr, tpr, marker='.', label=f'ROC curve (area={roc_auc:0.2f})')
    plt.plot([0, 1], [0, 1], linestyle='--', label='No skill')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")

    plt.savefig(outputFile)
    plt.show()


def drawPR(inputFile: str, outputFile: str):
    df = pd.read_csv(inputFile)

    y_test, probas = df['actual'], df['predict']

    precision, recall, _ = precision_recall_curve(y_test, probas)
    no_skill = len(y_test[y_test==1]) / len(y_test)

    plt.clf()
    plt.plot(recall, precision, marker='.', label='PR curve')
    plt.plot([0, 1], [no_skill, no_skill], linestyle='--', label='No skill')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc="lower right")

    plt.savefig(outputFile)
    plt.show()




def main():

    drawROC(INPUT_FILE, OUTPUT_ROC)
    drawPR(INPUT_FILE, OUTPUT_PR)


if __name__ == "__main__":
    main()