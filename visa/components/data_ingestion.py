from visa.entity.config_entity import DataIngestionConfig
from visa.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        print("Data ingestion started")
        # Load from CSV or MongoDB
        return DataIngestionArtifact(
            trained_file_path="artifact/train.csv",
            test_file_path="artifact/test.csv"
        )
