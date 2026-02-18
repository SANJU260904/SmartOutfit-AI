# scripts/classify_helper.py
import json
from pathlib import Path
import torch
from torchvision import transforms, models
from PIL import Image
import torch.nn as nn

MODEL_PATH = Path("models/garment_classifier.pth")
CLASSES_PATH = Path("models/classes.json")
IMG_SIZE = 224
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

_model = None
_classes = None

def load_classifier():
    global _model, _classes
    if _model is not None:
        return _model, _classes
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Classifier model not found at {MODEL_PATH}. Please run train_classifier.py")
    data = torch.load(str(MODEL_PATH), map_location=device)
    # Try to load classes from saved state or separate json
    if CLASSES_PATH.exists():
        with open(CLASSES_PATH) as f:
            _classes = json.load(f)
    else:
        _classes = data.get("classes", None)
        if _classes is None:
            raise RuntimeError("No classes info found. Re-run training to produce classes.json")

    # build model skeleton
    try:
        backbone = models.mobilenet_v2(weights=None)
        in_features = backbone.classifier[1].in_features
    except Exception:
        backbone = models.mobilenet_v2(pretrained=False)
        in_features = backbone.last_channel

    backbone.classifier = nn.Sequential(nn.Dropout(0.2), nn.Linear(in_features, len(_classes)))
    backbone.load_state_dict(data["state_dict"])
    backbone.to(device)
    backbone.eval()
    _model = backbone
    return _model, _classes

def predict_category(image_path):
    model, classes = load_classifier()
    img = Image.open(image_path).convert("RGB")
    x = _transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        out = model(x)
        _, pred = torch.max(out, 1)
    return classes[pred.item()]
