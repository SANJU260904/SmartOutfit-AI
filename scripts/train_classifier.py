# scripts/train_classifier.py
import os
import json
from pathlib import Path
from torchvision import datasets, transforms, models
import torch
from torch import nn, optim
from torch.utils.data import DataLoader

# === CONFIG ===
DATA_DIR = Path("scripts/dataset_classifier")
SAVE_DIR = Path("models")
SAVE_DIR.mkdir(parents=True, exist_ok=True)
SAVE_PATH = SAVE_DIR / "garment_classifier.pth"
CLASSES_PATH = SAVE_DIR / "classes.json"

BATCH_SIZE = 24
LR = 1e-4
EPOCHS = 6
NUM_WORKERS = 2  # adjust for your machine
IMG_SIZE = 224

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(0.15,0.15,0.15,0.05),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

def main():
    if not DATA_DIR.exists():
        raise SystemExit(f"Please create dataset at {DATA_DIR} with subfolders per class")
    dataset = datasets.ImageFolder(str(DATA_DIR), transform=transform)
    classes = dataset.classes
    if len(classes) < 2:
        raise SystemExit("Need at least 2 classes with images to train")

    train_size = int(0.85 * len(dataset))
    val_size = len(dataset) - train_size
    train_ds, val_ds = torch.utils.data.random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS)

    # load mobilenetv2 backbone
    try:
        # newer torchvision
        backbone = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
        in_features = backbone.classifier[1].in_features
    except Exception:
        backbone = models.mobilenet_v2(pretrained=True)
        in_features = backbone.classifier[1].in_features if hasattr(backbone.classifier, '__getitem__') else backbone.last_channel

    # replace classifier
    backbone.classifier = nn.Sequential(nn.Dropout(0.2), nn.Linear(in_features, len(classes)))
    backbone = backbone.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(backbone.parameters(), lr=LR)

    best_val_acc = 0.0

    for epoch in range(EPOCHS):
        backbone.train()
        running_loss = 0.0
        correct = 0
        total = 0
        for imgs, labels in train_loader:
            imgs = imgs.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            outputs = backbone(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * imgs.size(0)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += imgs.size(0)

        train_acc = correct / total
        train_loss = running_loss / total

        # validation
        backbone.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs = imgs.to(device)
                labels = labels.to(device)
                outputs = backbone(imgs)
                _, preds = torch.max(outputs, 1)
                correct += (preds == labels).sum().item()
                total += imgs.size(0)
        val_acc = correct / total if total > 0 else 0.0

        print(f"Epoch {epoch+1}/{EPOCHS}  train_loss={train_loss:.4f}  train_acc={train_acc:.3f}  val_acc={val_acc:.3f}")

        if val_acc > best_val_acc:
            torch.save({"state_dict": backbone.state_dict(), "classes": classes}, str(SAVE_PATH))
            with open(CLASSES_PATH, "w") as f:
                json.dump(classes, f)
            best_val_acc = val_acc

    print("Training complete. Best val_acc:", best_val_acc)
    print("Saved model to:", SAVE_PATH)
    print("Saved classes to:", CLASSES_PATH)

if __name__ == "__main__":
    main()
