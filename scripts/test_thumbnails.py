import json
import os
import sys

def test():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_file = os.path.join(root, 'content.json')
    with open(content_file, 'r', encoding='utf-8') as f:
        content = json.load(f)

    videos = content.get('aiVideo', {}).get('videos', [])
    print(f"Total videos in content.json: {len(videos)}")
    
    missing_thumbnails = []
    missing_files = []
    for v in videos:
        thumb = v.get('thumbnail')
        if not thumb:
            missing_thumbnails.append(v.get('title'))
        else:
            abs_path = os.path.join(root, thumb.replace('/', os.sep))
            if not os.path.exists(abs_path):
                missing_files.append((v.get('title'), thumb))

    if missing_thumbnails:
        print(f"[FAIL] Missing thumbnail property on: {missing_thumbnails}")
        sys.exit(1)
    else:
        print("[OK] Every video has a thumbnail property defined.")

    if missing_files:
        print(f"[FAIL] Thumbnail files missing on disk: {missing_files}")
        sys.exit(1)
    else:
        print(f"[OK] All {len(videos)} thumbnail files exist on disk in images/thumbnails/!")

if __name__ == '__main__':
    test()
