#!/usr/bin/env python3
"""
CafePulse — Centralized Website URL Configuration System
Applies BASE_URL from website/site_config.json to all HTML files, sitemap.xml, and robots.txt.
"""

import json
import re
from pathlib import Path

WEBSITE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = WEBSITE_DIR / "site_config.json"

def load_base_url():
    if not CONFIG_FILE.exists():
        print(f"Error: Configuration file not found at {CONFIG_FILE}")
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            base_url = config.get("BASE_URL")
            if not base_url:
                print("Error: BASE_URL key not found in config.")
                return None
            # Ensure base_url ends with a slash
            if not base_url.endswith("/"):
                base_url += "/"
            return base_url
    except Exception as e:
        print(f"Error reading config: {e}")
        return None

def update_file(file_path: Path, base_url: str):
    try:
        content = file_path.read_text(encoding="utf-8")
        original_content = content
        
        # Regex mappings to identify absolute URL references
        # 1. Canonical tag: <link rel="canonical" href="...">
        canonical_pat = r'(<link\s+rel=["\']canonical["\']\s+href=["\'])https?://[^/]+(?:/cafepulse)?/([^"\']*)(["\']\s*/?>)'
        content = re.sub(canonical_pat, rf'\1{base_url}\2\3', content, flags=re.IGNORECASE)
        
        # 2. Open Graph tags: <meta property="og:url" content="..."> and <meta property="og:image" content="...">
        og_url_pat = r'(<meta\s+property=["\']og:url["\']\s+content=["\'])https?://[^/]+(?:/cafepulse)?/([^"\']*)(["\']\s*/?>)'
        content = re.sub(og_url_pat, rf'\1{base_url}\2\3', content, flags=re.IGNORECASE)
        
        og_img_pat = r'(<meta\s+property=["\']og:image["\']\s+content=["\'])https?://[^/]+(?:/cafepulse)?/([^"\']*)(["\']\s*/?>)'
        content = re.sub(og_img_pat, rf'\1{base_url}\2\3', content, flags=re.IGNORECASE)
        
        # 3. Twitter Card tags
        twitter_url_pat = r'(<meta\s+name=["\']twitter:url["\']\s+content=["\'])https?://[^/]+(?:/cafepulse)?/([^"\']*)(["\']\s*/?>)'
        content = re.sub(twitter_url_pat, rf'\1{base_url}\2\3', content, flags=re.IGNORECASE)
        
        twitter_img_pat = r'(<meta\s+name=["\']twitter:image["\']\s+content=["\'])https?://[^/]+(?:/cafepulse)?/([^"\']*)(["\']\s*/?>)'
        content = re.sub(twitter_img_pat, rf'\1{base_url}\2\3', content, flags=re.IGNORECASE)
        
        # 4. robots.txt Sitemap linkage
        if file_path.name == "robots.txt":
            robots_pat = r'(Sitemap:\s+)https?://[^/]+(?:/cafepulse)?/([^\r\n]*)'
            content = re.sub(robots_pat, rf'\1{base_url}\2', content, flags=re.IGNORECASE)
            
        # 5. sitemap.xml loc mappings
        if file_path.name == "sitemap.xml":
            sitemap_pat = r'(<loc>)https?://[^/]+(?:/cafepulse)?/([^<]*)(</loc>)'
            content = re.sub(sitemap_pat, rf'\1{base_url}\2\3', content, flags=re.IGNORECASE)
            
        if content != original_content:
            file_path.write_text(content, encoding="utf-8")
            print(f"   [Configured] {file_path.name}")
        else:
            print(f"   [No Change]  {file_path.name}")
            
    except Exception as e:
        print(f"Error patching {file_path.name}: {e}")

def main():
    base_url = load_base_url()
    if not base_url:
        return
        
    print(f"Applying centralized configuration (BASE_URL: '{base_url}') to website assets...")
    
    # Process HTML files
    for html_file in WEBSITE_DIR.glob("*.html"):
        update_file(html_file, base_url)
        
    # Process robots.txt and sitemap.xml
    robots_txt = WEBSITE_DIR / "robots.txt"
    if robots_txt.exists():
        update_file(robots_txt, base_url)
        
    sitemap_xml = WEBSITE_DIR / "sitemap.xml"
    if sitemap_xml.exists():
        update_file(sitemap_xml, base_url)

if __name__ == "__main__":
    main()
