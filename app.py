from flask import Flask, request, jsonify, send_file, Response, send_from_directory
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import os
import base64
import io
import json
from datetime import datetime
import threading
import time

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

# Global variables
model = None
model_loaded = False
CLASS_LABELS = {0: "Helmet", 1: "Vest"}

def load_model():
    """Load YOLO model"""
    global model, model_loaded
    try:
        # You can change the model path here
        model_path = "model/BESTSModel.pt"
        model = YOLO(model_path)
        model_loaded = True
        print(f"✅ Model loaded successfully from {model_path}")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        model_loaded = False

def process_image(image, confidence_threshold=0.5):
    """Process image and return detection results"""
    if not model_loaded:
        return None, "Model not loaded"
    
    try:
        results = model(image, conf=confidence_threshold)
        result = results[0]
        
        detections = []
        if result.boxes is not None:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                cls = int(box.cls[0].cpu().numpy())
                conf = float(box.conf[0].cpu().numpy())
                
                detections.append({
                    "class": CLASS_LABELS[cls],
                    "confidence": round(conf, 3),
                    "bbox": [int(x1), int(y1), int(x2), int(y2)]
                })
        
        return detections, None
    except Exception as e:
        return None, str(e)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model_loaded,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/detect/image', methods=['POST'])
def detect_image():
    """Detect objects in uploaded image"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        confidence = float(request.form.get('confidence', 0.5))
        
        # Read image
        image = Image.open(file.stream)
        
        # Process image
        detections, error = process_image(image, confidence)
        
        if error:
            return jsonify({"error": error}), 500
        
        # Convert image to base64 for response
        img_array = np.array(image)
        
        # Draw bounding boxes
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            color = (0, 255, 0) if detection['class'] == 'Helmet' else (255, 255, 0)
            cv2.rectangle(img_array, (x1, y1), (x2, y2), color, 2)
            
            label = f"{detection['class']} {detection['confidence']:.2f}"
            cv2.putText(img_array, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Convert back to PIL and encode
        result_image = Image.fromarray(img_array)
        buffer = io.BytesIO()
        result_image.save(buffer, format='JPEG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return jsonify({
            "success": True,
            "detections": detections,
            "image": img_str,
            "total_detections": len(detections)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/detect/video', methods=['POST'])
def detect_video():
    """Detect objects in uploaded video"""
    try:
        if 'video' not in request.files:
            return jsonify({"error": "No video file provided"}), 400
        
        file = request.files['video']
        confidence = float(request.form.get('confidence', 0.5))
        
        # Save uploaded video temporarily
        temp_path = f"temp_video_{int(time.time())}.mp4"
        file.save(temp_path)
        
        # Process video
        cap = cv2.VideoCapture(temp_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Create output video writer
        output_path = f"output_video_{int(time.time())}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        total_detections = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert frame to PIL Image
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            
            # Process frame
            detections, error = process_image(pil_image, confidence)
            
            if detections:
                total_detections += len(detections)
                
                # Draw bounding boxes
                for detection in detections:
                    x1, y1, x2, y2 = detection['bbox']
                    color = (0, 255, 0) if detection['class'] == 'Helmet' else (255, 255, 0)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    label = f"{detection['class']} {detection['confidence']:.2f}"
                    cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            out.write(frame)
            frame_count += 1
        
        cap.release()
        out.release()
        
        # Clean up temp file
        os.remove(temp_path)
        
        return jsonify({
            "success": True,
            "output_path": output_path,
            "frame_count": frame_count,
            "total_detections": total_detections,
            "fps": fps
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/video/<filename>')
def get_video(filename):
    """Serve processed video file"""
    try:
        return send_file(filename, mimetype='video/mp4')
    except Exception as e:
        return jsonify({"error": str(e)}), 404

def generate_frames():
    """Generate frames for real-time detection"""
    # This would typically connect to a camera
    # For demo purposes, we'll use a placeholder
    cap = cv2.VideoCapture(0)  # Use default camera
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to PIL Image
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        
        # Process frame
        detections, error = process_image(pil_image, 0.5)
        
        if detections:
            # Draw bounding boxes
            for detection in detections:
                x1, y1, x2, y2 = detection['bbox']
                color = (0, 255, 0) if detection['class'] == 'Helmet' else (255, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                label = f"{detection['class']} {detection['confidence']:.2f}"
                cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/api/stream')
def video_stream():
    """Real-time video stream endpoint"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available models"""
    models = []
    model_dir = "model"
    if os.path.exists(model_dir):
        for file in os.listdir(model_dir):
            if file.endswith('.pt'):
                models.append({
                    "name": file.replace('.pt', ''),
                    "path": f"{model_dir}/{file}"
                })
    
    return jsonify({"models": models})

@app.route('/api/load-model', methods=['POST'])
def load_model_endpoint():
    """Load a specific model"""
    try:
        data = request.get_json()
        model_path = data.get('model_path')
        
        if not model_path or not os.path.exists(model_path):
            return jsonify({"error": "Invalid model path"}), 400
        
        global model, model_loaded
        model = YOLO(model_path)
        model_loaded = True
        
        return jsonify({
            "success": True,
            "message": f"Model {model_path} loaded successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    # Load model on startup
    load_model()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
