import os
import sys
import json
import base64

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root)

from app import app

client = app.test_client()

# 1. Test video list
res = client.get('/api/videos-list')
data = res.get_json()
print("Videos list status:", res.status_code, "Found videos:", len(data.get('videos', [])))
assert res.status_code == 200
assert len(data.get('videos', [])) >= 12

# 2. Test base64 thumbnail upload
# Tiny 1x1 black JPEG
dummy_jpg = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00`\x00`\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xbf\x00\xff\xd9'
b64_str = "data:image/jpeg;base64," + base64.b64encode(dummy_jpg).decode('utf-8')

res2 = client.post('/api/upload-thumbnail-base64', json={
    'image': b64_str,
    'filename': 'thumb_test_auto_unit.jpg'
})
data2 = res2.get_json()
print("Base64 thumb status:", res2.status_code, "imageUrl:", data2.get('imageUrl'))
assert res2.status_code == 200
assert data2.get('success') is True
assert os.path.exists(os.path.join(root, 'images', 'thumbnails', 'thumb_test_auto_unit.jpg'))

# Clean up test artifact
try:
    os.remove(os.path.join(root, 'images', 'thumbnails', 'thumb_test_auto_unit.jpg'))
except:
    pass

print("[ALL TESTS PASSED SUCCESSFULLY!]")
