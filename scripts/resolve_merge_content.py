import os
import json
from PIL import Image, ImageDraw, ImageFont

def make_thumbnail(output_path, title, album, tools, accent_color=(6, 182, 212)):
    width, height = 1280, 720
    im = Image.new('RGB', (width, height), color=(10, 15, 29))
    draw = ImageDraw.Draw(im)

    # Ambient glow
    for r in range(400, 0, -10):
        draw.ellipse([width - 300 - r, height // 2 - r, width - 300 + r, height // 2 + r],
                     fill=(accent_color[0] // 4, accent_color[1] // 4, accent_color[2] // 4))

    # Grid / Tech accent lines
    for y in range(0, height, 80):
        draw.line([(0, y), (width, y)], fill=(20, 28, 48), width=1)
    for x in range(0, width, 80):
        draw.line([(x, 0), (x, height)], fill=(20, 28, 48), width=1)

    draw.rectangle([0, 0, width, height], outline=(255, 255, 255, 15), width=2)

    font_path_bold = "C:\\Windows\\Fonts\\segoeuib.ttf"
    font_path_reg = "C:\\Windows\\Fonts\\segoeui.ttf"
    font_title = ImageFont.truetype(font_path_bold, 54) if os.path.exists(font_path_bold) else ImageFont.load_default()
    font_badge = ImageFont.truetype(font_path_bold, 24) if os.path.exists(font_path_bold) else ImageFont.load_default()
    font_tools = ImageFont.truetype(font_path_reg, 22) if os.path.exists(font_path_reg) else ImageFont.load_default()
    font_logo = ImageFont.truetype(font_path_bold, 28) if os.path.exists(font_path_bold) else ImageFont.load_default()

    draw.text((70, 60), "LYRCH DEV  •  AI CINEMATIC SHOWCASE", fill=(148, 163, 184), font=font_logo)

    badge_text = album.upper()
    badge_bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
    badge_w = badge_bbox[2] - badge_bbox[0] + 36
    badge_h = badge_bbox[3] - badge_bbox[1] + 18
    bx, by = 70, 130
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=12, fill=(accent_color[0]//3, accent_color[1]//3, accent_color[2]//3), outline=accent_color, width=2)
    draw.text((bx + 18, by + 8), badge_text, fill=(255, 255, 255), font=font_badge)

    import textwrap
    wrapped_lines = textwrap.wrap(title, width=24)
    ty = 230
    for line in wrapped_lines[:2]:
        draw.text((70, ty), line, fill=(255, 255, 255), font=font_title)
        ty += 70

    tx = 70
    tools_y = height - 120
    for t in tools[:4]:
        t_box = draw.textbbox((0, 0), t, font=font_tools)
        tw = t_box[2] - t_box[0] + 30
        th = t_box[3] - t_box[1] + 16
        draw.rounded_rectangle([tx, tools_y, tx + tw, tools_y + th], radius=8, fill=(22, 33, 56), outline=(51, 65, 85), width=1)
        draw.text((tx + 15, tools_y + 7), t, fill=(203, 213, 225), font=font_tools)
        tx += tw + 14

    cx, cy = width - 260, height // 2
    draw.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=(24, 32, 54), outline=accent_color, width=4)
    draw.polygon([(cx - 16, cy - 30), (cx - 16, cy + 30), (cx + 30, cy)], fill=accent_color)
    draw.text((width - 240, height - 70), "4K UHD • AI MEDIA", fill=(100, 116, 139), font=font_tools)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im.save(output_path, 'JPEG', quality=90)
    print(f"Created thumbnail: {output_path}")

# Generate thumbnail for the newly uploaded video
new_thumb = "images/thumbnails/thumb_Man_watching_clock_inside_house_20260919130641.jpg"
make_thumbnail(new_thumb, "Time & Anticipation AI Scene", "Gemini AI Workflows", ["Google Gemini", "Google Flow"], (6, 182, 212))

# Load full base content from our local branch commit (b0ad922)
all_videos = [
    {
        "id": "vid_1790948237773",
        "title": "Time & Anticipation AI Scene",
        "album": "Gemini AI Workflows",
        "videoUrl": "video/Man_watching_clock_inside_house_20260919130641.mp4",
        "thumbnail": "images/thumbnails/thumb_Man_watching_clock_inside_house_20260919130641.jpg",
        "tools": ["Google Gemini", "Google Flow"],
        "description": "Cinematic atmosphere study of patience and tension crafted through generative video workflows."
    },
    {
        "id": "vid-1",
        "title": "Filipino Street Food Commercial",
        "album": "AI Commercials & Ads",
        "videoUrl": "video/Creat_me_comercial_eating_fili.mp4",
        "thumbnail": "images/thumbnails/thumb_Creat_me_comercial_eating_fili.jpg",
        "tools": ["Google Gemini", "ChatGPT", "Runway Gen-3", "CapCut"],
        "description": "Vibrant AI food commercial showcasing Filipino cuisine, dynamic camera zooms, and sound-synced appetizing visual flows."
    },
    {
        "id": "vid_1790946509787",
        "title": "New AI Video Creation",
        "album": "Gemini AI Workflows",
        "videoUrl": "video/clip_1.mp4",
        "thumbnail": "images/thumbnails/thumb_clip_1.jpg",
        "tools": ["Google Gemini", "Google Flow"],
        "description": "Created with AI prompting and video workflow automation."
    },
    {
        "id": "vid-2",
        "title": "Luxury Fragrance & Fashion Commercial",
        "album": "AI Commercials & Ads",
        "videoUrl": "video/Seductive_comercial_video_man.mp4",
        "thumbnail": "images/thumbnails/thumb_Seductive_comercial_video_man.jpg",
        "tools": ["Google Flow", "Gemini AI", "Premiere Pro"],
        "description": "High-end aesthetic commercial with dramatic studio lighting, slow-motion camera movement, and luxury brand pacing."
    },
    {
        "id": "vid-3",
        "title": "Next-Gen Smartphone Product Promo",
        "album": "AI Commercials & Ads",
        "videoUrl": "video/iphone.mp4",
        "thumbnail": "images/thumbnails/thumb_iphone.jpg",
        "tools": ["Google Gemini", "AI Motion", "After Effects"],
        "description": "Sleek 3D product showcase animation highlighting hardware curves, dynamic reflections, and tech commercial styling."
    },
    {
        "id": "vid-4",
        "title": "Filipino Cultural Heritage AI Story",
        "album": "Gemini AI Workflows",
        "videoUrl": "video/Create_me_prompt_ah_filipino_c.mp4",
        "thumbnail": "images/thumbnails/thumb_Create_me_prompt_ah_filipino_c.jpg",
        "tools": ["Google Gemini", "ChatGPT Prompting", "Midjourney AI"],
        "description": "Cultural visual narrative generated through iterative Gemini prompting, capturing traditional Filipino warmth and scenery."
    },
    {
        "id": "vid-5",
        "title": "Magical Fantasy World Clip",
        "album": "Gemini AI Workflows",
        "videoUrl": "video/Create_me_video_clip_magical_t.mp4",
        "thumbnail": "images/thumbnails/thumb_Create_me_video_clip_magical_t.jpg",
        "tools": ["Google Gemini", "Google Flow", "AI Synthesis"],
        "description": "Surreal magical landscape with mystical particle effects, glowing foliage, and atmospheric lighting crafted via generative prompt pipelines."
    },
    {
        "id": "vid-6",
        "title": "Community Giving & Empathy Reel",
        "album": "Gemini AI Workflows",
        "videoUrl": "video/donating.mp4",
        "thumbnail": "images/thumbnails/thumb_donating.jpg",
        "tools": ["Google Gemini", "ChatGPT / GPT-4o", "Premiere Pro"],
        "description": "Heartfelt social message visual reel emphasizing community sharing, empathy, and emotional storytelling."
    },
    {
        "id": "vid-clip3",
        "title": "AI Dynamic Scene Generation",
        "album": "Gemini AI Workflows",
        "videoUrl": "video/clip_3.mp4",
        "thumbnail": "images/thumbnails/thumb_clip_3.jpg",
        "tools": ["Google Gemini", "Google Flow", "AI Motion"],
        "description": "Dynamic AI visual clip created with generative prompt pipelines and neural styling."
    },
    {
        "id": "vid-7",
        "title": "Portfolio Brand Opener & Intro",
        "album": "Creative Reels & Promos",
        "videoUrl": "video/intro.mp4",
        "thumbnail": "images/thumbnails/thumb_intro.jpg",
        "tools": ["Google Flow", "Premiere Pro", "CapCut"],
        "description": "Punchy, fast-paced brand opener with cybernetic transitions, neon lighting, and high-impact sound design."
    },
    {
        "id": "vid-clip6",
        "title": "Generative AI Motion Clip",
        "album": "Creative Reels & Promos",
        "videoUrl": "video/6.mp4",
        "thumbnail": "images/thumbnails/thumb_6.jpg",
        "tools": ["Google Gemini", "CapCut AI", "Google Flow"],
        "description": "Creative generative AI motion clip showcasing multi-model transitions and high visual pacing."
    },
    {
        "id": "vid-8",
        "title": "AI Production Showcase Reel (Widescreen)",
        "album": "Creative Reels & Promos",
        "videoUrl": "video/new-video-hero-hor.mp4",
        "thumbnail": "images/thumbnails/thumb_new-video-hero-hor.jpg",
        "tools": ["Google Gemini", "Google Flow", "Premiere Pro"],
        "description": "Comprehensive 16:9 cinematic showcase reel combining multi-model generative visuals, color grading, and commercial editing."
    },
    {
        "id": "vid-9",
        "title": "Social Media Vertical Reel (TikTok/Shorts)",
        "album": "Creative Reels & Promos",
        "videoUrl": "video/new-video-hero-ver.mp4",
        "thumbnail": "images/thumbnails/thumb_new-video-hero-ver.jpg",
        "tools": ["CapCut AI", "Google Gemini", "Mobile Motion"],
        "description": "9:16 vertical motion reel engineered for high engagement on mobile platforms, social shorts, and Instagram Reels."
    }
]

# Load git show b0ad922:content.json or build clean object
import subprocess
raw = subprocess.check_output(['git', 'show', 'b0ad922:content.json'], encoding='utf-8')
content = json.loads(raw)

content['aiVideo']['videos'] = all_videos
content['aiVideo']['videoUrl'] = "video/Man_watching_clock_inside_house_20260919130641.mp4"
content['aiVideo']['albums'] = ["AI Commercials & Ads", "Gemini AI Workflows", "Creative Reels & Promos"]

with open('content.json', 'w', encoding='utf-8') as f:
    json.dump(content, f, indent=2)

print(f"Successfully resolved content.json with {len(all_videos)} videos, all with thumbnails!")
