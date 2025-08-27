#!/usr/bin/env python3
"""
Test script for Safety Detection Dashboard API
"""

import requests
import json
import os
from datetime import datetime

class SafetyDetectionAPITester:
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_health(self):
        """Test health check endpoint"""
        print("🔍 Testing health check...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_models(self):
        """Test models endpoint"""
        print("🔍 Testing models endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/models")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Models endpoint: {data}")
                return data.get('models', [])
            else:
                print(f"❌ Models endpoint failed: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Models endpoint error: {e}")
            return []
    
    def test_load_model(self, model_path):
        """Test model loading"""
        print(f"🔍 Testing model loading: {model_path}")
        try:
            response = self.session.post(
                f"{self.base_url}/load-model",
                json={"model_path": model_path}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Model loaded: {data}")
                return True
            else:
                print(f"❌ Model loading failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Model loading error: {e}")
            return False
    
    def test_image_detection(self, image_path):
        """Test image detection"""
        print(f"🔍 Testing image detection: {image_path}")
        if not os.path.exists(image_path):
            print(f"❌ Image file not found: {image_path}")
            return False
        
        try:
            with open(image_path, 'rb') as f:
                files = {'image': f}
                data = {'confidence': 0.5}
                response = self.session.post(
                    f"{self.base_url}/detect/image",
                    files=files,
                    data=data
                )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Image detection successful: {data.get('total_detections', 0)} detections")
                return True
            else:
                print(f"❌ Image detection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Image detection error: {e}")
            return False
    
    def test_video_detection(self, video_path):
        """Test video detection"""
        print(f"🔍 Testing video detection: {video_path}")
        if not os.path.exists(video_path):
            print(f"❌ Video file not found: {video_path}")
            return False
        
        try:
            with open(video_path, 'rb') as f:
                files = {'video': f}
                data = {'confidence': 0.5}
                response = self.session.post(
                    f"{self.base_url}/detect/video",
                    files=files,
                    data=data
                )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Video detection successful: {data.get('frame_count', 0)} frames processed")
                return True
            else:
                print(f"❌ Video detection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Video detection error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print("=" * 60)
        print("🧪 Safety Detection API Test Suite")
        print("=" * 60)
        print(f"Testing API at: {self.base_url}")
        print(f"Timestamp: {datetime.now()}")
        print("=" * 60)
        
        # Test health
        health_ok = self.test_health()
        if not health_ok:
            print("❌ Health check failed. Make sure the server is running.")
            return
        
        # Test models
        models = self.test_models()
        if models:
            # Test loading first model
            first_model = models[0]['path']
            model_loaded = self.test_load_model(first_model)
            
            if model_loaded:
                # Test image detection if sample image exists
                sample_image = "image/val_batch0_pred.jpg"
                if os.path.exists(sample_image):
                    self.test_image_detection(sample_image)
                else:
                    print("⚠️  No sample image found for testing")
                
                # Test video detection if sample video exists
                sample_video = "sample_video.mp4"
                if os.path.exists(sample_video):
                    self.test_video_detection(sample_video)
                else:
                    print("⚠️  No sample video found for testing")
            else:
                print("❌ Model loading failed. Cannot test detection endpoints.")
        else:
            print("⚠️  No models found. Cannot test detection endpoints.")
        
        print("=" * 60)
        print("🏁 API testing completed")
        print("=" * 60)

def main():
    """Main function"""
    tester = SafetyDetectionAPITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
