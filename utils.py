"""
Utility functions for Safety Detection Dashboard
"""

import os
import logging
import cv2
import numpy as np
from PIL import Image
from datetime import datetime
import json

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/safety_detection.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def create_upload_directory():
    """Create upload directory if it doesn't exist"""
    upload_dir = 'uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return upload_dir

def save_uploaded_file(file, upload_dir):
    """Save uploaded file with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    return filepath

def draw_detections(image, detections):
    """Draw bounding boxes and labels on image"""
    img_array = np.array(image)
    
    for detection in detections:
        x1, y1, x2, y2 = detection['bbox']
        color = (0, 255, 0) if detection['class'] == 'Helmet' else (255, 255, 0)
        
        # Draw bounding box
        cv2.rectangle(img_array, (x1, y1), (x2, y2), color, 2)
        
        # Draw label
        label = f"{detection['class']} {detection['confidence']:.2f}"
        cv2.putText(img_array, label, (x1, y1-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    return Image.fromarray(img_array)

def get_model_info(model_path):
    """Get information about a model file"""
    if not os.path.exists(model_path):
        return None
    
    file_size = os.path.getsize(model_path)
    file_size_mb = file_size / (1024 * 1024)
    
    return {
        "path": model_path,
        "name": os.path.basename(model_path),
        "size_mb": round(file_size_mb, 2),
        "exists": True
    }

def validate_model_file(model_path):
    """Validate if model file is accessible and valid"""
    try:
        if not os.path.exists(model_path):
            return False, "Model file does not exist"
        
        if not model_path.endswith('.pt'):
            return False, "Model file must be a .pt file"
        
        file_size = os.path.getsize(model_path)
        if file_size < 1024:  # Less than 1KB
            return False, "Model file appears to be corrupted or empty"
        
        return True, "Model file is valid"
        
    except Exception as e:
        return False, f"Error validating model: {str(e)}"

def format_detection_results(detections):
    """Format detection results for API response"""
    if not detections:
        return {
            "total": 0,
            "helmets": 0,
            "vests": 0,
            "details": []
        }
    
    helmets = len([d for d in detections if d['class'] == 'Helmet'])
    vests = len([d for d in detections if d['class'] == 'Vest'])
    
    return {
        "total": len(detections),
        "helmets": helmets,
        "vests": vests,
        "details": detections
    }

def cleanup_temp_files(directory, pattern="temp_*", max_age_hours=24):
    """Clean up temporary files older than specified age"""
    try:
        current_time = datetime.now()
        for filename in os.listdir(directory):
            if filename.startswith(pattern.split('*')[0]):
                filepath = os.path.join(directory, filename)
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                
                if (current_time - file_time).total_seconds() > max_age_hours * 3600:
                    os.remove(filepath)
                    logging.info(f"Cleaned up temporary file: {filename}")
    except Exception as e:
        logging.error(f"Error cleaning up temporary files: {e}")

def get_system_info():
    """Get system information for debugging"""
    import platform
    import psutil
    
    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "cpu_count": psutil.cpu_count(),
        "memory_total": round(psutil.virtual_memory().total / (1024**3), 2),  # GB
        "memory_available": round(psutil.virtual_memory().available / (1024**3), 2),  # GB
        "disk_usage": round(psutil.disk_usage('/').free / (1024**3), 2)  # GB
    }

def check_camera_availability(camera_index=0):
    """Check if camera is available"""
    try:
        cap = cv2.VideoCapture(camera_index)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            return ret
        return False
    except Exception:
        return False

def resize_image(image, max_size=1024):
    """Resize image while maintaining aspect ratio"""
    width, height = image.size
    
    if width <= max_size and height <= max_size:
        return image
    
    if width > height:
        new_width = max_size
        new_height = int(height * max_size / width)
    else:
        new_height = max_size
        new_width = int(width * max_size / height)
    
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def create_error_response(message, error_code=500):
    """Create standardized error response"""
    return {
        "success": False,
        "error": message,
        "timestamp": datetime.now().isoformat(),
        "error_code": error_code
    }

def create_success_response(data, message="Success"):
    """Create standardized success response"""
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }
