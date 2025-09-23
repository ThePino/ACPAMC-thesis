import json
from pathlib import Path
from model import Datasets, DatasetName

def main():
    with open(Path(__file__).resolve().parent / 'data.json') as f:
        raw = json.load(f)

    datasets = Datasets.model_validate(raw)
    print(datasets.root[DatasetName.apimds])
    return


if __name__ == "__main__":
    main()