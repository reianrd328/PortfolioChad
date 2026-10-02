import shutil
import os
import sys

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def build():
    root = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(root, 'templates', 'index.html')
    dest = os.path.join(root, 'index.html')
    
    if os.path.exists(src):
        shutil.copyfile(src, dest)
        print(f"[SUCCESS] Compiled {src} -> {dest}")
        print("[INFO] Root index.html is ready for GitHub Pages hosting (reianrd328.github.io/myprofile)!")
    else:
        print(f"[ERROR] {src} not found.")

if __name__ == '__main__':
    build()
