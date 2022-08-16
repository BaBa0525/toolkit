import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_curve, RocCurveDisplay
from matplotlib import pyplot as plt

from toolkitpkg.csvops import read_csv_as_dict, write_csv
from toolkitpkg.analysis.extract_curve_data import extract_field, process_border
from toolkitpkg.analysis.draw_curve import draw_roc, draw_pr

def data_proc(path: str):
    correctedData = read_csv_as_dict('./testing-data/corrected/all-data-corrected.csv', 'image')
    firstInference = read_csv_as_dict(f'{path}/first_inference_official.csv', 'img')

    commentData = extract_field(list(correctedData.values()), list(firstInference.values()), truthField='isComment', predictField='comment')
    externalData = extract_field(list(correctedData.values()), list(firstInference.values()), truthField='isExternal', predictField='external')
    borderData = process_border(firstInference, correctedData)

    write_csv(f'{path}/comment.csv', fields=commentData[0].keys(), data=commentData)
    write_csv(f'{path}/external.csv', fields=externalData[0].keys(), data=externalData)
    write_csv(f'{path}/border.csv', fields=borderData[0].keys(), data=borderData)

def draw_curve(index: int = 0):
    categories = ['border', 'comment', 'external']
    plt.clf()
    draw_roc(f'testing-data/official-one/{categories[index]}.csv', label='official one')
    draw_roc(f'testing-data/official-two/{categories[index]}.csv', label='official two')
    plt.savefig(f'output/{categories[index]}/{categories[index]}_compared_roc.png')

    plt.clf()
    draw_pr(f'testing-data/official-one/{categories[index]}.csv', label='official one', noSkillLabel='No skill one')
    draw_pr(f'testing-data/official-two/{categories[index]}.csv', label='official two', noSkillLabel='No skill two')
    plt.savefig(f'output/{categories[index]}/{categories[index]}_compared_pr.png')

def draw_f1_fig(path: str, category: str, label: str, offset: tuple = (0, -10)):
    df = pd.read_csv(f'{path}/{category}.csv')

    y_test, probas = df['actual'], df['predict']

    precision, recall, threshold = precision_recall_curve(y_test, probas)

    numerator = 2 * precision * recall
    denom = precision + recall

    f1_scores = np.divide(numerator, denom, out=np.zeros_like(denom), where=(denom != 0))

    index = np.argmax(f1_scores)
    highest_score = f1_scores[index]
    best_threshold = threshold[index]

    plt.plot(threshold, f1_scores[:-1], marker='.', label=label)
    plt.plot([best_threshold, best_threshold], [0, 1], linestyle='--', label=f'thres={best_threshold:.3f} score={highest_score:.3f}')

    plt.xlabel('Threshold')
    plt.ylabel('F1-Score')
    plt.title('F1-Score by Threshold')


if __name__ == '__main__':

    data_proc('testing-data/official-one')
    data_proc('testing-data/official-two')

    draw_curve(0)
    draw_curve(1)
    draw_curve(2)

    # category = 'external'
    
    # plt.clf()
    
    # draw_f1_fig('testing-data/official-one', category=category, label=f'official-one-{category}', offset=(-50, -10))
    # draw_f1_fig('testing-data/official-two', category=category, label=f'official-two-{category}', offset=(5, -30))
    
    # plt.legend(loc='lower left')
    # plt.savefig(f'output/{category}/{category}_f1_by_threshold.png')