#!/usr/bin/env python3
"""
Safety Detection Dashboard Runner
This script runs the Flask application with proper configuration
"""

import os
import sys
from app import app
from config import config

def main():
    """Main function to run the dashboard"""
    
    # Get configuration from environment
    config_name = os.environ.get('FLASK_CONFIG') or 'default'
    
    if config_name not in config:
        print(f"Error: Configuration '{config_name}' not found.")
        print(f"Available configurations: {list(config.keys())}")
        sys.exit(1)
    
    # Initialize app with configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Get host and port from configuration
    host = app.config.get('API_HOST', '0.0.0.0')
    port = app.config.get('API_PORT', 5000)
    
    print("=" * 60)
    print("🛡️  Safety Detection Dashboard")
    print("=" * 60)
    print(f"Configuration: {config_name}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {app.config.get('DEBUG', False)}")
    print(f"Model Directory: {app.config.get('MODEL_DIR', 'model')}")
    print("=" * 60)
    print("Starting server...")
    print("Access the dashboard at: http://localhost:5000/static/index.html")
    print("=" * 60)
    
    try:
        app.run(
            host=host,
            port=port,
            debug=app.config.get('DEBUG', False),
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
