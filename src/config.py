import yaml
from pathlib import Path


class Config:
    def __init__(self, config_path: Path):
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)

        self.PROJECTDIR = config_path.parent
        self.PROJECTNAME = self.PROJECTDIR / config_data['project_name']
        self.PROJECTVERSION = self.PROJECTDIR / config_data['version']

        self.RAWDATADIR = self.PROJECTDIR / config_data['data']['raw']
        self.PROCESSEDDATADIR = self.PROJECTDIR / config_data['data']['processed']
        self.MODELDIR = self.PROJECTDIR / config_data['output']['model_save_path']

        self.MODEL = config_data['model']

def load_config():
    project_dir = Path(__file__).resolve().parent.parent
    config_path = project_dir / "configuration.yaml"
    return Config(config_path)

