from pathlib import Path


class Config:
    WEIGHT_PATH = Path("./weights")
    WEIGHT_PATH.mkdir(parents=True, exist_ok=True)
    SCALER_PATH = WEIGHT_PATH / "scalers"
    MODEL_PATH = WEIGHT_PATH / "models"
