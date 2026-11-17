from visa.entity.artifact_entity import DataValidationArtifact

class DataValidation:
    def initiate_data_validation(self):
        print("Data validation started")
        return DataValidationArtifact(validation_status=True)
