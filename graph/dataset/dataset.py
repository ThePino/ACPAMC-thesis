import json
from pathlib import Path
from model import Datasets, DatasetName, DatasetEntry, ClassifierName
import matplotlib.pyplot as plt
from enum import Enum
import numpy as np

class MediaOutput(str, Enum):
    png = "png"
    svg = 'svg'


CLASS_COLORS = {
    "goodware": "#1b9e77",    # Verde Smeraldo (Benigno)
    "malware": "#d95f02",     # Arancione Bruciato (Categoria Generale)
    "trojan": "#e7298a",      # Magenta Intenso (Priorità Alta)
    "virus": "#7570b3",       # Blu-Viola
    "backdoor": "#e6ab02",    # Giallo Ocra
    "downloader": "#66a61e",  # Verde Oliva Scuro
    "dropper": "#a6761d",     # Marrone Oro
    "spyware": "#666666",     # Grigio Ardesia
    "adware": "#a6cee3",      # Azzurro Chiaro
    "packed": "#fb9a99",      # Rosa Salmone
    "worm": "#cab2d6",        # Viola Lavanda
}

def print_graph_on_size(dataset: DatasetEntry, dataset_name: DatasetName, output_folder: Path, ext: MediaOutput):
    classes = list(dataset.classes.keys())
    test = [dataset.classes[c].test for c in classes]
    eval = [dataset.classes[c].eval for c in classes]
    total = [test[i] + eval[i] for i in range(len(classes))]
    x = range(len(classes))
    width = 0.25

    plt.figure(figsize=(10,6))
    plt.bar(x, total, width=width, label="Totali", color="#1f77b4")
    plt.bar([i + width for i in x], test, width=width, label="Test", color="#ff7f0e")
    plt.bar([i + width*2 for i in x], eval, width=width, label="Training", color="#2ca02c")

    plt.xticks([i + width for i in x], list( map(lambda x : x._value_,classes)), rotation=45)
    plt.ylabel("Numero di istanze")
    plt.title("")
    plt.legend()
    plt.tight_layout()

    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, height + 5, str(height), ha='center', va='bottom', fontsize=9)

    bars_total = plt.bar(x, total, width=width, label="Totali", color="#1f77b4")
    bars_test = plt.bar([i + width for i in x], test, width=width, label="Test", color="#ff7f0e")
    bars_eval = plt.bar([i + width*2 for i in x], eval, width=width, label="Training", color="#2ca02c")
    add_labels(bars_total)
    add_labels(bars_test)
    add_labels(bars_eval)

    output_path =  output_folder / (dataset_name._value_ + f'-class-distribution.{ext._value_}')
    plt.savefig(output_path, dpi=300)  # Salva ad alta risoluzione
    plt.close() 

def plot_class_metrics(dataset_name: DatasetName, data: Datasets):
    dataset = data.root[dataset_name]

    # Itera sui classificatori
    for clf_name, clf_data in dataset.classifiers.items():
        classes = list(clf_data.classes.keys())
        classes.sort()
        
        precision = [clf_data.classes[c].precision for c in classes]
        recall = [clf_data.classes[c].recall for c in classes]
        f1 = [clf_data.classes[c].f1_score for c in classes]

        x = range(len(classes))
        width = 0.25

        plt.figure(figsize=(12,6))
        bars_precision = plt.bar(x, precision, width=width, label="Precision", color="#1f77b4")
        bars_recall = plt.bar([i + width for i in x], recall, width=width, label="Recall", color="#ff7f0e")
        bars_f1 = plt.bar([i + width*2 for i in x], f1, width=width, label="F1 Score", color="#2ca02c")

        plt.xticks([i + width for i in x], [c.value for c in classes], rotation=45)
        plt.ylim(0, 1.05)
        plt.ylabel("Score")
        plt.title("")
        plt.legend()
        plt.tight_layout()

        # Aggiungi valori sopra le barre
        def add_labels(bars):
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, height + 0.02, f"{height:.2f}",
                         ha='center', va='bottom', fontsize=9)

        add_labels(bars_precision)
        add_labels(bars_recall)
        add_labels(bars_f1)

        # Salva su disco
        output_file = Path(__file__).resolve().parent / f"{dataset_name.value}_{clf_name.value}_class_metrics.png"
        plt.savefig(output_file, dpi=300)
        plt.close()
        print(f"Grafico salvato in: {output_file}")

