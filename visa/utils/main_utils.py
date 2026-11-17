import yaml

def read_yaml_file(file_path: str):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)
