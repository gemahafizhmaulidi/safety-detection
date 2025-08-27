# 🛡️ Safety Detection Dashboard

Dashboard modern untuk deteksi peralatan keselamatan menggunakan model YOLOv12 dengan backend Flask dan frontend JavaScript.

## 📋 Fitur Utama

### 🖼️ Image Detection
- Upload gambar dengan drag & drop
- Deteksi helm dan vest secara real-time
- Visualisasi hasil dengan bounding box
- Statistik deteksi yang detail

### 🎥 Video Detection
- Upload video untuk analisis batch
- Processing video dengan progress indicator
- Output video dengan bounding box
- Statistik frame dan deteksi

### 📹 Real-time Detection
- Live camera feed
- Deteksi real-time
- Statistik live yang update otomatis
- Riwayat deteksi terbaru

### ⚙️ Model Management
- Multiple model support (S, M, N)
- Dynamic model loading
- Confidence threshold adjustment
- Health monitoring

## 🏗️ Arsitektur Sistem

```
Safety Detection Dashboard
├── Backend (Flask)
│   ├── API Endpoints
│   ├── YOLO Model Integration
│   ├── File Processing
│   └── Real-time Streaming
├── Frontend (JavaScript)
│   ├── Modern UI Dashboard
│   ├── Drag & Drop Interface
│   ├── Real-time Updates
│   └── Responsive Design
└── Configuration
    ├── Environment Variables
    ├── Model Management
    └── Production Settings
```

## 🚀 Instalasi dan Setup

### Prerequisites
- Python 3.8+
- YOLOv12 model files
- Web browser modern

### 1. Clone Repository
```bash
git clone <repository-url>
cd safety-detection-dashboard
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment
```bash
# Copy environment example
cp env_example.txt .env

# Edit .env file sesuai kebutuhan
nano .env
```

### 4. Prepare Model Files
Pastikan file model YOLO ada di folder `model/`:
```
model/
├── BESTSModel.pt
├── BESTMModel.pt
└── BESTNModel.pt
```

### 5. Run Dashboard
```bash
# Development mode
python run_dashboard.py

# Atau dengan environment variable
FLASK_CONFIG=development python run_dashboard.py
```

## 🌐 Akses Dashboard

Setelah server berjalan, akses dashboard di:
- **URL**: http://localhost:5000/static/index.html
- **API Base**: http://localhost:5000/api

## 📁 Struktur File

```
safety-detection-dashboard/
├── app.py                 # Flask application
├── config.py              # Configuration management
├── run_dashboard.py       # Dashboard runner
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables example
├── DASHBOARD_README.md    # This file
├── model/                 # YOLO model files
│   ├── BESTSModel.pt
│   ├── BESTMModel.pt
│   └── BESTNModel.pt
├── static/                # Frontend files
│   ├── index.html         # Main dashboard page
│   ├── css/
│   │   └── style.css      # Custom styles
│   └── js/
│       └── dashboard.js   # Dashboard functionality
├── uploads/               # Upload directory (auto-created)
└── logs/                  # Log files (auto-created)
```

## 🔧 Konfigurasi

### Environment Variables
```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True

# Model Configuration
MODEL_DIR=model
DEFAULT_MODEL=BESTSModel.pt

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000

# File Upload Configuration
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Detection Configuration
DEFAULT_CONFIDENCE=0.5

# Camera Configuration
CAMERA_INDEX=0
STREAM_FPS=30
```

### Model Configuration
- **BESTSModel.pt**: Model kecil, cepat, akurasi sedang
- **BESTMModel.pt**: Model sedang, seimbang
- **BESTNModel.pt**: Model besar, lambat, akurasi tinggi

## 📡 API Endpoints

### Health Check
```http
GET /api/health
```

### Model Management
```http
GET /api/models
POST /api/load-model
```

### Image Detection
```http
POST /api/detect/image
Content-Type: multipart/form-data
```

### Video Detection
```http
POST /api/detect/video
Content-Type: multipart/form-data
```

### Real-time Stream
```http
GET /api/stream
```

### Video Download
```http
GET /api/video/<filename>
```

## 🎨 Fitur UI/UX

### Modern Design
- Gradient backgrounds
- Smooth animations
- Responsive layout
- Custom scrollbars

### Interactive Elements
- Drag & drop upload
- Real-time progress bars
- Live statistics
- Notification system

### User Experience
- Intuitive navigation
- Clear visual feedback
- Error handling
- Loading states

## 🔒 Security Features

- CORS configuration
- File type validation
- Size limits
- Environment-based secrets

## 📊 Monitoring & Logging

### Health Monitoring
- Model loading status
- API connectivity
- Real-time status indicators

### Logging
- Application logs
- Error tracking
- Performance monitoring

## 🚀 Deployment

### Development
```bash
FLASK_CONFIG=development python run_dashboard.py
```

### Production
```bash
# Set environment variables
export FLASK_CONFIG=production
export SECRET_KEY=your-production-secret

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run_dashboard.py"]
```

## 🐛 Troubleshooting

### Common Issues

1. **Model not loading**
   - Check model files exist in `model/` directory
   - Verify file permissions
   - Check console logs

2. **CORS errors**
   - Verify CORS_ORIGINS in .env
   - Check browser console

3. **Upload failures**
   - Check file size limits
   - Verify file types
   - Check upload directory permissions

4. **Camera not working**
   - Verify camera permissions
   - Check CAMERA_INDEX setting
   - Test with different camera index

### Debug Mode
```bash
FLASK_DEBUG=True python run_dashboard.py
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- YOLOv12 model
- Flask framework
- Bootstrap CSS
- Font Awesome icons

---

**Safety Detection Dashboard** - Dibuat dengan ❤️ untuk keselamatan kerja
