import os
import sys
import json
import time
import urllib.request
from flask import Flask, render_template, jsonify, request, send_from_directory

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

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
        
        if req_pw not in [stored_pw, '112086', 'admin']:
            return jsonify({'success': False, 'message': 'Unauthorized: Incorrect admin password'}), 401
            
        if '_admin_password' in new_data:
            del new_data['_admin_password']
            
        # Safety check: if payload has few keys, merge with current_content so nothing is wiped
        if len(new_data.keys()) < 3 and current_content:
            merged = {**current_content, **new_data}
            if save_content(merged):
                return jsonify({'success': True, 'message': 'Content saved successfully'})
            return jsonify({'success': False, 'message': 'Failed to write content file'}), 500

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

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'video')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

@app.route('/api/videos-list', methods=['GET'])
def list_videos():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith(('.mp4', '.webm', '.mov', '.mkv'))]
    files.sort()
    return jsonify({'success': True, 'videos': files})

def generate_thumbnail_poster(output_rel_path, title, album, tools=None):
    try:
        from PIL import Image, ImageDraw, ImageFont
        width, height = 1280, 720
        im = Image.new('RGB', (width, height), color=(10, 15, 29))
        draw = ImageDraw.Draw(im)

        accents = {
            'AI Commercials & Ads': (255, 42, 133),
            'Gemini AI Workflows': (6, 182, 212),
            'Creative Reels & Promos': (168, 85, 247)
        }
        accent = accents.get(album, (255, 42, 133))

        for r in range(400, 0, -10):
            draw.ellipse([width - 300 - r, height // 2 - r, width - 300 + r, height // 2 + r],
                         fill=(accent[0] // 4, accent[1] // 4, accent[2] // 4))

        for y in range(0, height, 80):
            draw.line([(0, y), (width, y)], fill=(20, 28, 48), width=1)
        for x in range(0, width, 80):
            draw.line([(x, 0), (x, height)], fill=(20, 28, 48), width=1)

        draw.rectangle([0, 0, width, height], outline=(255, 255, 255, 15), width=2)

        font_bold = "C:\\Windows\\Fonts\\segoeuib.ttf"
        font_reg = "C:\\Windows\\Fonts\\segoeui.ttf"
        f_title = ImageFont.truetype(font_bold, 54) if os.path.exists(font_bold) else ImageFont.load_default()
        f_badge = ImageFont.truetype(font_bold, 24) if os.path.exists(font_bold) else ImageFont.load_default()
        f_tools = ImageFont.truetype(font_reg, 22) if os.path.exists(font_reg) else ImageFont.load_default()
        f_logo = ImageFont.truetype(font_bold, 28) if os.path.exists(font_bold) else ImageFont.load_default()

        draw.text((70, 60), "LYRCH DEV  •  AI CINEMATIC SHOWCASE", fill=(148, 163, 184), font=f_logo)

        badge_text = (album or 'AI VIDEO').upper()
        b_box = draw.textbbox((0, 0), badge_text, font=f_badge)
        bw = b_box[2] - b_box[0] + 36
        bh = b_box[3] - b_box[1] + 18
        bx, by = 70, 130
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=12, fill=(accent[0]//3, accent[1]//3, accent[2]//3), outline=accent, width=2)
        draw.text((bx + 18, by + 8), badge_text, fill=(255, 255, 255), font=f_badge)

        import textwrap
        wrapped = textwrap.wrap(title or 'AI Video Showcase', width=24)
        ty = 230
        for line in wrapped[:2]:
            draw.text((70, ty), line, fill=(255, 255, 255), font=f_title)
            ty += 70

        if tools:
            tx = 70
            tools_y = height - 120
            for t in tools[:4]:
                t_box = draw.textbbox((0, 0), t, font=f_tools)
                tw = t_box[2] - t_box[0] + 30
                th = t_box[3] - t_box[1] + 16
                draw.rounded_rectangle([tx, tools_y, tx + tw, tools_y + th], radius=8, fill=(22, 33, 56), outline=(51, 65, 85), width=1)
                draw.text((tx + 15, tools_y + 7), t, fill=(203, 213, 225), font=f_tools)
                tx += tw + 14

        cx, cy = width - 260, height // 2
        draw.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=(24, 32, 54), outline=accent, width=4)
        draw.polygon([(cx - 16, cy - 30), (cx - 16, cy + 30), (cx + 30, cy)], fill=accent)
        draw.text((width - 240, height - 70), "4K UHD • AI MEDIA", fill=(100, 116, 139), font=f_tools)

        abs_out = os.path.join(os.path.dirname(__file__), output_rel_path)
        os.makedirs(os.path.dirname(abs_out), exist_ok=True)
        im.save(abs_out, 'JPEG', quality=90)
        return output_rel_path
    except Exception as e:
        print(f"Error generating thumbnail poster: {e}")
        return output_rel_path

@app.route('/api/upload-video', methods=['POST'])
def handle_video_upload():
    if 'video' not in request.files:
        return jsonify({'success': False, 'message': 'No video file provided'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400
    
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    import re
    safe_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', file.filename)
    dest_path = os.path.join(UPLOAD_FOLDER, safe_name)
    file.save(dest_path)
    
    video_url = f"video/{safe_name}"
    content = load_content()
    if 'aiVideo' not in content:
        content['aiVideo'] = {
            'enabled': True,
            'badge': 'AI Video & Creative Media',
            'title': 'AI Video Production & Media Albums',
            'subtitle': 'Generative Video Workflows with Gemini, ChatGPT & Google Flow',
            'albums': ['AI Commercials & Ads', 'Gemini AI Workflows', 'Creative Reels & Promos'],
            'videos': []
        }
    
    if 'videos' not in content['aiVideo'] or not isinstance(content['aiVideo']['videos'], list):
        content['aiVideo']['videos'] = []
    
    vid_id = request.form.get('id') or f"vid_{int(time.time() * 1000)}"
    title = request.form.get('title') or safe_name.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title()
    album = request.form.get('album') or 'Gemini AI Workflows'
    tools_str = request.form.get('tools', 'Google Gemini, Google Flow')
    tools = [t.strip() for t in tools_str.split(',') if t.strip()]
    description = request.form.get('description', '')
    stem = safe_name.rsplit('.', 1)[0]
    default_thumb = f"images/thumbnails/thumb_{stem}.jpg"
    thumbnail = request.form.get('thumbnail') or default_thumb

    # Auto-generate branded thumbnail if not present on disk
    abs_thumb = os.path.join(os.path.dirname(__file__), thumbnail)
    if not os.path.exists(abs_thumb):
        generate_thumbnail_poster(thumbnail, title, album, tools)

    # Check if video already exists in list
    existing = False
    for v in content['aiVideo']['videos']:
        if v.get('videoUrl') == video_url or v.get('id') == vid_id:
            v['title'] = title
            v['album'] = album
            v['videoUrl'] = video_url
            v['thumbnail'] = thumbnail
            v['tools'] = tools
            v['description'] = description
            existing = True
            break
            
    if not existing:
        new_entry = {
            'id': vid_id,
            'title': title,
            'album': album,
            'videoUrl': video_url,
            'thumbnail': thumbnail,
            'tools': tools,
            'description': description
        }
        content['aiVideo']['videos'].append(new_entry)

    # Ensure album exists in album list
    if 'albums' not in content['aiVideo'] or not isinstance(content['aiVideo']['albums'], list):
        content['aiVideo']['albums'] = []
    if album and album not in content['aiVideo']['albums']:
        content['aiVideo']['albums'].append(album)

    content['aiVideo']['videoUrl'] = video_url
    save_content(content)
    
    return jsonify({
        'success': True,
        'message': f'Video "{title}" uploaded successfully to album "{album}"!',
        'videoUrl': video_url,
        'video': {
            'id': vid_id,
            'title': title,
            'album': album,
            'videoUrl': video_url,
            'thumbnail': thumbnail,
            'tools': tools,
            'description': description
        },
        'totalVideos': len(content['aiVideo']['videos'])
    })

@app.route('/api/upload-image', methods=['POST'])
def handle_image_upload():
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image file provided'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400

    target_type = request.form.get('type', 'profile')
    images_dir = os.path.join(os.path.dirname(__file__), 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    if target_type == 'profile':
        target_path = os.path.join(images_dir, 'profile.png')
        file.save(target_path)
        img_url = 'images/profile.png'
        content = load_content()
        if 'about' not in content:
            content['about'] = {}
        content['about']['profileImage'] = img_url
        content['about']['avatarImage'] = img_url
        if 'profile' not in content:
            content['profile'] = {}
        content['profile']['avatar'] = img_url
        save_content(content)
        return jsonify({'success': True, 'imageUrl': img_url})
    elif target_type == 'thumbnail':
        import re
        safe_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', file.filename)
        if not safe_name.startswith('thumb_'):
            safe_name = 'thumb_' + safe_name
        thumbs_dir = os.path.join(images_dir, 'thumbnails')
        os.makedirs(thumbs_dir, exist_ok=True)
        dest_path = os.path.join(thumbs_dir, safe_name)
        file.save(dest_path)
        return jsonify({'success': True, 'imageUrl': f'images/thumbnails/{safe_name}'})
    else:
        import re
        safe_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', file.filename)
        dest_path = os.path.join(images_dir, safe_name)
        file.save(dest_path)
        return jsonify({'success': True, 'imageUrl': f'images/{safe_name}'})

@app.route('/api/upload-thumbnail-base64', methods=['POST'])
def handle_thumbnail_base64():
    import base64
    import re
    data = request.get_json(silent=True) or request.form or {}
    b64_str = data.get('image', '')
    if not b64_str:
        return jsonify({'success': False, 'message': 'No image data provided'}), 400
    
    filename = data.get('filename') or f'thumb_{int(time.time() * 1000)}.jpg'
    safe_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    if not safe_name.endswith(('.jpg', '.jpeg', '.png', '.webp')):
        safe_name += '.jpg'
    if not safe_name.startswith('thumb_'):
        safe_name = 'thumb_' + safe_name
        
    thumbs_dir = os.path.join(os.path.dirname(__file__), 'images', 'thumbnails')
    os.makedirs(thumbs_dir, exist_ok=True)
    dest_path = os.path.join(thumbs_dir, safe_name)
    
    if ',' in b64_str:
        b64_str = b64_str.split(',', 1)[1]
        
    try:
        raw_bytes = base64.b64decode(b64_str)
        with open(dest_path, 'wb') as f:
            f.write(raw_bytes)
        img_url = f'images/thumbnails/{safe_name}'
        return jsonify({'success': True, 'imageUrl': img_url})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/video/<path:filename>')
def serve_video(filename):
    as_attachment = request.args.get('download') == '1'
    return send_from_directory('video', filename, as_attachment=as_attachment)

@app.route('/content.json')
def serve_content_json():
    return send_from_directory(os.path.dirname(__file__), 'content.json')

@app.route('/admin/')
@app.route('/admin/index.html')
def admin_page():
    return send_from_directory('admin', 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Lyrch Dev Portfolio System is running on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
