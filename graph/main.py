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

def plot_class_metrics(dataset_name: DatasetName, data: Datasets):
    dataset = data.root[dataset_name]

    # Itera sui classificatori
    for clf_name, clf_data in dataset.classifiers.items():
        classes = list(clf_data.classes.keys())
        
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
        plt.title(f"Metrics per classe - {clf_name.value}")
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

def main():
    with open(Path(__file__).resolve().parent / 'data.json') as f:
        raw = json.load(f)

    datasets = Datasets.model_validate(raw)
    
    # print_graph_on_size(DatasetName.apimds, datasets)
    # plot_class_metrics(DatasetName.apimds, datasets)
    plot_aggregates(DatasetName.apimds, datasets)
    return


if __name__ == "__main__":
    main()