#!/usr/bin/env python3
"""
Update imple folder with all changes made to the project
"""
import os
import shutil

def copy_file(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    print(f"  ✅ Copied: {src} → {dst}")

def main():
    print("=" * 60)
    print("Updating imple folder with all project changes")
    print("=" * 60)

    # 1. Search module JS components (updated)
    print("\n[1] Search module components...")
    copy_file("modules/search/index.js",                              "imple/modules/search/index.js")
    copy_file("modules/search/utils/searchEngine.js",                 "imple/modules/search/utils/searchEngine.js")
    copy_file("modules/search/components/FAQList.js",                 "imple/modules/search/components/FAQList.js")
    copy_file("modules/search/components/SearchInput.js",             "imple/modules/search/components/SearchInput.js")
    copy_file("modules/search/components/SearchOverlay.js",           "imple/modules/search/components/SearchOverlay.js")
    copy_file("modules/search/components/SearchResultsPreview.js",    "imple/modules/search/components/SearchResultsPreview.js")
    copy_file("modules/search/styles/search.css",                     "imple/modules/search/styles/search.css")

    # 2. New data files
    print("\n[2] New data files...")
    os.makedirs("imple/modules/search/data", exist_ok=True)
    copy_file("modules/search/data/searchData.js",      "imple/modules/search/data/searchData.js")
    copy_file("modules/search/data/chroniclesData.js",  "imple/modules/search/data/chroniclesData.js")

    # 3. CSS files
    print("\n[3] CSS files...")
    os.makedirs("imple/css", exist_ok=True)
    copy_file("css/search-integration.css",   "imple/css/search-integration.css")
    copy_file("css/chronicles-section.css",   "imple/css/chronicles-section.css")

    # 4. New pages
    print("\n[4] New pages...")
    copy_file("search-results.html",  "imple/pages/search-results.html")
    copy_file("chronicles.html",      "imple/pages/chronicles.html")

    # 5. Reference index.html
    print("\n[5] Reference index...")
    copy_file("index.html", "imple/index.html")

    print("\n" + "=" * 60)
    print("✅ Done! imple folder updated.")
    print("=" * 60)

if __name__ == "__main__":
    main()
