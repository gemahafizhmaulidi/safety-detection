import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import os

# Page config
st.set_page_config(
    page_title="Safety Equipment Detection",
    page_icon="🛡️",
    layout="wide"
)

# Title
st.title("🛡️ Safety Equipment Detection")
st.markdown("Deteksi Helm dan Vest menggunakan YOLOv12")

# Sidebar
st.sidebar.header("⚙️ Konfigurasi")

# Model selection
model_files = {
    "Model S": "model/BESTSModel.pt",
    "Model M": "model/BESTMModel.pt", 
    "Model N": "model/BESTNModel.pt"
}

selected_model = st.sidebar.selectbox("Pilih Model:", list(model_files.keys()))

# Threshold
confidence_threshold = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05
)

# Load model
@st.cache_resource
def load_model(model_path):
    try:
        model = YOLO(model_path)
        return model, True
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, False

# Load selected model
model, model_loaded = load_model(model_files[selected_model])

if not model_loaded:
    st.error("❌ Model tidak dapat dimuat. Pastikan file model ada di folder model/")
    st.stop()

st.sidebar.success(f"✅ Model {selected_model} berhasil dimuat!")

# Class labels
CLASS_LABELS = {0: "Helmet", 1: "Vest"}

# Main content
st.header("📸 Deteksi Gambar")

# Upload image
uploaded_file = st.file_uploader(
    "Pilih gambar untuk deteksi",
    type=['png', 'jpg', 'jpeg']
)

if uploaded_file is not None:
    # Display original image
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖼️ Gambar Original")
        image = Image.open(uploaded_file)
        st.image(image, caption="Gambar yang diupload", use_column_width=True)
    
    # Perform detection
    with st.spinner("🔍 Melakukan deteksi..."):
        results = model(image, conf=confidence_threshold)
        result = results[0]
        
        # Create result image
        img_array = np.array(image)
        
        if result.boxes is not None:
            for box in result.boxes:
                # Get coordinates
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                
                # Get class and confidence
                cls = int(box.cls[0].cpu().numpy())
                conf = float(box.conf[0].cpu().numpy())
                
                # Draw bounding box
                color = (0, 255, 0) if cls == 0 else (255, 255, 0)
                cv2.rectangle(img_array, (x1, y1), (x2, y2), color, 2)
                
                # Draw label
                label = f"{CLASS_LABELS[cls]} {conf:.2f}"
                cv2.putText(img_array, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        result_image = Image.fromarray(img_array)
        
        with col2:
            st.subheader("🎯 Hasil Deteksi")
            st.image(result_image, caption="Hasil deteksi", use_column_width=True)
    
    # Display results
    st.subheader("📋 Hasil Deteksi")
    
    if result.boxes is not None and len(result.boxes) > 0:
        helmet_count = 0
        vest_count = 0
        
        for box in result.boxes:
            cls = int(box.cls[0].cpu().numpy())
            conf = float(box.conf[0].cpu().numpy())
            
            if cls == 0:
                helmet_count += 1
            else:
                vest_count += 1
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Deteksi", len(result.boxes))
        with col2:
            st.metric("Helmet", helmet_count)
        with col3:
            st.metric("Vest", vest_count)
    else:
        st.warning("⚠️ Tidak ada objek yang terdeteksi")

# Footer
st.markdown("---")
st.markdown("**Safety Equipment Detection** - Dibuat dengan Streamlit dan YOLOv12")
