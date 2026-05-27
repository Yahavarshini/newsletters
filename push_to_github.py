"""
iNextLabs Newsletter — Push to GitHub
Run: python push_to_github.py

Pushes to: Yahavarshini/newsletters
- index.html           → repo root (newsletter archive homepage)
- 2026-05/images/...   → screenshots for May 2026
- 2026-05/whatsapp-calling.html → updated feature page
"""

import base64, os, json, urllib.request, urllib.error

# ── Config ─────────────────────────────────────────────────────────────────
TOKEN = os.environ.get('GITHUB_TOKEN', '')
OWNER = 'Yahavarshini'
REPO  = 'newsletters'

if not TOKEN:
    print("ERROR: GITHUB_TOKEN environment variable not set.")
    print("Set it with:  set GITHUB_TOKEN=your_token_here")
    input("Press Enter to exit...")
    exit(1)

# ── Helpers ─────────────────────────────────────────────────────────────────
def _headers():
    return {
        'Authorization': f'Bearer {TOKEN}',
        'Accept': 'application/vnd.github+json',
        'Content-Type': 'application/json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

def get_sha(path):
    req = urllib.request.Request(
        f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}',
        headers=_headers()
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read()).get('sha')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise

def push(github_path, content_b64, message):
    sha = get_sha(github_path)
    payload = {'message': message, 'content': content_b64, 'branch': 'main'}
    if sha:
        payload['sha'] = sha
    req = urllib.request.Request(
        f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{github_path}',
        data=json.dumps(payload).encode(),
        method='PUT',
        headers=_headers()
    )
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            action = 'updated' if sha else 'created'
            print(f'  [{status}] {action}: {github_path}')
    except urllib.error.HTTPError as e:
        print(f'  [ERROR {e.code}] {github_path}: {e.read().decode()[:200]}')

def push_text(github_path, local_path, message):
    with open(local_path, 'r', encoding='utf-8') as f:
        content = base64.b64encode(f.read().encode('utf-8')).decode()
    push(github_path, content, message)

def push_binary(github_path, local_path, message):
    with open(local_path, 'rb') as f:
        content = base64.b64encode(f.read()).decode()
    push(github_path, content, message)

# ── Files to push ────────────────────────────────────────────────────────────
HERE = os.path.dirname(os.path.abspath(__file__))

files = [
    # (github_path, local_path, message, is_binary)
    ('index.html',
     os.path.join(HERE, 'index_root.html'),
     'feat: add newsletter archive homepage',
     False),

    ('2026-05/whatsapp-calling.html',
     os.path.join(HERE, '2026-05-whatsapp-calling.html'),
     'feat: update WhatsApp Calling page with screenshots and outcomes',
     False),

    ('2026-05/images/Whatsapp-call/Support_Desk_WhatsApp_Calling.png',
     os.path.join(HERE, 'Images', 'Whatsapp-call', 'Support_Desk_WhatsApp_Calling.png'),
     'feat: add Support Desk screenshot',
     True),

    ('2026-05/images/Whatsapp-call/Call_Permission_Request.png',
     os.path.join(HERE, 'Images', 'Whatsapp-call', 'Call_Permission_Request.png'),
     'feat: add Call Permission Request screenshot',
     True),

    ('2026-05/images/Whatsapp-call/Logs_Call_Request.png',
     os.path.join(HERE, 'Images', 'Whatsapp-call', 'Logs_Call_Request.png'),
     'feat: add Logs Call Request screenshot',
     True),

    ('2026-05/images/Whatsapp-call/Call_Logs.png',
     os.path.join(HERE, 'Images', 'Whatsapp-call', 'Call_Logs.png'),
     'feat: add Call Logs screenshot',
     True),
]

# ── Run ───────────────────────────────────────────────────────────────────────
print('Pushing to GitHub: Yahavarshini/newsletters')
print()
for github_path, local_path, message, is_binary in files:
    if not os.path.exists(local_path):
        print(f'  [SKIP] File not found: {local_path}')
        continue
    if is_binary:
        push_binary(github_path, local_path, message)
    else:
        push_text(github_path, local_path, message)

print()
print('Done! View at: https://github.com/Yahavarshini/newsletters')
print('Live:          https://yahavarshini.github.io/newsletters/')
input('Press Enter to exit...')
