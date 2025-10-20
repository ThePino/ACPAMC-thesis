from enum import Enum
from typing import Dict
from pydantic import BaseModel, RootModel, ConfigDict

# ----- Enums for type-safe keys -----
class ClassName(str, Enum):
    malware = "malware"
    backdoor = "backdoor"
    downloader = "downloader"
    trojan = "trojan"
    virus = "virus"
    packed = "packed"
    worm = "worm"
    goodware = "goodware"
    adware = "adware"
    spyware = "spyware"
    dropper = "dropper"
    
class DatasetName(str, Enum):
    apimds = "apimds"
    octak = "octak"
    mpasco = "mpasco"
    quovadis = "quovadis"

class ClassifierName(str, Enum):
    XGBoost = "XGBoost"
    RandomForest = "RandomForest"

# ----- Models -----
class ClassCounts(BaseModel):
    test: int
    eval: int
    model_config = ConfigDict(extra="forbid")

class ClassMetrics(BaseModel):
    precision: float
    recall: float
    f1_score: float
    model_config = ConfigDict(extra="forbid")

class Aggregates(BaseModel):
    micro: ClassMetrics
    macro: ClassMetrics
    model_config = ConfigDict(extra="forbid")

class ConfusionMatrix(BaseModel):
    classes: list[ClassName]
    matrix: list[list[int]]  # entrambe obbligatorie


class Classifier(BaseModel):
    classes: Dict[ClassName, ClassMetrics]
    confusion_matrix: ConfusionMatrix
    aggregates: Aggregates
    global_accuracy: float
    model_config = ConfigDict(extra="forbid")

class DatasetEntry(BaseModel):
    classes: Dict[ClassName, ClassCounts]  # Optional keys allowed
    classifiers: Dict[ClassifierName, Classifier]
    model_config = ConfigDict(extra="forbid")

# ----- Root model -----
class Datasets(RootModel[Dict[DatasetName, DatasetEntry]]):
    pass