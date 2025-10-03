import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def get_bbox_from_polygon(points: List[List[float]]) -> Tuple[float, float, float, float]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    return x_min, y_min, x_max, y_max


def collect_classes(json_paths: List[Path]) -> List[str]:
    labels = []
    for jp in json_paths:
        try:
            data = json.loads(jp.read_text(encoding="utf-8"))
        except Exception:
            continue
        for shape in data.get("shapes", []):
            label = shape.get("label")
            if label and label not in labels:
                labels.append(label)
    return labels


def convert_split(split_dir: Path, out_split_dir: Path, class_to_id: Dict[str, int]) -> None:
    img_out = out_split_dir / "images"
    lbl_out = out_split_dir / "labels"
    ensure_dir(img_out)
    ensure_dir(lbl_out)

    json_files = sorted(split_dir.glob("*.json"))

    for jp in json_files:
        data = json.loads(jp.read_text(encoding="utf-8"))
        img_name = data.get("imagePath")
        img_w = float(data.get("imageWidth"))
        img_h = float(data.get("imageHeight"))
        if not img_name:
            img_name = f"{jp.stem}.jpg"
        img_src = split_dir / img_name
        if not img_src.exists():
            alt1 = split_dir / f"{jp.stem}.JPG"
            alt2 = split_dir / f"{jp.stem}.png"
            img_src = alt1 if alt1.exists() else (alt2 if alt2.exists() else img_src)

        if img_src.exists():
            shutil.copy2(img_src, img_out / img_src.name)

        lines: List[str] = []
        for shape in data.get("shapes", []):
            label = shape.get("label")
            points = shape.get("points", [])
            if not label or not points:
                continue
            if label not in class_to_id:
                continue
            x_min, y_min, x_max, y_max = get_bbox_from_polygon(points)
            cx = ((x_min + x_max) / 2.0) / img_w
            cy = ((y_min + y_max) / 2.0) / img_h
            w = (x_max - x_min) / img_w
            h = (y_max - y_min) / img_h
            cls_id = class_to_id[label]
            lines.append(f"{cls_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

        (lbl_out / f"{jp.stem}.txt").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    splits = ["train", "val", "test"]
    split_dirs = [root / s for s in splits if (root / s).exists()]

    all_jsons: List[Path] = []
    for sd in split_dirs:
        all_jsons.extend(sorted(sd.glob("*.json")))
    classes = collect_classes(all_jsons)
    class_to_id = {c: i for i, c in enumerate(classes)}

    out_root = root / "yolo"
    for s in splits:
        sd = root / s
        if sd.exists():
            convert_split(sd, out_root / s, class_to_id)

    yaml_lines = [
        f"path: {out_root.as_posix()}",
        "train: train/images",
        "val: val/images",
        "test: test/images",
        f"names: {classes}",
    ]
    (root / "dataset.yaml").write_text("\n".join(yaml_lines) + "\n", encoding="utf-8")
    print("Classes:", classes)
    print("Wrote dataset.yaml and YOLO directories under", out_root)


if __name__ == "__main__":
    main()
