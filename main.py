import argparse
from src.pipeline import Pipeline

parser = argparse.ArgumentParser()
parser.add_argument("--mode", default="train",
                    choices=["train","predict"])

args = parser.parse_args()

pipeline = Pipeline(mode=args.mode)
pipeline.run()
