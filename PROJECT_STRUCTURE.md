# 📁 Safety Detection Dashboard - Project Structure

```
safety-detection-dashboard/
├── 📄 app.py                    # Flask application & API endpoints
├── 📄 config.py                 # Configuration management
├── 📄 utils.py                  # Utility functions & helpers
├── 📄 run_dashboard.py          # Dashboard runner script
├── 📄 run_dashboard.bat         # Windows batch file to run dashboard
├── 📄 test_api.py               # API testing script
├── 📄 test_dashboard.bat        # Windows batch file to run tests
├── 📄 requirements.txt          # Python dependencies
├── 📄 env_example.txt           # Environment variables example
├── 📄 DASHBOARD_README.md       # Main documentation
├── 📄 ARCHITECTURE.md           # Architecture documentation
├── 📄 PROJECT_STRUCTURE.md      # This file
├── 📄 README.md                 # Original README
├── 📄 simple_app.py             # Original Streamlit app
├── 📄 run_app.bat               # Original batch file
│
├── 📁 model/                    # YOLO model files
│   ├── 🎯 BESTSModel.pt         # Small model (fast, moderate accuracy)
│   ├── 🎯 BESTMModel.pt         # Medium model (balanced)
│   └── 🎯 BESTNModel.pt         # Large model (slow, high accuracy)
│
├── 📁 static/                   # Frontend files
│   ├── 📄 index.html            # Main dashboard page
│   ├── 📁 css/
│   │   └── 📄 style.css         # Custom styling
│   └── 📁 js/
│       └── 📄 dashboard.js      # Dashboard functionality
│
├── 📁 image/                    # Sample images (existing)
│   ├── 📷 BoxF1_curve.png
│   ├── 📷 BoxP_curve.png
│   ├── 📷 BoxPR_curve.png
│   ├── 📷 BoxR_curve.png
│   ├── 📷 results.png
│   ├── 📷 val_batch0_pred.jpg
│   ├── 📷 val_batch1_pred.jpg
│   └── 📷 val_batch2_pred.jpg
│
├── 📁 uploads/                  # Upload directory (auto-created)
├── 📁 logs/                     # Log files (auto-created)
└── 📁 .streamlit/               # Streamlit config (existing)
```

## 📋 File Descriptions

### 🔧 Core Application Files

| File | Description |
|------|-------------|
| `app.py` | Main Flask application with all API endpoints |
| `config.py` | Configuration management with environment support |
| `utils.py` | Utility functions for file handling, validation, etc. |
| `run_dashboard.py` | Script to run the dashboard with proper configuration |
| `requirements.txt` | Python package dependencies |

### 🎨 Frontend Files

| File | Description |
|------|-------------|
| `static/index.html` | Main dashboard HTML page |
| `static/css/style.css` | Custom CSS styling |
| `static/js/dashboard.js` | JavaScript functionality |

### 🚀 Deployment & Scripts

| File | Description |
|------|-------------|
| `run_dashboard.bat` | Windows batch file to run dashboard |
| `test_api.py` | API testing script |
| `test_dashboard.bat` | Windows batch file to run tests |
| `env_example.txt` | Environment variables template |

### 📚 Documentation

| File | Description |
|------|-------------|
| `DASHBOARD_README.md` | Comprehensive user guide |
| `ARCHITECTURE.md` | Technical architecture documentation |
| `PROJECT_STRUCTURE.md` | This file - project structure overview |
| `README.md` | Original project README |

### 🎯 Model Files

| File | Description |
|------|-------------|
| `model/BESTSModel.pt` | Small YOLO model (fast inference) |
| `model/BESTMModel.pt` | Medium YOLO model (balanced) |
| `model/BESTNModel.pt` | Large YOLO model (high accuracy) |

## 🔄 Auto-Created Directories

| Directory | Purpose | Created When |
|-----------|---------|--------------|
| `uploads/` | Store uploaded files | First file upload |
| `logs/` | Application logs | First log entry |

## 🛠️ Key Features by File

### Backend Features (`app.py`)
- ✅ RESTful API endpoints
- ✅ Image detection processing
- ✅ Video detection processing
- ✅ Real-time streaming
- ✅ Model management
- ✅ File upload handling
- ✅ CORS support

### Frontend Features (`dashboard.js`)
- ✅ Drag & drop file upload
- ✅ Real-time statistics
- ✅ Model selection
- ✅ Confidence threshold adjustment
- ✅ Live camera feed
- ✅ Progress indicators
- ✅ Error handling

### Configuration Features (`config.py`)
- ✅ Environment-based configuration
- ✅ Multiple deployment modes
- ✅ Security settings
- ✅ Model configuration
- ✅ File upload limits

### Utility Features (`utils.py`)
- ✅ File validation
- ✅ Image processing helpers
- ✅ Model validation
- ✅ Error response formatting
- ✅ System monitoring

## 🚀 Quick Start Commands

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
python run_dashboard.py

# Or use batch file (Windows)
run_dashboard.bat
```

### Testing
```bash
# Test API endpoints
python test_api.py

# Or use batch file (Windows)
test_dashboard.bat
```

### Production
```bash
# Set environment
export FLASK_CONFIG=production

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📊 File Size Estimates

| Component | Estimated Size |
|-----------|----------------|
| Backend Code | ~50KB |
| Frontend Code | ~30KB |
| Documentation | ~40KB |
| YOLO Models | ~100-500MB each |
| Sample Images | ~5MB |

## 🔧 Dependencies

### Python Packages
- Flask (Web framework)
- OpenCV (Computer vision)
- Ultralytics (YOLO models)
- Pillow (Image processing)
- NumPy (Numerical computing)
- CORS (Cross-origin support)

### Frontend Libraries
- Bootstrap 5 (UI framework)
- Font Awesome (Icons)
- Vanilla JavaScript (No frameworks)

## 📈 Scalability Considerations

### Current Structure
- ✅ Modular design
- ✅ Separation of concerns
- ✅ Configuration management
- ✅ Error handling

### Future Enhancements
- 🔄 Database integration
- 🔄 User authentication
- 🔄 Cloud deployment
- 🔄 Microservices architecture

---

**Project Structure** - Organized for maintainability and scalability
