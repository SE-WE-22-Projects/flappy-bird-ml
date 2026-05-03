from pathlib import Path


def model_dir():
    return (Path(__file__).parent.parent.parent / "models").resolve()
