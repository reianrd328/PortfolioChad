import os
import json
from PIL import Image, ImageDraw, ImageFont

def make_thumbnail(output_path, title, album, tools, accent_color=(255, 42, 133)):
    width, height = 1280, 720
    im = Image.new('RGB', (width, height), color=(10, 15, 29))
    draw = ImageDraw.Draw(im)

    # Ambient gradient glow
    for r in range(400, 0, -10):
        alpha = int(25 * (1 - r / 400))
        glow_box = [width - 300 - r, height // 2 - r, width - 300 + r, height // 2 + r]
        draw.ellipse(glow_box, fill=(accent_color[0] // 4, accent_color[1] // 4, accent_color[2] // 4))

    # Grid / Tech accent lines
    for y in range(0, height, 80):
        draw.line([(0, y), (width, y)], fill=(20, 28, 48), width=1)
    for x in range(0, width, 80):
        draw.line([(x, 0), (x, height)], fill=(20, 28, 48), width=1)

    # Dark vignette gradient on edges
    draw.rectangle([0, 0, width, height], outline=(255, 255, 255, 15), width=2)

    # Load font
    font_path_bold = "C:\\Windows\\Fonts\\segoeuib.ttf"
    font_path_reg = "C:\\Windows\\Fonts\\segoeui.ttf"
    
    font_title = ImageFont.truetype(font_path_bold, 54) if os.path.exists(font_path_bold) else ImageFont.load_default()
    font_badge = ImageFont.truetype(font_path_bold, 24) if os.path.exists(font_path_bold) else ImageFont.load_default()
    font_tools = ImageFont.truetype(font_path_reg, 22) if os.path.exists(font_path_reg) else ImageFont.load_default()
    font_logo = ImageFont.truetype(font_path_bold, 28) if os.path.exists(font_path_bold) else ImageFont.load_default()

    # Top Brand Bar
    draw.text((70, 60), "LYRCH DEV  •  AI CINEMATIC SHOWCASE", fill=(148, 163, 184), font=font_logo)

    # Album Category Badge
    badge_text = album.upper()
    badge_bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
    badge_w = badge_bbox[2] - badge_bbox[0] + 36
    badge_h = badge_bbox[3] - badge_bbox[1] + 18
    bx, by = 70, 130
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=12, fill=(accent_color[0], accent_color[1], accent_color[2], 50), outline=accent_color, width=2)
    draw.text((bx + 18, by + 8), badge_text, fill=(255, 255, 255), font=font_badge)

    # Title - wrap if long
    import textwrap
    wrapped_lines = textwrap.wrap(title, width=24)
    ty = 230
    for line in wrapped_lines[:2]:
        draw.text((70, ty), line, fill=(255, 255, 255), font=font_title)
        ty += 70

    # Tools Pills
    tx = 70
    tools_y = height - 120
    for t in tools[:4]:
        t_box = draw.textbbox((0, 0), t, font=font_tools)
        tw = t_box[2] - t_box[0] + 30
        th = t_box[3] - t_box[1] + 16
        draw.rounded_rectangle([tx, tools_y, tx + tw, tools_y + th], radius=8, fill=(22, 33, 56), outline=(51, 65, 85), width=1)
        draw.text((tx + 15, tools_y + 7), t, fill=(203, 213, 225), font=font_tools)
        tx += tw + 14

    # Center-Right Play Button
    cx, cy = width - 260, height // 2
    draw.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=(24, 32, 54), outline=accent_color, width=4)
    # Draw play triangle
    draw.polygon([(cx - 16, cy - 30), (cx - 16, cy + 30), (cx + 30, cy)], fill=accent_color)

    # 4K UHD Badge bottom right
    draw.text((width - 240, height - 70), "4K UHD • AI MEDIA", fill=(100, 116, 139), font=font_tools)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im.save(output_path, 'JPEG', quality=90)
    print(f"Created thumbnail: {output_path}")

def generate_all():
    with open('content.json', 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    videos = content.get('aiVideo', {}).get('videos', [])
    accents = {
        'AI Commercials & Ads': (255, 42, 133),
        'Gemini AI Workflows': (6, 182, 212),
        'Creative Reels & Promos': (168, 85, 247)
    }

    for v in videos:
        url = v.get('videoUrl', '')
        stem = os.path.splitext(os.path.basename(url))[0]
        thumb_rel = f"images/thumbnails/thumb_{stem}.jpg"
        accent = accents.get(v.get('album', ''), (255, 42, 133))
        make_thumbnail(thumb_rel, v.get('title', stem), v.get('album', 'AI Video'), v.get('tools', ['Google Gemini']), accent)
        v['thumbnail'] = thumb_rel

    with open('content.json', 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2)
    print(f"Updated content.json with {len(videos)} thumbnails!")

if __name__ == '__main__':
    generate_all()
