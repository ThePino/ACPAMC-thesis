import json
from pathlib import Path
from model import Datasets, DatasetName
import matplotlib.pyplot as plt

def print_graph_on_size(dataset_name: DatasetName, data: Datasets):
    dataset = data.root[dataset_name]
    classes = list(dataset.classes.keys())
    test = [dataset.classes[c].test for c in classes]
    eval = [dataset.classes[c].eval for c in classes]
    total = [test[i] + eval[i] for i in range(len(classes))]
    x = range(len(classes))
    width = 0.25

    plt.figure(figsize=(10,6))
    plt.bar(x, total, width=width, label="Total", color="#1f77b4")
    plt.bar([i + width for i in x], test, width=width, label="Test", color="#ff7f0e")
    plt.bar([i + width*2 for i in x], eval, width=width, label="Eval", color="#2ca02c")

    plt.xticks([i + width for i in x], list( map(lambda x : x._value_,classes)), rotation=45)
    plt.ylabel("Numero di istanze")
    plt.title("Distribuzione delle classi nel dataset Apimds")
    plt.legend()
    plt.tight_layout()

    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, height + 5, str(height), ha='center', va='bottom', fontsize=9)

    bars_total = plt.bar(x, total, width=width, label="Total", color="#1f77b4")
    bars_test = plt.bar([i + width for i in x], test, width=width, label="Test", color="#ff7f0e")
    bars_eval = plt.bar([i + width*2 for i in x], eval, width=width, label="Eval", color="#2ca02c")
    add_labels(bars_total)
    add_labels(bars_test)
    add_labels(bars_eval)

    output_path =  Path(__file__).resolve().parent / (dataset_name._value_ + '.png')
    plt.savefig(output_path, dpi=300)  # Salva ad alta risoluzione
    plt.close() 


def main():
    with open(Path(__file__).resolve().parent / 'data.json') as f:
        raw = json.load(f)

    datasets = Datasets.model_validate(raw)
    
    print_graph_on_size(DatasetName.apimds, datasets)
    return


if __name__ == "__main__":
    main()