from pathlib import Path
from ultralytics import YOLO
import torch


def main():
    root = Path(__file__).resolve().parent
    dataset_yaml = root / "dataset.yaml"
    if not dataset_yaml.exists():
        raise FileNotFoundError("dataset.yaml not found. Run tools/convert_labelme_to_yolo.py first.")

    # Auto-resume if a previous run exists
    default_run = root / "runs" / "yolov8n-strawberry" / "weights"
    last_ckpt = default_run / "last.pt"
    best_ckpt = default_run / "best.pt"

    if last_ckpt.exists():
        # Resume from last checkpoint
        model = YOLO(str(last_ckpt))
        resume = True
    else:
        # Fresh start from pretrained nano
        model = YOLO("yolov8n.pt")
        resume = False
    device = 0 if torch.cuda.is_available() else 'cpu'
    model.train(
        data=str(dataset_yaml),
        imgsz=640,
        epochs=50,
        batch=16,
        device=device,
        project=str(root / "runs"),
        name="yolov8n-strawberry",
        resume=resume,
    )


if __name__ == "__main__":
    main()



