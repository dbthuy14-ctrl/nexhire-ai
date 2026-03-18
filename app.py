from flask import Flask, send_from_directory, request, jsonify
import os
import logging
import sqlite3
from ai_engine import NexHireAIEngine

from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='.')
logging.basicConfig(level=logging.INFO)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Serve the English Landing Page
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Serve the Vietnamese Landing Page
@app.route('/vi')
def home_vi():
    return send_from_directory('.', 'index-vi.html')

# Serve all other static files (CSS, JS, Subpages, Images)
@app.route('/<path:path>')
def static_proxy(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return "Page Not Found", 404

# Initialize MVP Database
def init_db():
    conn = sqlite3.connect('nexhire_mvp.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS candidates (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, linkedin TEXT, skills TEXT)''')
    try:
        c.execute("ALTER TABLE candidates ADD COLUMN cv_path TEXT")
        c.execute("ALTER TABLE candidates ADD COLUMN video_path TEXT")
    except sqlite3.OperationalError:
        pass # Columns already exist
    
    c.execute('''CREATE TABLE IF NOT EXISTS employers (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, plan TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, message TEXT)''')
    conn.commit()
    conn.close()

init_db()

# DB Helper
def insert_db(query, args):
    conn = sqlite3.connect('nexhire_mvp.db')
    c = conn.cursor()
    c.execute(query, args)
    conn.commit()
    conn.close()

# Mock Backend API: Candidate Signup
@app.route('/api/candidates', methods=['POST'])
def candidate_signup():
    """Endpoint for candidate profile creation"""
    data = request.json or request.form
    name = data.get('name', '')
    email = data.get('email', '')
    linkedin = data.get('linkedin', '')
    skills = data.get('skills', '')
    
    cv_path = ""
    video_path = ""
    
    cv_file = request.files.get('cv_file')
    if cv_file and cv_file.filename:
        filename = secure_filename(cv_file.filename)
        cv_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        cv_file.save(cv_path)
        
    video_file = request.files.get('video_file')
    if video_file and video_file.filename:
        filename = secure_filename(video_file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video_file.save(video_path)
        
    insert_db("INSERT INTO candidates (name, email, linkedin, skills, cv_path, video_path) VALUES (?, ?, ?, ?, ?, ?)",
              (name, email, linkedin, skills, cv_path, video_path))
              
    app.logger.info(f"New Candidate Signup Received. Files attached: CV: {bool(cv_file)} Video: {bool(video_file)}")
    return jsonify({
        "status": "success", 
        "message": "Welcome to NexHire AI! Your profile and media have been uploaded."
    }), 201

# Mock Backend API: Employer Subscription / Payment
@app.route('/api/employers/subscribe', methods=['POST'])
def process_payment():
    """Endpoint for employer subscription payments"""
    data = request.json or request.form
    plan_type = data.get('plan', 'starter')
    insert_db("INSERT INTO employers (email, plan) VALUES (?, ?)", (data.get('email', ''), plan_type))
    app.logger.info(f"Payment processed for Employer. Plan: {plan_type}")
    return jsonify({
        "status": "success", 
        "message": f"Successfully subscribed to the {plan_type.upper()} plan. The AI engine is now unlocked."
    }), 200

# Mock Backend API: Lead Generation (Contact Form)
@app.route('/api/contact', methods=['POST'])
def contact_submit():
    """Endpoint for contact form submissions"""
    data = request.json or request.form
    insert_db("INSERT INTO leads (email, message) VALUES (?, ?)", (data.get('email', ''), data.get('message', '')))
    app.logger.info(f"Contact form submitted by {data.get('email')}")
    return jsonify({"status": "success", "message": "We have received your message and will reach out shortly."})

# -------------------------------------------------------------
# REAL / DEMO AI ENDPOINTS
# -------------------------------------------------------------

@app.route('/api/ai/job-post', methods=['POST'])
def ai_generate_job():
    data = request.json or request.form
    prompt = data.get('prompt', 'Software Engineer')
    result = NexHireAIEngine.generate_job_post(prompt)
    return jsonify(result)

@app.route('/api/ai/screen-cv', methods=['POST'])
def ai_screen_cv():
    data = request.json or request.form
    cv_text = data.get('cv_text', 'MOCK CV')
    requirements = data.get('requirements', 'Python, React')
    result = NexHireAIEngine.screen_and_score_cv(cv_text, requirements)
    return jsonify(result)

@app.route('/api/ai/generate-test', methods=['POST'])
def ai_generate_test():
    data = request.json or request.form
    role = data.get('role', 'Developer')
    skills = data.get('skills', 'Programming')
    result = NexHireAIEngine.generate_dynamic_test(role, skills)
    return jsonify(result)

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.json or {}
    message = data.get('message', '')
    reply = NexHireAIEngine.chat_with_assistant(message)
    app.logger.info(f"AI Chat received message: {message}")
    return jsonify({"reply": reply})

if __name__ == '__main__':
    # Binds to 0.0.0.0 to make it publicly accessible if deployed in a container (Render, Heroku, etc)
    app.run(host='0.0.0.0', port=8000, debug=True)
