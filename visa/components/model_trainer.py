from visa.entity.artifact_entity import ModelTrainerArtifact

class ModelTrainer:
    def initiate_model_trainer(self):
        print("Model training started")
        return ModelTrainerArtifact(trained_model_file_path="artifact/model.pkl")
