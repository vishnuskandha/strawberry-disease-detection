 import io
 from pathlib import Path
 import streamlit as st
 from PIL import Image
 from ultralytics import YOLO


@st.cache_resource
def load_model(weights_path: Path):
    return YOLO(str(weights_path))


def main():
    st.title("Strawberry Disease Detection")
    st.caption("Model: YOLOv8. Dataset: Usman Afzaal (Kaggle)")

    # Choose best weights
    root = Path(__file__).resolve().parent
    default_weights = root / "runs" / "detect" / "yolov8n-strawberry" / "weights" / "best.pt"
    weights = st.text_input("Path to weights (.pt)", value=str(default_weights))
    weights_path = Path(weights)
    if not weights_path.exists():
        st.warning("Weights not found yet. Train the model first or provide a valid path.")

    uploaded = st.file_uploader("Upload a strawberry image", type=["jpg", "jpeg", "png"])
    if uploaded and weights_path.exists():
        image = Image.open(io.BytesIO(uploaded.read())).convert("RGB")
        st.image(image, caption="Input", use_column_width=True)
        model = load_model(weights_path)
        results = model.predict(source=image, imgsz=640, conf=0.25, verbose=False)
        res = results[0]
        plot = res.plot()  # numpy array BGR
        st.image(plot[:, :, ::-1], caption="Detections", use_column_width=True)

        # Healthy vs Not Healthy heuristic: if any detection, it's not healthy
        class_names = model.names
        if len(res.boxes) > 0:
            detected = [class_names[int(b.cls)] for b in res.boxes]
            st.error(f"Not Healthy. Detected: {', '.join(detected)}")
        else:
            st.success("Healthy")


if __name__ == "__main__":
    main()



