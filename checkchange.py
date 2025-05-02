import csv
import hashlib
import os
import requests
import webbrowser
from bs4 import BeautifulSoup
from urllib.parse import urlparse

WEBSITE_FILE = 'websites.csv'
HASH_FILE = 'site_hash.csv'
SNAPSHOT_FOLDER = 'html_snapshots'
DEFACEMENT_KEYWORDS = ['hacked by', 'owned by', 'defaced', 'we are legion', 'anonymous', 'cyber army']

os.makedirs(SNAPSHOT_FOLDER, exist_ok=True)

def get_cleaned_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove potentially irrelevant elements
        for tag in soup(['script', 'style', 'noscript', 'footer', 'header']):
            tag.decompose()

        cleaned_text = soup.get_text(separator=' ', strip=True).lower()
        cleaned_html = soup.prettify()
        return cleaned_text, cleaned_html
    except Exception as e:
        print(f"[!] Error fetching {url}: {e}")
        return None, None

def get_text_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def save_cleaned_html(domain, html):
    filename = os.path.join(SNAPSHOT_FOLDER, f"{domain}.html")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

def load_websites():
    with open(WEBSITE_FILE, 'r') as f:
        reader = csv.DictReader(f)
        return [{'website': row['website address'], 'email': row['email']} for row in reader]

def load_hashes():
    if not os.path.exists(HASH_FILE):
        return {}
    with open(HASH_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        return {row[0]: row[1] for row in reader if len(row) >= 2}

def save_hashes(hashes):
    with open(HASH_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['website', 'hash'])
        for site, h in hashes.items():
            writer.writerow([site, h])

def check_for_defacement(text):
    return any(keyword in text for keyword in DEFACEMENT_KEYWORDS)

def extract_domain(url):
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path.split('/')[0]
    return domain.replace("www.", "").replace("/", "_")

def check_websites():
    websites = load_websites()
    hashes = load_hashes()
    changed_sites = []
    updated_hashes = False

    for entry in websites:
        url = entry['website']
        print(f"\n🔍 Checking: {url}")
        
        cleaned_text, cleaned_html = get_cleaned_html(url)
        if not cleaned_text:
            continue

        current_hash = get_text_hash(cleaned_text)
        domain_name = extract_domain(url)

        # If website not in hashes, store initial hash
        if url not in hashes:
            print(f"[+] New site detected. Storing initial hash for {url}")
            hashes[url] = current_hash
            save_cleaned_html(domain_name, cleaned_html)
            updated_hashes = True
            continue

        # Compare with stored hash
        if current_hash != hashes[url]:
            print(f"[⚠️] Change detected in {url}")
            defaced = check_for_defacement(cleaned_text)
            changed_sites.append({
                'url': url,
                'email': entry['email'],
                'domain': domain_name,
                'defaced': defaced,
                'new_hash': current_hash,
                'html': cleaned_html
            })
        else:
            print(f"[✓] No changes detected in {url}")

    # Save updated hashes if any new sites were added
    if updated_hashes:
        save_hashes(hashes)
        print("\n[✓] Updated hash file with new websites")

    return changed_sites