"""
Configuration settings for 3D Character AI using Hunyuan3D-2.0
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    FLASK_PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Hugging Face Token
    HF_API_TOKEN = os.environ.get('HF_API_TOKEN')
    
    # Model settings
    MODEL_ID = "tencent/Hunyuan3D-2"
    MODEL_SUBFOLDER = "hunyuan3d-dit-v2-0"
    TEXGEN_MODEL_ID = "tencent/Hunyuan3D-2"
    
    # Generation settings
    MAX_PROMPT_LENGTH = 500
    DEFAULT_OUTPUT_FORMAT = "glb"
    
    def validate(self):
        errors = []
        
        if not self.SECRET_KEY or self.SECRET_KEY == 'dev-secret-key-change-in-production':
            errors.append("WARNING: Using default SECRET_KEY")
        
        if not self.HF_API_TOKEN:
            errors.append("HF_API_TOKEN is missing! Add your Hugging Face token to .env file")
        elif not self.HF_API_TOKEN.startswith('hf_'):
            errors.append("WARNING: HF_API_TOKEN should start with 'hf_'")
        
        if errors:
            print("=" * 60)
            print("CONFIGURATION WARNINGS:")
            print("=" * 60)
            for error in errors:
                print(f"   • {error}")
            print("=" * 60)

config = Config()