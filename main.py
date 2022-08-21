from matplotlib import pyplot as plt

from enum import Enum

from utils.csv import read_csv_as_dict, write_csv
from analysis.data_preprocessing.curve_data import extract_field, extract_border_data
from analysis.curves import draw_roc, draw_pr, draw_f1


def data_proc(path: str):
    correctedData = read_csv_as_dict("data/corrected/all-data-corrected.csv", "image")
    firstInference = read_csv_as_dict(f"{path}/first_inference_official.csv", "img")

    commentData = extract_field(
        list(correctedData.values()),
        list(firstInference.values()),
        truthField="isComment",
        predictField="comment",
    )
    externalData = extract_field(
        list(correctedData.values()),
        list(firstInference.values()),
        truthField="isExternal",
        predictField="external",
    )
    borderData = extract_border_data(firstInference, correctedData)

    write_csv(f"{path}/comment.csv", fields=commentData[0].keys(), data=commentData)
    write_csv(f"{path}/external.csv", fields=externalData[0].keys(), data=externalData)
    write_csv(f"{path}/border.csv", fields=borderData[0].keys(), data=borderData)


def draw_combined_curve(drawFunc, category: str, **kwargs):
    plt.clf()
    drawFunc(f"data/official-one/{category}.csv", label="official one", **kwargs)
    drawFunc(f"data/official-two/{category}.csv", label="official two", **kwargs)
    drawFunc(f"data/official-three/{category}.csv", label="official three", **kwargs)
    drawFunc(
        f"data/official-three-last/{category}.csv",
        label="official three last",
        **kwargs,
    )

    figureType = drawFunc.__name__.split("_")[-1]
    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left")

    plt.savefig(
        f"output/{category}/{category}_compared_{figureType}.png",
        bbox_inches="tight",
        pad_inches=0.25,
    )


class Category(Enum):
    BORDER = 0
    COMMENT = 1
    EXTERNAL = 2


def draw_curves(category: Category):
    categories = ["border", "comment", "external"]
    index = category.value
    draw_combined_curve(draw_roc, categories[index])
    draw_combined_curve(draw_pr, categories[index], noSkillLabel="No skill")
    draw_combined_curve(draw_f1, categories[index])


if __name__ == "__main__":

    # data_proc("data/official-one")
    # data_proc("data/official-two")
    # data_proc("data/official-three")
    # data_proc("data/official-three-last")

    draw_curves(Category.BORDER)
    draw_curves(Category.COMMENT)
    draw_curves(Category.EXTERNAL)
