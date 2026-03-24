# ================================================
# SIGNALHIRE - ONE BY ONE (Credit Safe Version)
# ================================================

import requests
import time
import threading
from flask import Flask, request

API_KEY = "202.M3D7xK6FykhOIHuKoFGLLjMI8jwW"
BASE_URL = "https://www.signalhire.com/api/v1"
CALLBACK_URL = "https://YOUR-NGROK-URL.ngrok-free.app"   # ← Har baar update karna

app = Flask(__name__)
results_cache = {}

def get_seniority_rank(title):
    if not title: return 999
    t = title.lower()
    if any(x in t for x in ['chief', 'cfo']): return 1
    if any(x in t for x in ['vp', 'vice president', 'svp']): return 2
    if any(x in t for x in ['director', 'head of']): return 3
    if any(x in t for x in ['senior manager', 'lead']): return 4
    if 'manager' in t: return 5
    return 6

# ====================== FLASK CALLBACK ======================
@app.route('/', methods=['POST'])
def handle_callback():
    try:
        data = request.get_json(force=True)
        items = data if isinstance(data, list) else [data]
        
        for item in items:
            if item.get("status") != "success": continue
            cand = item.get("candidate", {})
            name = cand.get("fullName", "N/A")
            
            # Latest experience only (ended = null)
            exp = next((e for e in cand.get("experience", []) if e.get("ended") is None or e.get("current")), {})
            
            contacts = cand.get("contacts", [])
            emails = [f"{c['value']} ({c.get('subType','')})" for c in contacts 
                     if c.get("type","").upper() == "EMAIL" and "personal" not in c.get("subType","").lower()]
            phones = [f"{c['value']} ({c.get('subType','')})" for c in contacts 
                     if c.get("type","").upper() == "PHONE"]
            
            results_cache[name] = {
                "position": exp.get("position", "N/A"),
                "company": exp.get("company", "N/A"),
                "location": exp.get("location", "N/A"),
                "started": exp.get("started", "N/A"),
                "emails": emails,
                "phones": phones
            }
            print(f"\n✅ DETAILS RECEIVED FOR: {name}")
            print("   → Ab number dubara type karke full details dekh sakte ho\n")
    except:
        pass
    return {"status": "ok"}, 200

# Start Flask in background
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False), daemon=True).start()
time.sleep(2)

# ====================== MAIN ======================
print("=== SignalHire One-by-One Mode (Credit Safe) ===\n")

company = input("Enter Company Name: ").strip()

# Step 1: Search people
headers = {"apikey": API_KEY, "Content-Type": "application/json"}
payload = {
    "keywords": "finance OR treasury",
    "currentTitle": "CFO OR \"Vice President Finance\" OR Director OR Manager",
    "currentCompany": f"\"{company}\"",
    "size": 20
}
resp = requests.post(BASE_URL + "/candidate/searchByQuery", headers=headers, json=payload)
profiles = resp.json().get("profiles", [])

sorted_profiles = sorted(profiles, key=lambda p: get_seniority_rank(p.get("experience", [{}])[0].get("title", "")))[:10]

print(f"\nTop 10 Senior People in {company}:\n")
person_map = {}
uid_map = {}

for i, p in enumerate(sorted_profiles, 1):
    name = p.get("fullName", "N/A")
    title = p.get("experience", [{}])[0].get("title", "N/A")
    uid = p.get("uid")
    print(f"{i}. {name} - {title}")
    person_map[i] = {"name": name, "title": title}
    if uid:
        uid_map[i] = uid

print("\nInstructions:")
print("• Number (1-10) daalo → Sirf us person ke contacts ka request jayega")
print("• 30-90 seconds wait karo")
print("• Details aane ke baad number dubara daal sakte ho\n")

while True:
    choice = input("Enter number (1-10) or 'exit': ").strip()
    
    if choice.lower() == 'exit':
        break
    if not choice.isdigit() or int(choice) not in person_map:
        print("Invalid number!")
        continue
        
    num = int(choice)
    person = person_map[num]
    uid = uid_map.get(num)
    
    print(f"\n→ Selected: {person['name']} - {person['title']}")
    
    if person['name'] in results_cache:
        d = results_cache[person['name']]
        print("\nFULL DETAILS:")
        print(f"Name     : {person['name']}")
        print(f"Position : {d['position']}")
        print(f"Company  : {d['company']}")
        print(f"Location : {d['location']}")
        print(f"Started  : {d['started']}")
        print(f"Emails   : {', '.join(d['emails']) if d['emails'] else 'Not found'}")
        print(f"Phones   : {', '.join(d['phones']) if d['phones'] else 'Not found'}")
        print("-" * 60)
    elif uid:
        # Send request for ONLY this person
        payload = {"items": [uid], "callbackUrl": CALLBACK_URL}
        r = requests.post(BASE_URL + "/candidate/search", headers=headers, json=payload)
        print(f"Request sent (Status: {r.status_code}) → Waiting for callback...")
        print("30-90 seconds mein details aayenge...\n")
    else:
        print("No UID available.\n")