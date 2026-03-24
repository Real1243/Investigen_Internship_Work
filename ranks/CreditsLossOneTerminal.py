# We lose credits on this one but all the details are shown -->
import requests
import json
import time
import threading
from flask import Flask, request

API_KEY = "202.M3D7xK6FykhOIHuKoFGLLjMI8jwW"
BASE_URL = "https://www.signalhire.com/api/v1"
SEARCH_ENDPOINT = "/candidate/searchByQuery"
PERSON_ENDPOINT = "/candidate/search"

CALLBACK_URL = "https://uninwrapped-celinda-subcranially.ngrok-free.dev"  # ← PASTE YOUR CURRENT NGROK HTTPS URL HERE EVERY RUN

app = Flask(__name__)
results_cache = {}          # name → details

def get_seniority_rank(title):
    if not title: return 999
    title_lower = title.lower()
    if any(w in title_lower for w in ['chief', 'cfo', 'chief financial', 'chief treasury']): return 1
    if any(w in title_lower for w in ['vp', 'vice president', 'svp', 'evp']): return 2
    if any(w in title_lower for w in ['director', 'head of', 'group head']): return 3
    if any(w in title_lower for w in ['senior manager', 'lead', 'principal']): return 4
    if 'manager' in title_lower: return 5
    return 6

def search_finance_treasury(company_name, size=20):
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    payload = {
        "keywords": "finance OR treasury",
        "currentTitle": "CFO OR \"Vice President Finance\" OR \"Finance Director\" OR \"Treasury Director\" OR \"Group Treasurer\" OR Manager OR Director",
        "currentCompany": f"\"{company_name}\"",
        "size": size,
    }
    r = requests.post(BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload)
    if r.status_code != 200:
        print("Search error:", r.text)
        return []
    profiles = r.json().get("profiles", [])
    def get_title(p): return p.get("experience", [{}])[0].get("title", "") if p.get("experience") else ""
    return sorted(profiles, key=lambda p: get_seniority_rank(get_title(p)))[:10]

@app.route('/', methods=['POST', 'GET'])
def callback():
    print("\n" + "═"*80)
    print(f"CALLBACK RECEIVED {time.strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        data = request.get_json(force=True)
        items = data if isinstance(data, list) else [data]
        for item in items:
            if item.get("status") != "success": continue
            cand = item.get("candidate", {})
            name = cand.get("fullName", "N/A")
            
            # Latest exp only (ended null or current)
            exp = next((e for e in cand.get("experience", []) if e.get("ended") is None or e.get("current")), {})
            pos = exp.get("position", "N/A")
            co  = exp.get("company", "N/A")
            loc = exp.get("location", "N/A")
            start = exp.get("started", "N/A")
            
            contacts = cand.get("contacts", [])
            emails = [f"{c['value']} ({c.get('subType','')})" for c in contacts if c.get("type","").upper()=="EMAIL" and "personal" not in c.get("subType","").lower()]
            phones = [f"{c['value']} ({c.get('subType','')})" for c in contacts if c.get("type","").upper()=="PHONE"]
            
            results_cache[name] = {"pos":pos, "co":co, "loc":loc, "start":start, "emails":emails, "phones":phones}
            
            print(f"DETAILS READY → {name}")
            print("   Type the number to see full info!\n")
    except Exception as e:
        print("Callback error:", str(e))
    return {"status":"ok"}, 200

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    time.sleep(2)
    
    print("\nSignalHire Enricher - all in one terminal")
    company = input("Company name (e.g. HDFC Bank): ").strip()
    
    profiles = search_finance_treasury(company)
    if not profiles:
        print("No results.")
    else:
        print(f"\nTop 10 senior for {company}:\n")
        person_map = {}
        uids = []
        for i, p in enumerate(profiles, 1):
            name = p.get("fullName", "N/A")
            title = p.get("experience", [{}])[0].get("title", "N/A")
            uid = p.get("uid")
            print(f"{i}. {name} - {title}")
            person_map[i] = {"name":name, "title":title}
            if uid: uids.append(uid)
        
        if uids:
            print(f"\nRequesting contacts for {len(uids)} people...")
            headers = {"apikey": API_KEY, "Content-Type": "application/json"}
            payload = {"items": uids, "callbackUrl": CALLBACK_URL}
            resp = requests.post(BASE_URL + PERSON_ENDPOINT, headers=headers, json=payload)
            print(f"Status: {resp.status_code} | {resp.text}")
            print("Waiting for callbacks... details will print here automatically.\n")
        
        while True:
            inp = input("Number (1-10) or 'exit': ").strip()
            if inp.lower() == 'exit': break
            if not inp.isdigit() or int(inp) not in person_map:
                print("Invalid, try 1-10 or 'exit'")
                continue
            num = int(inp)
            p = person_map[num]
            print(f"\n{p['name']} - {p['title']}")
            if p['name'] in results_cache:
                d = results_cache[p['name']]
                print("Current experience (ended=null):")
                print(f"  Position: {d['pos']}")
                print(f"  Company : {d['co']}")
                print(f"  Location: {d['loc']}")
                print(f"  Started : {d['start']}")
                print("\nWork emails:")
                print("  " + "\n  ".join(d['emails']) if d['emails'] else "None")
                print("\nPhones:")
                print("  " + "\n  ".join(d['phones']) if d['phones'] else "None")
                print("─"*60)
            else:
                print("Not received yet. Wait a bit and try again.")

