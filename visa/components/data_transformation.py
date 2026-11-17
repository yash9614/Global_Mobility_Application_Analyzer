from visa.entity.artifact_entity import DataTransformationArtifact

class DataTransformation:
    def initiate_data_transformation(self):
        print("Data transformation started")
        return DataTransformationArtifact(
            transformed_object_file_path="artifact/preprocessor.pkl",
            transformed_train_file_path="artifact/train_transformed.csv",
            transformed_test_file_path="artifact/test_transformed.csv"
        )
