// Safety Detection Dashboard JavaScript

class SafetyDetectionDashboard {
    constructor() {
        this.apiBaseUrl = 'http://localhost:5000/api';
        this.currentModel = null;
        this.confidenceThreshold = 0.5;
        this.isStreaming = false;
        this.streamInterval = null;
        this.recentDetections = [];
        
        this.initializeEventListeners();
        this.loadModels();
        this.checkHealth();
    }

    initializeEventListeners() {
        // Model selection
        document.getElementById('modelSelect').addEventListener('change', (e) => {
            this.loadModel(e.target.value);
        });

        // Confidence slider
        document.getElementById('confidenceSlider').addEventListener('input', (e) => {
            this.confidenceThreshold = parseFloat(e.target.value);
            document.getElementById('confidenceValue').textContent = e.target.value;
        });

        // Image upload
        this.setupImageUpload();
        
        // Video upload
        this.setupVideoUpload();
        
        // Real-time camera
        this.setupRealTimeCamera();
    }

    async checkHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            
            const statusIndicator = document.getElementById('status-indicator');
            if (data.model_loaded) {
                statusIndicator.textContent = 'Connected';
                statusIndicator.parentElement.querySelector('.fas').className = 'fas fa-circle text-success me-1';
            } else {
                statusIndicator.textContent = 'Model Loading...';
                statusIndicator.parentElement.querySelector('.fas').className = 'fas fa-circle text-warning me-1';
            }
        } catch (error) {
            console.error('Health check failed:', error);
            document.getElementById('status-indicator').textContent = 'Disconnected';
            document.getElementById('status-indicator').parentElement.querySelector('.fas').className = 'fas fa-circle text-danger me-1';
        }
    }

    async loadModels() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/models`);
            const data = await response.json();
            
            const modelSelect = document.getElementById('modelSelect');
            modelSelect.innerHTML = '<option value="">Select a model...</option>';
            
            data.models.forEach(model => {
                const option = document.createElement('option');
                option.value = model.path;
                option.textContent = model.name;
                modelSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Failed to load models:', error);
        }
    }

    async loadModel(modelPath) {
        if (!modelPath) return;
        
        try {
            this.showLoading('Loading model...');
            
            const response = await fetch(`${this.apiBaseUrl}/load-model`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ model_path: modelPath })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.currentModel = modelPath;
                this.showNotification('Model loaded successfully!', 'success');
                this.checkHealth();
            } else {
                this.showNotification('Failed to load model', 'error');
            }
        } catch (error) {
            console.error('Error loading model:', error);
            this.showNotification('Error loading model', 'error');
        } finally {
            this.hideLoading();
        }
    }

    setupImageUpload() {
        const imageInput = document.getElementById('imageInput');
        const imageUploadArea = document.getElementById('imageUploadArea');
        const imagePreview = document.getElementById('imagePreview');
        const previewImg = document.getElementById('previewImg');

        // File input change
        imageInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                this.handleImageFile(file);
            }
        });

        // Drag and drop
        imageUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            imageUploadArea.classList.add('dragover');
        });

        imageUploadArea.addEventListener('dragleave', () => {
            imageUploadArea.classList.remove('dragover');
        });

        imageUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            imageUploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleImageFile(files[0]);
            }
        });

        // Click to upload
        imageUploadArea.addEventListener('click', () => {
            imageInput.click();
        });
    }

    async handleImageFile(file) {
        if (!file.type.startsWith('image/')) {
            this.showNotification('Please select an image file', 'error');
            return;
        }

        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('previewImg').src = e.target.result;
            document.getElementById('imagePreview').style.display = 'block';
        };
        reader.readAsDataURL(file);

        // Process image
        await this.processImage(file);
    }

    async processImage(file) {
        try {
            this.showLoading('Processing image...');
            
            const formData = new FormData();
            formData.append('image', file);
            formData.append('confidence', this.confidenceThreshold);

            const response = await fetch(`${this.apiBaseUrl}/detect/image`, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                this.displayImageResults(data);
                this.updateStatistics(data.detections);
            } else {
                this.showNotification(data.error || 'Failed to process image', 'error');
            }
        } catch (error) {
            console.error('Error processing image:', error);
            this.showNotification('Error processing image', 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayImageResults(data) {
        const imageResults = document.getElementById('imageResults');
        
        imageResults.innerHTML = `
            <div class="detection-result">
                <img src="data:image/jpeg;base64,${data.image}" alt="Detection Result" class="img-fluid">
                <div class="detection-stats">
                    <div class="detection-stat">
                        <h4>${data.total_detections}</h4>
                        <small>Total</small>
                    </div>
                    <div class="detection-stat">
                        <h4>${data.detections.filter(d => d.class === 'Helmet').length}</h4>
                        <small>Helmets</small>
                    </div>
                    <div class="detection-stat">
                        <h4>${data.detections.filter(d => d.class === 'Vest').length}</h4>
                        <small>Vests</small>
                    </div>
                </div>
            </div>
        `;
    }

    setupVideoUpload() {
        const videoInput = document.getElementById('videoInput');
        const videoUploadArea = document.getElementById('videoUploadArea');
        const videoPreview = document.getElementById('videoPreview');
        const previewVideo = document.getElementById('previewVideo');

        // File input change
        videoInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                this.handleVideoFile(file);
            }
        });

        // Drag and drop
        videoUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            videoUploadArea.classList.add('dragover');
        });

        videoUploadArea.addEventListener('dragleave', () => {
            videoUploadArea.classList.remove('dragover');
        });

        videoUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            videoUploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleVideoFile(files[0]);
            }
        });

        // Click to upload
        videoUploadArea.addEventListener('click', () => {
            videoInput.click();
        });
    }

    async handleVideoFile(file) {
        if (!file.type.startsWith('video/')) {
            this.showNotification('Please select a video file', 'error');
            return;
        }

        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('previewVideo').src = e.target.result;
            document.getElementById('videoPreview').style.display = 'block';
        };
        reader.readAsDataURL(file);

        // Process video
        await this.processVideo(file);
    }

    async processVideo(file) {
        try {
            this.showLoading('Processing video...');
            this.showVideoProgress();
            
            const formData = new FormData();
            formData.append('video', file);
            formData.append('confidence', this.confidenceThreshold);

            const response = await fetch(`${this.apiBaseUrl}/detect/video`, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                this.displayVideoResults(data);
            } else {
                this.showNotification(data.error || 'Failed to process video', 'error');
            }
        } catch (error) {
            console.error('Error processing video:', error);
            this.showNotification('Error processing video', 'error');
        } finally {
            this.hideLoading();
            this.hideVideoProgress();
        }
    }

    displayVideoResults(data) {
        const videoResults = document.getElementById('videoResults');
        
        videoResults.innerHTML = `
            <div class="detection-result">
                <video controls class="img-fluid">
                    <source src="${this.apiBaseUrl}/video/${data.output_path}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <div class="detection-stats">
                    <div class="detection-stat">
                        <h4>${data.frame_count}</h4>
                        <small>Frames</small>
                    </div>
                    <div class="detection-stat">
                        <h4>${data.total_detections}</h4>
                        <small>Detections</small>
                    </div>
                    <div class="detection-stat">
                        <h4>${data.fps}</h4>
                        <small>FPS</small>
                    </div>
                </div>
            </div>
        `;
    }

    setupRealTimeCamera() {
        const startCameraBtn = document.getElementById('startCameraBtn');
        const stopCameraBtn = document.getElementById('stopCameraBtn');
        const cameraFeed = document.getElementById('cameraFeed');
        const cameraStream = document.getElementById('cameraStream');
        const streamImg = document.getElementById('streamImg');

        startCameraBtn.addEventListener('click', () => {
            this.startRealTimeDetection();
        });

        stopCameraBtn.addEventListener('click', () => {
            this.stopRealTimeDetection();
        });
    }

    startRealTimeDetection() {
        if (this.isStreaming) return;

        this.isStreaming = true;
        document.getElementById('cameraFeed').style.display = 'none';
        document.getElementById('cameraStream').style.display = 'block';

        // Start streaming
        const streamImg = document.getElementById('streamImg');
        streamImg.src = `${this.apiBaseUrl}/stream?t=${Date.now()}`;

        // Update live statistics periodically
        this.streamInterval = setInterval(() => {
            this.updateLiveStatistics();
        }, 1000);
    }

    stopRealTimeDetection() {
        if (!this.isStreaming) return;

        this.isStreaming = false;
        document.getElementById('cameraFeed').style.display = 'block';
        document.getElementById('cameraStream').style.display = 'none';

        if (this.streamInterval) {
            clearInterval(this.streamInterval);
            this.streamInterval = null;
        }
    }

    updateLiveStatistics() {
        // Simulate live statistics update
        // In a real implementation, this would come from the streaming API
        const total = Math.floor(Math.random() * 10);
        const helmets = Math.floor(Math.random() * total);
        const vests = total - helmets;

        document.getElementById('liveTotalDetections').textContent = total;
        document.getElementById('liveHelmetCount').textContent = helmets;
        document.getElementById('liveVestCount').textContent = vests;

        // Add recent detection
        if (total > 0) {
            this.addRecentDetection('Helmet', 0.85);
        }
    }

    addRecentDetection(className, confidence) {
        const recentDetections = document.getElementById('recentDetections');
        const detectionItem = document.createElement('div');
        detectionItem.className = `detection-item ${className.toLowerCase()}`;
        
        const time = new Date().toLocaleTimeString();
        detectionItem.innerHTML = `
            <span><i class="fas fa-${className === 'Helmet' ? 'hard-hat' : 'tshirt'} me-2"></i>${className}</span>
            <span class="detection-time">${time}</span>
        `;

        recentDetections.insertBefore(detectionItem, recentDetections.firstChild);

        // Keep only last 10 detections
        while (recentDetections.children.length > 10) {
            recentDetections.removeChild(recentDetections.lastChild);
        }
    }

    updateStatistics(detections) {
        const total = detections.length;
        const helmets = detections.filter(d => d.class === 'Helmet').length;
        const vests = detections.filter(d => d.class === 'Vest').length;

        document.getElementById('totalDetections').textContent = total;
        document.getElementById('helmetCount').textContent = helmets;
        document.getElementById('vestCount').textContent = vests;
    }

    showLoading(message = 'Loading...') {
        document.getElementById('loadingMessage').textContent = message;
        const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
        modal.show();
    }

    hideLoading() {
        const modal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
        if (modal) {
            modal.hide();
        }
    }

    showVideoProgress() {
        document.getElementById('videoProgress').style.display = 'block';
        const progressBar = document.querySelector('#videoProgress .progress-bar');
        progressBar.style.width = '0%';
        
        // Simulate progress
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 10;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
            }
            progressBar.style.width = progress + '%';
        }, 200);
    }

    hideVideoProgress() {
        document.getElementById('videoProgress').style.display = 'none';
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SafetyDetectionDashboard();
});
