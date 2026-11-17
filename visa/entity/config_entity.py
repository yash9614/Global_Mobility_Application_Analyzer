from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    data_path: str = "data/EasyVisa.csv"
    target_column: str = "case_status"

@dataclass
class DataValidationConfig:
    pass

@dataclass
class DataTransformationConfig:
    pass

@dataclass
class ModelTrainerConfig:
    pass