def plot_aggregates(dataset_name: DatasetName, data: Datasets):
    dataset = data.root[dataset_name]

    # Itera sui classificatori
    for clf_name, clf_data in dataset.classifiers.items():
        for agg_type in ["micro", "macro"]:
            aggregates = getattr(clf_data.aggregates, agg_type)
            metrics = ["precision", "recall", "f1_score"]
            values = [getattr(aggregates, m) for m in metrics]

            x = range(len(metrics))
            width = 0.5

            plt.figure(figsize=(6,4))
            bars = plt.bar(x, values, width=width, color=["#1f77b4","#ff7f0e","#2ca02c"])
            plt.xticks(x, ["Precision", "Recall", "F1"])
            plt.ylim(0,1.05)
            plt.ylabel("Score")
            plt.title(f"{clf_name.value} - {agg_type.capitalize()} Aggregates")
            plt.tight_layout()

            # Aggiungi valori sopra le barre
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, height + 0.02, f"{height:.3f}",
                         ha='center', va='bottom', fontsize=9)

            # Salva grafico
            output_file = Path(__file__).resolve().parent / f"{dataset_name.value}_{clf_name.value}_{agg_type}_aggregates.png"
            plt.savefig(output_file, dpi=300)
            plt.close()
            print(f"Grafico salvato in: {output_file}")

def print_cake(dataset: DatasetEntry, dataset_name: DatasetName, output_folder: Path, ext: MediaOutput):
    classes = list(dataset.classes.keys())

    train_vals = [dataset.classes[clx].test for clx in classes]
    eval_vals = [dataset.classes[clx].test for clx in classes]
    sizes = [train_vals[i] + eval_vals[i] for i in range(0, len(classes))]
    fig, ax = plt.subplots(figsize=(5, 5))
    colors = [CLASS_COLORS[clx] for clx in classes]
    ax.pie(
     sizes,
     labels=list(map(lambda x : x.name, classes)),
        autopct='%1.1f%%',
        startangle=90,
        colors=colors
    ) 
    ax.set_title("")
    output = output_folder / f"{dataset_name.value}-class_distribution.{ext.value}"
    # Salva il grafico su file (es. SVG con sfondo trasparente)
    plt.savefig(output, format=ext.value, transparent=True, bbox_inches="tight")
    # Chiudi la figura per evitare sovrapposizioni in loop multipli
    plt.close(fig)
    pass

def print_graph_metrics(dataset: DatasetEntry, dataset_name: DatasetName, output_folder: Path, ext: MediaOutput):
    classes = list(dataset.classes.keys())
    class_labels = [c.value for c in classes]
    x = np.arange(len(classes))  # per gestire bene i bar offset

    fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharey=True)
    width = 0.25

    for index, classifier in enumerate(ClassifierName):
        precision, recall, f1 = [], [], []
        for clx in classes:
            data = dataset.classifiers[classifier].classes[clx]
            precision.append(data.precision)
            recall.append(data.recall)
            f1.append(data.f1_score)

        ax = axes[index]
        ax.bar(x - width, precision, width, label="Precision")
        ax.bar(x, recall, width, label="Recall")
        ax.bar(x + width, f1, width, label="F1-Score")

        ax.set_title(f"{dataset_name.value} - {classifier.name}")
        ax.set_xticks(x)
        ax.set_xticklabels(class_labels, rotation=45)
        ax.set_ylim(0, 1)

        if index == 0:
            ax.set_ylabel("Score")

    fig.suptitle("Confronto per classe: Precision, Recall e F1-score", fontsize=14)
    fig.legend(["Precision", "Recall", "F1-Score"], loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.03))
    fig.tight_layout(rect=[0, 0.05, 1, 0.95])

    output = output_folder / f"{dataset_name.value}-metrics-class.{ext.value}"
    plt.savefig(output, format=ext.value, transparent=True, bbox_inches="tight")
    plt.close(fig)

def main():
    with open(Path(__file__).resolve().parent / 'data.json') as f:
        raw = json.load(f)

    output_dir = Path(__file__).parent / "output"
    datasets = Datasets.model_validate(raw).root

    for dataset in DatasetName:
        #print_graph_on_size(datasets[dataset.name], dataset, output_dir, MediaOutput.svg)
        #print_cake(datasets[dataset.name], dataset, output_dir, MediaOutput.svg)
        print_graph_metrics(datasets[dataset.name], dataset, output_dir, MediaOutput.svg)
    return


if __name__ == "__main__":
    main()