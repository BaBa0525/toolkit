from toolkitpkg.csvops import read_csv_as_dict, write_csv
from toolkitpkg.analysis.extract_curve_data import extract_field, process_border
from toolkitpkg.analysis.draw_curve import draw_roc, draw_pr
from matplotlib import pyplot as plt

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
    draw_pr(f'testing-data/official-one/{categories[index]}.csv', label='official one', no_skill_label='No skill one')
    draw_pr(f'testing-data/official-two/{categories[index]}.csv', label='official two', no_skill_label='No skill two')
    plt.savefig(f'output/{categories[index]}/{categories[index]}_compared_pr.png')


    

if __name__ == '__main__':
    data_proc(path='./testing-data/official-one')
    data_proc(path='./testing-data/official-two')
    draw_curve(index=0)
    draw_curve(index=1)
    draw_curve(index=2)
