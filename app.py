"""
3D Character AI - Main Flask Application
Text-to-3D using Hunyuan3D-2.0 via Hugging Face (NO MSVC needed)
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import threading
import os

# Configuration
from config import config
config.validate()

# Database
from models import db, User, Generation

# Services
from text_to3d import generate_3d_model
from utils import is_valid_email, estimate_generation_time

# Initialize Flask
app = Flask(__name__)
app.config.from_object(config)

# Extensions
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()

# ==========================================
# AUTHENTICATION ROUTES
# ==========================================

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not email or not password:
            flash('Email and password are required', 'error')
            return redirect(url_for('signup'))
        
        if not is_valid_email(email):
            flash('Please enter a valid email address', 'error')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'error')
            return redirect(url_for('login'))
        
        # Create user
        user = User(
            email=email, 
            password_hash=generate_password_hash(password), 
            is_verified=True,
            created_at=datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash(f'Welcome back!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

# ==========================================
# DASHBOARD & GENERATION ROUTES
# ==========================================

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with stats."""
    total = Generation.query.filter_by(user_id=current_user.id).count()
    completed = Generation.query.filter_by(user_id=current_user.id, status='completed').count()
    processing = Generation.query.filter_by(user_id=current_user.id, status='processing').count()
    
    recent = Generation.query.filter_by(user_id=current_user.id)\
        .order_by(Generation.created_at.desc()).limit(6).all()
    
    return render_template('dashboard.html',
                         total_generations=total,
                         completed_generations=completed,
                         processing_generations=processing,
                         recent_generations=recent)

@app.route('/generate-3d')
@login_required
def generate_3d():
    """Main generation interface."""
    generations = Generation.query.filter_by(user_id=current_user.id)\
        .order_by(Generation.created_at.desc()).limit(10).all()
    return render_template('generate_3d.html', generations=generations)

@app.route('/api/generate', methods=['POST'])
@login_required
def api_generate():
    """
    Start 3D generation using Hunyuan3D-2.0
    """
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    use_simple = data.get('simple_mode', False)  # Option for low VRAM
    
    if not prompt:
        return jsonify({'success': False, 'error': 'Prompt is required'}), 400
    
    if len(prompt) > config.MAX_PROMPT_LENGTH:
        return jsonify({'success': False, 'error': f'Prompt too long (max {config.MAX_PROMPT_LENGTH} characters)'}), 400
    
    try:
        # Create generation record
        generation = Generation(
            user_id=current_user.id, 
            prompt=prompt, 
            status='pending'
        )
        db.session.add(generation)
        db.session.commit()
        
        # Start background processing
        thread = threading.Thread(
            target=process_generation, 
            args=(generation.id, prompt, use_simple, app)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'generation_id': generation.id,
            'message': 'Generation started with Hunyuan3D-2.0',
            'estimated_time': estimate_generation_time(),
            'mode': 'simple' if use_simple else 'full'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def process_generation(gen_id: int, prompt: str, use_simple: bool, app):
    with app.app_context():
        generation = Generation.query.get(gen_id)
        if not generation:
            print(f"❌ Generation {gen_id} not found")
            return
        
        try:
            generation.status = 'processing'
            db.session.commit()
            
            if use_simple:
                filename, filepath = generate_3d_model_simple(prompt)
            else:
                filename, filepath = generate_3d_model(prompt)
            
            generation.status = 'completed'
            generation.completed_at = datetime.utcnow()
            
            # Store model info - MUST be JSON string
            model_urls = {
                'glb': f'/download-file/{filename}',
                'filename': filename
            }
            generation.set_model_urls(model_urls)
            db.session.commit()
            
            print(f"✅ Generation {gen_id} completed: {filename}")
            print(f"   URL: /download-file/{filename}")
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Generation {gen_id} failed: {error_msg}")
            generation.status = 'failed'
            generation.error_message = error_msg
            db.session.commit()
            
            print(f"✅ Generation {gen_id} completed: {filename}")
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Generation {gen_id} failed: {error_msg}")
            generation.status = 'failed'
            generation.error_message = error_msg
            db.session.commit()

@app.route('/api/generation-status/<int:gen_id>')
@login_required
def check_status(gen_id):
    """Check generation status."""
    generation = Generation.query.get_or_404(gen_id)
    
    if generation.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'id': generation.id,
        'status': generation.status,
        'prompt': generation.prompt,
        'model_urls': generation.get_model_urls(),
        'created_at': generation.created_at.isoformat(),
        'completed_at': generation.completed_at.isoformat() if generation.completed_at else None,
        'error': generation.error_message
    })

@app.route('/download-file/<filename>')
@login_required
def download_file(filename):
    """Serve generated model file for download."""
    if '..' in filename or '/' in filename or '\\' in filename:
        return jsonify({'error': 'Invalid filename'}), 400
    
    filepath = os.path.join('static', 'models', filename)
    full_path = os.path.abspath(filepath)
    
    base_dir = os.path.abspath('static/models')
    if not full_path.startswith(base_dir):
        return jsonify({'error': 'Access denied'}), 403
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(filepath, as_attachment=True, download_name=filename)

@app.route('/view-file/<filename>')
@login_required
def view_file(filename):
    """Serve GLB file for 3D viewer (not as download)."""
    if '..' in filename or '/' in filename or '\\' in filename:
        return jsonify({'error': 'Invalid filename'}), 400
    
    filepath = os.path.join('static', 'models', filename)
    full_path = os.path.abspath(filepath)
    
    base_dir = os.path.abspath('static/models')
    if not full_path.startswith(base_dir):
        return jsonify({'error': 'Access denied'}), 403
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(filepath, mimetype='model/gltf-binary')


@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     🎨 3D CHARACTER AI - HUNYUAN3D-2.0 VERSION          ║
    ║                                                          ║
    ║  🚀 Powered by: Tencent Hunyuan3D-2.0                   ║
    ║  🔑 API Token: Get from huggingface.co/settings/tokens  ║
    ║                                                          ║
    ║  📖 Setup:                                               ║
    ║  1. Add HF_API_TOKEN=hf_your_token_here to .env         ║
    ║  2. Accept model license at huggingface.co/tencent/Hunyuan3D-2
    ║  3. pip install -r requirements.txt                     ║
    ║  4. pip install git+https://github.com/Tencent/Hunyuan3D-2.git
    ║  5. huggingface-cli login                               ║
    ║  6. python app.py                                       ║
    ║                                                          ║
    ║  💾 VRAM Requirements:                                   ║
    ║  • Full mode (shape + texture): ~16GB VRAM              ║
    ║  • Simple mode (shape only): ~6GB VRAM                  ║
    ║                                                          ║
    ║  🌐 Open: http://localhost:5000                         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=config.FLASK_PORT)