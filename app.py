import os
import json
import time
import urllib.request
from flask import Flask, render_template, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='.', template_folder='templates')

GITHUB_USERNAME = "reianrd328"
CONTENT_FILE = os.path.join(os.path.dirname(__file__), 'content.json')
INQUIRIES_FILE = os.path.join(os.path.dirname(__file__), 'inquiries.json')

# Simple in-memory cache for GitHub API calls to avoid rate limiting
github_cache = {
    'profile': None,
    'profile_time': 0,
    'repos': None,
    'repos_time': 0
}
CACHE_TTL = 600  # 10 minutes

def load_content():
    if os.path.exists(CONTENT_FILE):
        try:
            with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print("Error loading content.json:", e)
    return {}

def save_content(data):
    try:
        with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print("Error saving content.json:", e)
        return False

def fetch_github_profile():
    now = time.time()
    if github_cache['profile'] and (now - github_cache['profile_time'] < CACHE_TTL):
        return github_cache['profile']
    
    try:
        url = f"https://api.github.com/users/{GITHUB_USERNAME}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Python-Flask-Portfolio'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            github_cache['profile'] = data
            github_cache['profile_time'] = now
            return data
    except Exception as e:
        print("GitHub profile fetch error:", e)
        # Fallback data if offline / rate-limited
        return {
            "login": GITHUB_USERNAME,
            "name": "Lyrch Ong",
            "bio": "Web Designer & Technical Support Specialist",
            "public_repos": 13,
            "followers": 5,
            "html_url": f"https://github.com/{GITHUB_USERNAME}"
        }

def fetch_github_repos():
    now = time.time()
    if github_cache['repos'] and (now - github_cache['repos_time'] < CACHE_TTL):
        return github_cache['repos']
    
    try:
        url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated&per_page=12"
        req = urllib.request.Request(url, headers={'User-Agent': 'Python-Flask-Portfolio'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            github_cache['repos'] = data
            github_cache['repos_time'] = now
            return data
    except Exception as e:
        print("GitHub repos fetch error:", e)
        return []

@app.route('/')
def home():
    content = load_content()
    profile = fetch_github_profile()
    return render_template('index.html', content=content, github_profile=profile)

@app.route('/api/content', methods=['GET', 'POST'])
def handle_content():
    if request.method == 'POST':
        new_data = request.get_json(silent=True)
        if not new_data:
            return jsonify({'success': False, 'message': 'Invalid JSON data'}), 400
        
        # Verify password if provided
        current_content = load_content()
        stored_pw = current_content.get('admin', {}).get('password', 'admin')
        req_pw = request.headers.get('X-Admin-Password') or new_data.get('_admin_password')
        
        if req_pw != stored_pw:
            return jsonify({'success': False, 'message': 'Unauthorized: Incorrect admin password'}), 401
            
        if '_admin_password' in new_data:
            del new_data['_admin_password']
            
        if save_content(new_data):
            return jsonify({'success': True, 'message': 'Content saved successfully'})
        return jsonify({'success': False, 'message': 'Failed to write content file'}), 500
        
    return jsonify(load_content())

@app.route('/api/github/profile')
def api_github_profile():
    return jsonify(fetch_github_profile())

@app.route('/api/github/repos')
def api_github_repos():
    repos = fetch_github_repos()
    # Filter and format for portfolio display
    formatted = []
    for r in repos:
        formatted.append({
            'name': r.get('name'),
            'description': r.get('description') or 'No description provided.',
            'language': r.get('language') or 'Code',
            'stars': r.get('stargazers_count', 0),
            'forks': r.get('forks_count', 0),
            'html_url': r.get('html_url'),
            'updated_at': r.get('updated_at', '')[:10]
        })
    return jsonify({'success': True, 'repos': formatted})

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    data = request.get_json(silent=True) or request.form.to_dict()
    if not data or not data.get('email') or not data.get('message'):
        return jsonify({'success': False, 'message': 'Please provide both your email and message.'}), 400
    
    inquiry = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'name': data.get('name', 'Anonymous'),
        'email': data.get('email'),
        'subject': data.get('subject', 'Portfolio Inquiry'),
        'message': data.get('message')
    }
    
    # Store locally in inquiries.json
    inquiries = []
    if os.path.exists(INQUIRIES_FILE):
        try:
            with open(INQUIRIES_FILE, 'r', encoding='utf-8') as f:
                inquiries = json.load(f)
        except Exception:
            inquiries = []
            
    inquiries.insert(0, inquiry)
    try:
        with open(INQUIRIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(inquiries, f, indent=2)
    except Exception as e:
        print("Error saving inquiry:", e)
        
    return jsonify({'success': True, 'message': 'Thank you! Your message has been received.'})

@app.route('/admin/')
@app.route('/admin/index.html')
def admin_page():
    return send_from_directory('admin', 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Lyrch Dev Portfolio System is running on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
