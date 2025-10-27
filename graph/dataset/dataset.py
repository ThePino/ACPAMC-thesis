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

def print_graph_metrics(dataset: DatasetEntry, dataset_name: DatasetName, output_folder: Path, ext: MediaOutput):
    """
    Stampa affiancate le matrici di confusione per ciascun classificatore.
    Usa solo Matplotlib.
    """
    classifiers = list(dataset.classifiers.keys())
    n = len(classifiers)
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 5))

    if n == 1:
        axes = [axes]

    for i, classifier in enumerate(classifiers):
        ax = axes[i]
        clf_data = dataset.classifiers[classifier]

        # Estraggo la matrice e le classi (dal tuo oggetto personalizzato)
        matrix = np.array(clf_data.confusion_matrix.matrix)
        classes = [c.value for c in clf_data.confusion_matrix.classes]

        im = ax.imshow(matrix, cmap="Blues")
        ax.set_title(f"{classifier.name}")
        ax.set_xticks(np.arange(len(classes)))
        ax.set_yticks(np.arange(len(classes)))
        ax.set_xticklabels(classes, rotation=45, ha="right")
        ax.set_yticklabels(classes)
        ax.set_xlabel("Predetto")
        ax.set_ylabel("Reale")

        # Valori numerici al centro di ogni cella
        for x in range(len(classes)):
            for y in range(len(classes)):
                ax.text(y, x, matrix[x, y], ha="center", va="center", color="black", fontsize=8)

    fig.tight_layout()

    # Percorso di output
    output = output_folder / f"{dataset_name.value}-confusion-matrix.{ext.value}"
    plt.savefig(output, format=ext.value, bbox_inches="tight", transparent=True)
    plt.close(fig)

def print_class_metrics(dataset: DatasetEntry, dataset_name: DatasetName, output_folder: Path, ext: MediaOutput):
    """
    Genera un grafico per ciascuna metrica (F1-score, Precision, Recall)
    per ogni classificatore del dataset, con legenda sotto.
    """

    metrics = {
        "f1_score": "F1-score",
        "precision": "Precision",
        "recall": "Recall"
    }

    for metric_key, metric_name in metrics.items():
        for classifier, classifier_data in dataset.classifiers.items():
            data = classifier_data.classes
            classes_keys = list(data.keys())
            values = [getattr(data[clx], metric_key) for clx in classes_keys]

            fig, ax = plt.subplots(figsize=(8, 6))
            x = np.arange(len(classes_keys))
            bars = ax.bar(x, values, color="steelblue", label=metric_name)

            # valori sopra le barre
            for bar in bars:
                y = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    y + 0.01,
                    f"{y:.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=8
                )

            ax.set_title(f"{classifier.name}")
            ax.set_xlabel("Classi")
            ax.set_ylabel(metric_name)
            ax.set_xticks(x)
            ax.set_xticklabels([clx.value for clx in classes_keys], rotation=45, ha="right")
            ax.set_ylim(0, 1.1)   
           
            fig.tight_layout(rect=[0, 0.08, 1, 0.95])  # spazio per la legenda

            # nome file di output
            output = output_folder / f"{dataset_name.value}-{classifier.name}-{metric_key}.{ext.value}"
            plt.savefig(output, format=ext.value, bbox_inches="tight", transparent=True)
            plt.close(fig)


def print_global_metrics(dataset: DatasetEntry, dataset_name: DatasetName, output_folder: Path, ext: MediaOutput):
    classifiers = list(dataset.classifiers.keys())
    n = len(classifiers)

    # Imposto la figura: una barra per ogni metrica, per ogni classificatore
    fig, ax = plt.subplots(figsize=(7, 6))

    metrics_names = [
        "Overall Accuracy",
        "Micro Precision", "Micro Recall", "Micro F1-score",
        "Macro Precision", "Macro Recall", "Macro F1-score"
    ]

    # Raccolgo i valori per ogni classificatore
    all_values = []
    for classifier in classifiers:
        metrics = dataset.classifiers[classifier]
        all_values.append([
            metrics.global_accuracy,
            metrics.aggregates.micro.precision, metrics.aggregates.micro.recall, metrics.aggregates.micro.f1_score,
            metrics.aggregates.macro.precision, metrics.aggregates.macro.recall, metrics.aggregates.macro.f1_score
        ])

    all_values = np.array(all_values)
    x = np.arange(len(metrics_names))
    width = 0.35

    # Disegno le barre affiancate per i classificatori
    for i, classifier in enumerate(classifiers):
        ax.bar(
            x + i * width,
            all_values[i],
            width=width,
            label=classifier.name
        )

    # Etichette e legenda
    ax.set_title("")
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(metrics_names, rotation=30, ha='right')
    ax.set_ylabel("Valore")
    
    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.15),
        ncol=n,  # una colonna per ogni classificatore
        frameon=False
    )

    # Mostro i valori sopra le barre
    for i, classifier in enumerate(classifiers):
        for j, v in enumerate(all_values[i]):
            ax.text(x[j] + i * width, v + 0.005, f"{v:.2f}", ha='center', va='bottom', fontsize=8)


    fig.tight_layout()

    # Percorso di output
    output = output_folder / f"{dataset_name.value}-global-metrics.{ext.value}"
    plt.savefig(output, format=ext.value, bbox_inches="tight", transparent=True)
    plt.close(fig)

def main():
    with open(Path(__file__).resolve().parent / 'data.json') as f:
        raw = json.load(f)

    output_dir = Path(__file__).parent / "output"
    datasets = Datasets.model_validate(raw).root

    for dataset in DatasetName:
        print("dataset ", dataset, "in")
        #print_graph_on_size(datasets[dataset.name], dataset, output_dir, MediaOutput.svg)
        #print_cake(datasets[dataset.name], dataset, output_dir, MediaOutput.svg)
        #print_graph_metrics(datasets[dataset.name], dataset, output_dir, MediaOutput.svg)
        #print_class_metrics(datasets[dataset.name], dataset, output_dir, MediaOutput.svg)
        print_global_metrics(datasets[dataset.name], dataset, output_dir, MediaOutput.svg)
        print("dataset ", dataset, "ok")
    return


if __name__ == "__main__":
    main()