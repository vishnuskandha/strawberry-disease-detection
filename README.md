## Strawberry Disease Detection (Usman Afzaal, Kaggle)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Made by Vishnu Skandha](https://img.shields.io/badge/Author-Vishnu%20Skandha-blue.svg)](https://github.com/vishnuskandha)
[![Version](https://img.shields.io/badge/Version-1.0.0-purple.svg)](VERSION)

### Quickstart
```bash
# 1) Install deps
pip install -r requirements.txt

# 2) Convert LabelMe JSON → YOLO format and create dataset.yaml
python tools/convert_labelme_to_yolo.py

# 3) Train (auto-resume supported)
python train_yolov8.py

# 4) Run inference (no server)
python detect_strawberry.py "path\to\image.jpg"

# Optional: Streamlit app
streamlit run app.py
```

This repo trains a YOLOv8 model to detect strawberry diseases from the Kaggle dataset by Usman Afzaal and ships a simple Streamlit app to predict Healthy vs Not Healthy on uploaded images.

### 1) Prerequisites
- Windows 10/11 with Python 3.10–3.12 recommended
- Optional NVIDIA GPU + CUDA for faster training

### 2) Project layout
```
archive/
  train/ val/ test/            # Kaggle dataset with .jpg + .json (LabelMe)
  tools/convert_labelme_to_yolo.py  # converter -> YOLO format + dataset.yaml
  train_yolov8.py              # training (auto-resume supported)
  train_yolov8.bat             # Windows one-click training with simple ETA
  app.py                       # Streamlit demo (upload & detect)
  requirements.txt             # Python deps
```

### 3) Setup
Open PowerShell in the `archive` folder and run:
```bash
pip install -r requirements.txt
```
Optional (quiet a pip note from another package):
```bash
pip install opencv-python-headless
```

### 4) Convert annotations to YOLO format
This reads LabelMe `.json` files in `train/`, `val/`, `test/`, copies images, writes YOLO labels to `yolo/`, and generates `dataset.yaml`.
```bash
python tools/convert_labelme_to_yolo.py
```

You should now have:
- `yolo/train/images`, `yolo/train/labels`, etc.
- `dataset.yaml` in repo root

### 5) Train the model
Two options:

1) One-click batch file (with simple ETA on epochs remaining):
```bat
train_yolov8.bat
```

2) Direct Python:
```bash
python train_yolov8.py
```

Notes:
- Uses `yolov8n.pt` as a lightweight base.
- Logs and checkpoints are saved to `runs/detect/yolov8n-strawberry/`.

#### Train options
- Change epochs/img size: edit `epochs` or `imgsz` in `train_yolov8.py`.
- Resume: training auto-resumes if `weights/last.pt` exists (see next section).
- Fresh start: delete the run folder (see next section).

### 6) Auto-resume and continue training
`train_yolov8.py` auto-resumes if it finds `runs/detect/yolov8n-strawberry/weights/last.pt`.

- If you previously stopped at, e.g., epoch 30 of 50, re-running training continues from there automatically.
- To force a fresh start, delete `runs/detect/yolov8n-strawberry/weights/last.pt` (and optionally the entire run directory) before launching training again.

### 7) Run the model (inference)

**Option A: Simple detection script (Recommended - No web server needed!)**
```bash
# Test with a specific image
python detect_strawberry.py "path\to\your\image.jpg"

# Or run interactively
python detect_strawberry.py
```

**Option B: Batch file (Windows)**
```bash
# Double-click detect.bat or run:
detect.bat "path\to\image.jpg"
```

**Option C: Streamlit web app (if you want a web interface)**
```bash
streamlit run app.py
# Then open http://localhost:8501
```

The detection script will:
- Load your trained model automatically
- Analyze the image for diseases
- Show "HEALTHY" or "NOT HEALTHY" result
- Save an annotated image with bounding boxes

### 10) One-click setup, train, and detect (Windows)
Use the provided batch file to install dependencies, convert annotations, train (auto-resume), and run a quick detection on a sample image.

```bat
all_in_one.bat

:: Or pass an image path to detect at the end
all_in_one.bat "path\to\your\image.jpg"
```

What it does:
- Installs requirements (and quietly adds opencv-python-headless)
- Converts LabelMe annotations and generates `dataset.yaml`
- Trains the model, resuming if `last.pt` exists
- Runs detection on a sample image (from `test/` or `train/`) or the path you provide

### 11) Cleanup repository (remove heavy/derived files)
Safely remove training outputs, converted YOLO folders, caches, and large weight files without touching your code:

```bat
clean_repo.bat
```

This deletes:
- `runs/`, `yolo/`, `.streamlit/`, all `__pycache__/`
- Root `*.pt`, `*.onnx`, `*.engine`, `*.tflite` artifacts

### 12) Publish to GitHub
Initialize and push the repository (replace the URL with your repo):

```powershell
cd C:\Users\admin\Downloads\archive
git init
git lfs install
git add .
git commit -m "Strawberry Disease Detection: YOLOv8 + scripts + docs"
git branch -M main
git remote add origin https://github.com/vishnuskandha/strawberry-disease-detection.git
git push -u origin main
```

### 8) Tips & troubleshooting
- Conversion fails: ensure each `.json` has `imagePath`, `imageWidth`, `imageHeight`, and `shapes`. The converter falls back to `<json-stem>.jpg` if `imagePath` is missing.
- Slow training: reduce `epochs` or `imgsz` in `train_yolov8.py`, or use a GPU.
- Fresh run: delete the `runs/detect/yolov8n-strawberry` folder to remove prior checkpoints and logs.

### 13) Contributing
Contributions are welcome! See `CONTRIBUTING.md` for setup, branching, and PR guidelines.

### 14) Web Demo
🌐 **Live Demo:** [View on GitHub Pages](https://vishnuskandha.github.io/strawberry-disease-detection/)

**Local Demo:**
```bash
# Open the web demo locally
start web_demo.html
# or double-click web_demo.html
```

**Features:**
- Drag & drop image upload
- Visual preview of uploaded images
- Simulated disease detection results
- Links to GitHub repository and documentation

**Note:** This is a demo interface. For actual detection, use the Python scripts locally.

#### Deploy to GitHub Pages
The web demo automatically deploys to GitHub Pages when you push to the `main` branch:

1. Go to your repository Settings → Pages
2. Source: "GitHub Actions"
3. Push to `main` branch triggers deployment
4. Access at: `https://vishnuskandha.github.io/strawberry-disease-detection/`

### 15) Roadmap
- Export to ONNX/TFLite and add mobile inference example
- Severity scoring from detection sizes/counts
- CI for formatting/linting and tests for utilities
- Deploy web demo with real model backend

### 9) License & credits
- Code license: MIT (see `LICENSE`).
- Dataset: `Strawberry Disease Detection Dataset` by Usman Afzaal on Kaggle — please cite and follow the dataset license.
- Model/training: Ultralytics `YOLOv8`.
- Inspiration: community posts and open-source examples from GitHub and LinkedIn on plant disease detection and YOLOv8 best practices.

If you use this repo, please also see `CITATION.cff` for citation information.





