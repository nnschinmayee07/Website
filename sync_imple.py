#!/usr/bin/env python3
"""
Sync all project files into imple/ folder
"""
import os
import shutil

def copy(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    print(f"  ✅ {src}  →  {dst}")

def copy_tree(src_dir, dst_dir, skip_exts=None):
    """Recursively copy a directory"""
    skip_exts = skip_exts or []
    for root, dirs, files in os.walk(src_dir):
        # Skip hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if any(f.endswith(e) for e in skip_exts):
                continue
            src = os.path.join(root, f)
            rel = os.path.relpath(src, src_dir)
            dst = os.path.join(dst_dir, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  ✅ {src}  →  {dst}")

print("=" * 70)
print("Syncing all project files into imple/")
print("=" * 70)

# ── 1. Root HTML pages ──────────────────────────────────────────────────
print("\n[1] Root pages...")
copy("index.html",          "imple/index.html")
copy("chronicles.html",     "imple/chronicles.html")
copy("search-results.html", "imple/search-results.html")

# ── 2. CSS folder ───────────────────────────────────────────────────────
print("\n[2] CSS files...")
copy_tree("css", "imple/css")

# ── 3. JS folder ────────────────────────────────────────────────────────
print("\n[3] JS files...")
copy_tree("js", "imple/js")

# ── 4. Search modules ───────────────────────────────────────────────────
print("\n[4] Search modules...")
copy_tree("modules", "imple/modules")

# ── 5. Departments HTML pages ───────────────────────────────────────────
print("\n[5] Department pages (HTML only)...")
dept_html = [
    "departments/cse.html",
    "departments/ece.html",
    "departments/eee.html",
    "departments/aeronautical.html",
    "departments/mechanical.html",
    "departments/aiml.html",
    "departments/cse-cs.html",
    "departments/cse-ds.html",
    "departments/freshman.html",
    "departments/mba.html",
    "departments/ug.html",
    "departments/pg.html",
    "departments/faculty-profile.html",
]
for f in dept_html:
    if os.path.exists(f):
        copy(f, f"imple/{f}")

# ── 6. Placements page ──────────────────────────────────────────────────
print("\n[6] Placements page...")
copy("placements/placements.html", "imple/placements/placements.html")
copy("placements/placements.css",  "imple/placements/placements.css")
copy("placements/placements.js",   "imple/placements/placements.js")

# ── 7. Assets ───────────────────────────────────────────────────────────
print("\n[7] Assets...")
copy_tree("assets", "imple/assets")

# ── 8. NIRF logos ───────────────────────────────────────────────────────
print("\n[8] NIRF logos...")
copy_tree("nirf", "imple/nirf")

# ── 9. Logo images ──────────────────────────────────────────────────────
print("\n[9] Logo images...")
for f in ["mlrit-logo-transparent.png", "mlrit-logo.png"]:
    if os.path.exists(f):
        copy(f, f"imple/{f}")

print("\n" + "=" * 70)
print("✅ All files synced to imple/")
print("=" * 70)
