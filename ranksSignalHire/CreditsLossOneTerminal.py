# # We lose credits on this one but all the details are shown -->
# import requests
# import json
# import time
# import threading
# from flask import Flask, request

# API_KEY = "202.M3D7xK6FykhOIHuKoFGLLjMI8jwW"
# BASE_URL = "https://www.signalhire.com/api/v1"
# SEARCH_ENDPOINT = "/candidate/searchByQuery"
# PERSON_ENDPOINT = "/candidate/search"

# CALLBACK_URL = "https://uninwrapped-celinda-subcranially.ngrok-free.dev"  # ← PASTE YOUR CURRENT NGROK HTTPS URL HERE EVERY RUN

# app = Flask(__name__)
# results_cache = {}          # name → details

# def get_seniority_rank(title):
#     if not title: return 999
#     title_lower = title.lower()
#     if any(w in title_lower for w in ['chief', 'cfo', 'chief financial', 'chief treasury']): return 1
#     if any(w in title_lower for w in ['vp', 'vice president', 'svp', 'evp']): return 2
#     if any(w in title_lower for w in ['director', 'head of', 'group head']): return 3
#     if any(w in title_lower for w in ['senior manager', 'lead', 'principal']): return 4
#     if 'manager' in title_lower: return 5
#     return 6

# def search_finance_treasury(company_name, size=20):
#     headers = {"apikey": API_KEY, "Content-Type": "application/json"}
#     payload = {
#         "keywords": "finance OR treasury",
#         "currentTitle": "CFO OR \"Vice President Finance\" OR \"Finance Director\" OR \"Treasury Director\" OR \"Group Treasurer\" OR Manager OR Director",
#         "currentCompany": f"\"{company_name}\"",
#         "size": size,
#     }
#     r = requests.post(BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload)
#     if r.status_code != 200:
#         print("Search error:", r.text)
#         return []
#     profiles = r.json().get("profiles", [])
#     def get_title(p): return p.get("experience", [{}])[0].get("title", "") if p.get("experience") else ""
#     return sorted(profiles, key=lambda p: get_seniority_rank(get_title(p)))[:10]

# @app.route('/', methods=['POST', 'GET'])
# def callback():
#     print("\n" + "═"*80)
#     print(f"CALLBACK RECEIVED {time.strftime('%Y-%m-%d %H:%M:%S')}")
#     try:
#         data = request.get_json(force=True)
#         items = data if isinstance(data, list) else [data]
#         for item in items:
#             if item.get("status") != "success": continue
#             cand = item.get("candidate", {})
#             name = cand.get("fullName", "N/A")
            
#             # Latest exp only (ended null or current)
#             exp = next((e for e in cand.get("experience", []) if e.get("ended") is None or e.get("current")), {})
#             pos = exp.get("position", "N/A")
#             co  = exp.get("company", "N/A")
#             loc = exp.get("location", "N/A")
#             start = exp.get("started", "N/A")
            
#             contacts = cand.get("contacts", [])
#             emails = [f"{c['value']} ({c.get('subType','')})" for c in contacts if c.get("type","").upper()=="EMAIL" and "personal" not in c.get("subType","").lower()]
#             phones = [f"{c['value']} ({c.get('subType','')})" for c in contacts if c.get("type","").upper()=="PHONE"]
            
#             results_cache[name] = {"pos":pos, "co":co, "loc":loc, "start":start, "emails":emails, "phones":phones}
            
#             print(f"DETAILS READY → {name}")
#             print("   Type the number to see full info!\n")
#     except Exception as e:
#         print("Callback error:", str(e))
#     return {"status":"ok"}, 200

# def run_flask():
#     app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# if __name__ == "__main__":
#     threading.Thread(target=run_flask, daemon=True).start()
#     time.sleep(2)
    
#     print("\nSignalHire Enricher - all in one terminal")
#     company = input("Company name (e.g. HDFC Bank): ").strip()
    
#     profiles = search_finance_treasury(company)
#     if not profiles:
#         print("No results.")
#     else:
#         print(f"\nTop 10 senior for {company}:\n")
#         person_map = {}
#         uids = []
#         for i, p in enumerate(profiles, 1):
#             name = p.get("fullName", "N/A")
#             title = p.get("experience", [{}])[0].get("title", "N/A")
#             uid = p.get("uid")
#             print(f"{i}. {name} - {title}")
#             person_map[i] = {"name":name, "title":title}
#             if uid: uids.append(uid)
        
#         if uids:
#             print(f"\nRequesting contacts for {len(uids)} people...")
#             headers = {"apikey": API_KEY, "Content-Type": "application/json"}
#             payload = {"items": uids, "callbackUrl": CALLBACK_URL}
#             resp = requests.post(BASE_URL + PERSON_ENDPOINT, headers=headers, json=payload)
#             print(f"Status: {resp.status_code} | {resp.text}")
#             print("Waiting for callbacks... details will print here automatically.\n")
        
#         while True:
#             inp = input("Number (1-10) or 'exit': ").strip()
#             if inp.lower() == 'exit': break
#             if not inp.isdigit() or int(inp) not in person_map:
#                 print("Invalid, try 1-10 or 'exit'")
#                 continue
#             num = int(inp)
#             p = person_map[num]
#             print(f"\n{p['name']} - {p['title']}")
#             if p['name'] in results_cache:
#                 d = results_cache[p['name']]
#                 print("Current experience (ended=null):")
#                 print(f"  Position: {d['pos']}")
#                 print(f"  Company : {d['co']}")
#                 print(f"  Location: {d['loc']}")
#                 print(f"  Started : {d['start']}")
#                 print("\nWork emails:")
#                 print("  " + "\n  ".join(d['emails']) if d['emails'] else "None")
#                 print("\nPhones:")
#                 print("  " + "\n  ".join(d['phones']) if d['phones'] else "None")
#                 print("─"*60)
#             else:
#                 print("Not received yet. Wait a bit and try again.")















# # We lose credits on this one but all the details are shown -->
# import requests
# import json
# import time
# import threading
# from flask import Flask, request

# API_KEY = "202.M3D7xK6FykhOIHuKoFGLLjMI8jwW"
# BASE_URL = "https://www.signalhire.com/api/v1"
# SEARCH_ENDPOINT = "/candidate/searchByQuery"
# PERSON_ENDPOINT = "/candidate/search"

# CALLBACK_URL = "https://uninwrapped-celinda-subcranially.ngrok-free.dev"

# app = Flask(__name__)
# results_cache = {}

# def get_seniority_rank(title):
#     if not title:
#         return 999
#     title_lower = title.lower()
    
#     # MAXIMUM STRICT FINANCE CHECK
#     finance_words = ['finance', 'treasury', 'cfo', 'chief financial', 'financial officer', 'group cfo']
#     if not any(word in title_lower for word in finance_words):
#         return 999  # Anything without finance/treasury is rejected
    
#     # Rank 1 - Highest (CFO level)
#     if any(w in title_lower for w in ['cfo', 'chief financial officer', 'chief treasury officer', 'group cfo']):
#         return 1
#     # Rank 2
#     if any(w in title_lower for w in ['svp', 'senior vice president', 'vp', 'vice president finance', 'dvp', 'avp']):
#         return 2
#     # Rank 3
#     if any(w in title_lower for w in ['director', 'finance director', 'treasury director', 'head of finance', 'head of treasury']):
#         return 3
#     # Rank 4
#     if any(w in title_lower for w in ['sgm', 'agm', 'dgm', 'general manager finance']):
#         return 4
#     # Rank 5
#     if any(w in title_lower for w in ['sm', 'senior manager finance', 'manager finance', 'dm', 'am']):
#         return 5
#     return 999


# def search_finance_treasury(company_name, size=15):
#     headers = {"apikey": API_KEY, "Content-Type": "application/json"}
#     payload = {
#         "keywords": "finance OR treasury",   # This forces only finance people
#         # MAXIMUM AGGRESSIVE TITLE FILTER
#         "currentTitle": "CFO OR \"Chief Financial Officer\" OR \"Group CFO\" OR "
#                         "SVP OR \"Senior Vice President Finance\" OR \"Vice President Finance\" OR "
#                         "Director OR \"Finance Director\" OR \"Treasury Director\" OR "
#                         "\"Head of Finance\" OR \"Head of Treasury\" OR SGM OR AGM OR DGM OR "
#                         "\"Senior Manager Finance\" OR \"Finance Manager\"",
#         "currentCompany": f"\"{company_name}\"",
#         "size": size,
#     }
#     r = requests.post(BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload)
#     if r.status_code != 200:
#         print("Search error:", r.text)
#         return []
    
#     profiles = r.json().get("profiles", [])
    
#     # === FINAL DANGEROUSLY STRICT FILTER (This is the killer part) ===
#     strict_profiles = []
#     for p in profiles:
#         exp = p.get("experience", [{}])[0]
#         title = exp.get("title", "").lower()
#         ended = exp.get("ended")
#         is_current = exp.get("current")
        
#         # Must be CURRENT position + must have finance keyword
#         if (ended is None or is_current is True):
#             if any(k in title for k in ['finance', 'treasury', 'cfo', 'chief financial']) and \
#                not any(bad in title for bad in ['hr', 'human resource', 'marketing', 'sales', 'operations', 
#                                                 'it', 'information technology', 'legal', 'admin']):
#                 strict_profiles.append(p)
    
#     # Sort by strict rank
#     def get_title(p):
#         return p.get("experience", [{}])[0].get("title", "") if p.get("experience") else ""
    
#     sorted_profiles = sorted(strict_profiles, key=lambda p: get_seniority_rank(get_title(p)))
#     return sorted_profiles[:10]




# # ====================== REST OF YOUR CODE (UNCHANGED) ======================
# @app.route('/', methods=['POST', 'GET'])
# def callback():
#     print("\n" + "═"*80)
#     print(f"CALLBACK RECEIVED {time.strftime('%Y-%m-%d %H:%M:%S')}")
#     try:
#         data = request.get_json(force=True)
#         items = data if isinstance(data, list) else [data]
#         for item in items:
#             if item.get("status") != "success": continue
#             cand = item.get("candidate", {})
#             name = cand.get("fullName", "N/A")
           
#             exp = next((e for e in cand.get("experience", []) if e.get("ended") is None or e.get("current")), {})
#             pos = exp.get("position", "N/A")
#             co = exp.get("company", "N/A")
#             loc = exp.get("location", "N/A")
#             start = exp.get("started", "N/A")
           
#             contacts = cand.get("contacts", [])
#             emails = [f"{c['value']} ({c.get('subType','')})" for c in contacts if c.get("type","").upper()=="EMAIL" and "personal" not in c.get("subType","").lower()]
#             phones = [f"{c['value']} ({c.get('subType','')})" for c in contacts if c.get("type","").upper()=="PHONE"]
           
#             results_cache[name] = {"pos":pos, "co":co, "loc":loc, "start":start, "emails":emails, "phones":phones}
           
#             print(f"DETAILS READY → {name}")
#             print(" Type the number to see full info!\n")
#     except Exception as e:
#         print("Callback error:", str(e))
#     return {"status":"ok"}, 200

# def run_flask():
#     app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# if __name__ == "__main__":
#     threading.Thread(target=run_flask, daemon=True).start()
#     time.sleep(2)
   
#     print("\nSignalHire Enricher - all in one terminal")
#     company = input("Company name (e.g. HDFC Bank): ").strip()
   
#     profiles = search_finance_treasury(company)
#     if not profiles:
#         print("No results.")
#     else:
#         print(f"\nTop 10 senior for {company}:\n")
#         person_map = {}
#         uids = []
#         for i, p in enumerate(profiles, 1):
#             name = p.get("fullName", "N/A")
#             title = p.get("experience", [{}])[0].get("title", "N/A")
#             uid = p.get("uid")
#             print(f"{i}. {name} - {title}")
#             person_map[i] = {"name":name, "title":title}
#             if uid: uids.append(uid)
       
#         if uids:
#             print(f"\nRequesting contacts for {len(uids)} people...")
#             headers = {"apikey": API_KEY, "Content-Type": "application/json"}
#             payload = {"items": uids, "callbackUrl": CALLBACK_URL}
#             resp = requests.post(BASE_URL + PERSON_ENDPOINT, headers=headers, json=payload)
#             print(f"Status: {resp.status_code} | {resp.text}")
#             print("Waiting for callbacks... details will print here automatically.\n")
       
#         while True:
#             inp = input("Number (1-10) or 'exit': ").strip()
#             if inp.lower() == 'exit': break
#             if not inp.isdigit() or int(inp) not in person_map:
#                 print("Invalid, try 1-10 or 'exit'")
#                 continue
#             num = int(inp)
#             p = person_map[num]
#             print(f"\n{p['name']} - {p['title']}")
#             if p['name'] in results_cache:
#                 d = results_cache[p['name']]
#                 print("Current experience (ended=null):")
#                 print(f" Position: {d['pos']}")
#                 print(f" Company : {d['co']}")
#                 print(f" Location: {d['loc']}")
#                 print(f" Started : {d['start']}")
#                 print("\nWork emails:")
#                 print(" " + "\n ".join(d['emails']) if d['emails'] else "None")
#                 print("\nPhones:")
#                 print(" " + "\n ".join(d['phones']) if d['phones'] else "None")
#                 print("─"*60)
#             else:
#                 print("Not received yet. Wait a bit and try again.")




# this is the one ok

# We lose credits on this one but all the details are shown -->
# ULTRA STRICT + TOP 5 ONLY (Max 5 credits used)

# import requests
# import json
# import time
# import threading
# from flask import Flask, request

# API_KEY = "202.M3D7xK6FykhOIHuKoFGLLjMI8jwW"
# BASE_URL = "https://www.signalhire.com/api/v1"
# SEARCH_ENDPOINT = "/candidate/searchByQuery"
# PERSON_ENDPOINT = "/candidate/search"

# CALLBACK_URL = "https://uninwrapped-celinda-subcranially.ngrok-free.dev"

# app = Flask(__name__)
# results_cache = {}

# def get_seniority_rank(title):
#     if not title:
#         return 999
#     title_lower = title.lower()
    
#     # EXTREME FINANCE CHECK - no finance/treasury word = rejected immediately
#     if not any(word in title_lower for word in ['finance', 'treasury', 'cfo', 'chief financial']):
#         return 999
    
#     # Rank 1 - CFO level only
#     if any(w in title_lower for w in ['cfo', 'chief financial officer', 'group cfo']):
#         return 1
#     # Rank 2
#     if any(w in title_lower for w in ['svp', 'senior vice president', 'vp', 'vice president finance']):
#         return 2
#     # Rank 3
#     if any(w in title_lower for w in ['director', 'finance director', 'head of finance']):
#         return 3
#     # Rank 4
#     if any(w in title_lower for w in ['sgm', 'agm', 'dgm', 'general manager finance']):
#         return 4
#     # Rank 5
#     if any(w in title_lower for w in ['senior manager finance', 'finance manager']):
#         return 5
#     return 999


# def search_finance_treasury(company_name, size=12):
#     headers = {"apikey": API_KEY, "Content-Type": "application/json"}
#     payload = {
#         "keywords": "finance OR treasury",
#         "currentTitle": "CFO OR \"Chief Financial Officer\" OR SVP OR \"Senior Vice President\" OR "
#                         "\"Vice President Finance\" OR \"Finance Director\" OR \"Head of Finance\" OR "
#                         "SGM OR AGM OR DGM OR \"Senior Manager Finance\"",
#         "currentCompany": f"\"{company_name}\"",
#         "size": size,
#     }
#     r = requests.post(BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload)
#     if r.status_code != 200:
#         print("Search error:", r.text)
#         return []
    
#     profiles = r.json().get("profiles", [])
    
#     # MAXIMUM STRICT FILTER (This is the strongest possible)
#     strict_profiles = []
#     for p in profiles:
#         exp = p.get("experience", [{}])[0]
#         title = exp.get("title", "").lower()
#         is_current = (exp.get("ended") is None or exp.get("current") is True)
        
#         # Must be CURRENT position + must contain finance keyword + no bad departments
#         if is_current and any(k in title for k in ['finance', 'treasury', 'cfo']):
#             if not any(bad in title for bad in ['hr', 'human', 'marketing', 'sales', 'operations', 
#                                                 'it', 'legal', 'admin', 'public relation']):
#                 strict_profiles.append(p)
    
#     def get_title(p):
#         return p.get("experience", [{}])[0].get("title", "") if p.get("experience") else ""
    
#     sorted_profiles = sorted(strict_profiles, key=lambda p: get_seniority_rank(get_title(p)))
#     return sorted_profiles[:5]   # Locked at 5 only

# # ====================== REST OF YOUR CODE (UNCHANGED) ======================
# @app.route('/', methods=['POST', 'GET'])
# def callback():
#     print("\n" + "═"*80)
#     print(f"CALLBACK RECEIVED {time.strftime('%Y-%m-%d %H:%M:%S')}")
#     try:
#         data = request.get_json(force=True)
#         items = data if isinstance(data, list) else [data]
#         for item in items:
#             if item.get("status") != "success": continue
#             cand = item.get("candidate", {})
#             name = cand.get("fullName", "N/A")
           
#             exp = next((e for e in cand.get("experience", []) if e.get("ended") is None or e.get("current")), {})
#             pos = exp.get("position", "N/A")
#             co = exp.get("company", "N/A")
#             loc = exp.get("location", "N/A")
#             start = exp.get("started", "N/A")
           
#             contacts = cand.get("contacts", [])
#             emails = [f"{c['value']} ({c.get('subType','')})" for c in contacts if c.get("type","").upper()=="EMAIL" and "personal" not in c.get("subType","").lower()]
#             phones = [f"{c['value']} ({c.get('subType','')})" for c in contacts if c.get("type","").upper()=="PHONE"]
           
#             results_cache[name] = {"pos":pos, "co":co, "loc":loc, "start":start, "emails":emails, "phones":phones}
           
#             print(f"DETAILS READY → {name}")
#             print(" Type the number to see full info!\n")
#     except Exception as e:
#         print("Callback error:", str(e))
#     return {"status":"ok"}, 200

# def run_flask():
#     app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# if __name__ == "__main__":
#     threading.Thread(target=run_flask, daemon=True).start()
#     time.sleep(2)
   
#     print("\nSignalHire Enricher - ULTRA STRICT MODE (Top 5 only)")
#     company = input("Company name (e.g. HDFC Bank): ").strip()
   
#     profiles = search_finance_treasury(company)
#     if not profiles:
#         print("No results.")
#     else:
#         print(f"\nTop 5 senior for {company}:\n")
#         person_map = {}
#         uids = []
#         for i, p in enumerate(profiles, 1):
#             name = p.get("fullName", "N/A")
#             title = p.get("experience", [{}])[0].get("title", "N/A")
#             uid = p.get("uid")
#             print(f"{i}. {name} - {title}")
#             person_map[i] = {"name":name, "title":title}
#             if uid: uids.append(uid)
       
#         if uids:
#             print(f"\nRequesting contacts for {len(uids)} people (max 5 credits)...")
#             headers = {"apikey": API_KEY, "Content-Type": "application/json"}
#             payload = {"items": uids, "callbackUrl": CALLBACK_URL}
#             resp = requests.post(BASE_URL + PERSON_ENDPOINT, headers=headers, json=payload)
#             print(f"Status: {resp.status_code} | {resp.text}")
#             print("Waiting for callbacks... details will print here automatically.\n")
       
#         while True:
#             inp = input("Number (1-5) or 'exit': ").strip()
#             if inp.lower() == 'exit': break
#             if not inp.isdigit() or int(inp) not in person_map:
#                 print("Invalid, try 1-5 or 'exit'")
#                 continue
#             num = int(inp)
#             p = person_map[num]
#             print(f"\n{p['name']} - {p['title']}")
#             if p['name'] in results_cache:
#                 d = results_cache[p['name']]
#                 print("Current experience (ended=null):")
#                 print(f" Position: {d['pos']}")
#                 print(f" Company : {d['co']}")
#                 print(f" Location: {d['loc']}")
#                 print(f" Started : {d['start']}")
#                 print("\nWork emails:")
#                 print(" " + "\n ".join(d['emails']) if d['emails'] else "None")
#                 print("\nPhones:")
#                 print(" " + "\n ".join(d['phones']) if d['phones'] else "None")
#                 print("─"*60)
#             else:
#                 print("Not received yet. Wait a bit and try again.")


























# import requests
# import json
# import time
# import threading
# from flask import Flask, request

# API_KEY = "202.M3D7xK6FykhOIHuKoFGLLjMI8jwW"
# BASE_URL = "https://www.signalhire.com/api/v1"
# SEARCH_ENDPOINT = "/candidate/searchByQuery"
# PERSON_ENDPOINT = "/candidate/search"

# CALLBACK_URL = "https://uninwrapped-celinda-subcranially.ngrok-free.dev"

# app = Flask(__name__)
# results_cache = {}

# def get_seniority_rank(title):
#     if not title:
#         return 999

#     t = title.lower()

#     if any(x in t for x in ['cfo', 'chief financial officer', 'group cfo']):
#         return 1

#     if any(x in t for x in ['svp', 'senior vice president']):
#         return 2

#     if any(x in t for x in ['vp', 'vice president', 'avp', 'assistant vice president', 'dvp']):
#         return 3

#     if any(x in t for x in ['director', 'finance director', 'treasury director', 'head']):
#         return 4

#     if any(x in t for x in ['sgm', 'gm', 'dgm', 'agm', 'general manager']):
#         return 5

#     if any(x in t for x in ['senior manager']):
#         return 6

#     if any(x in t for x in ['manager', 'am', 'dm']):
#         return 7

#     return 999



# # 🔥 STRONG SENIORITY LOGIC
# def search_finance_treasury(company_name, size=40):
#     headers = {"apikey": API_KEY, "Content-Type": "application/json"}

#     # 🔥 PRIMARY SEARCH
#     payload = {
#         "keywords": "finance OR treasury OR accounts OR FP&A OR audit OR controller",
#         "currentCompany": f"\"{company_name}\"",
#         "size": size,
#     }

#     r = requests.post(BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload)

#     if r.status_code != 200:
#         print("Search error:", r.text)
#         return []

#     profiles = r.json().get("profiles", [])

#     # 🔥 FALLBACK IF EMPTY
#     if not profiles:
#         print("⚠️ No data → retrying broader search...")
#         payload["keywords"] = "finance OR accounts OR treasury OR manager"
#         r = requests.post(BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload)
#         profiles = r.json().get("profiles", [])

#     if not profiles:
#         return []

#     # ================= FILTERS =================
#     indian_keywords = [
#         'india', 'mumbai', 'delhi', 'bangalore', 'pune',
#         'hyderabad', 'chennai', 'navi mumbai',
#         'ahmedabad', 'kolkata', 'gurgaon', 'noida'
#     ]

#     finance_keywords = [
#         'finance', 'treasury', 'accounts', 'fp&a',
#         'financial', 'controller', 'audit'
#     ]

#     strict_titles = [
#         'cfo', 'chief financial officer',
#         'finance director', 'treasury director',
#         'head of finance', 'finance head',
#         'financial controller', 'group cfo'
#     ]

#     bad_keywords = [
#         'hr', 'human resources', 'marketing',
#         'sales', 'legal', 'recruitment'
#     ]

#     strict = []
#     medium = []

#     for p in profiles:
#         exp = p.get("experience", [{}])[0]

#         title = exp.get("title", "").lower()
#         location = exp.get("location", "").lower()
#         is_current = (exp.get("ended") is None or exp.get("current") is True)

#         if not is_current:
#             continue

#         # ❌ remove junk roles
#         if any(bad in title for bad in bad_keywords):
#             continue

#         # ❌ STRICT FINANCE ONLY
#         if not any(fin in title for fin in finance_keywords):
#             continue

#         # ❌ India filter (but allow blank)
#         if location and not (
#             any(city in location for city in indian_keywords) or 'india' in location
#         ):
#             continue

#         # ✅ BUCKETING (FIXED - INSIDE LOOP)
#         if any(x in title for x in strict_titles):
#             strict.append(p)
#         else:
#             medium.append(p)

#     # 🔥 FINAL SELECTION LOGIC
#     final = strict if len(strict) >= 3 else strict + medium

#     # 🚀 LAST FALLBACK (NEVER EMPTY)
#     if not final:
#         print("⚠️ Using raw fallback (no strict finance found)")
#         final = profiles

#     def get_title(p):
#         return p.get("experience", [{}])[0].get("title", "")

#     sorted_profiles = sorted(
#         final,
#         key=lambda p: get_seniority_rank(get_title(p))
#     )

#     return sorted_profiles[:10]

# # ====================== REST SAME ======================
# @app.route('/', methods=['POST', 'GET'])
# def callback():
#     print("\n" + "═"*80)
#     print(f"CALLBACK RECEIVED {time.strftime('%Y-%m-%d %H:%M:%S')}")

#     try:
#         data = request.get_json(force=True)
#         items = data if isinstance(data, list) else [data]

#         for item in items:
#             if item.get("status") != "success":
#                 continue

#             cand = item.get("candidate", {})
#             name = cand.get("fullName", "N/A")

#             exp = next(
#                 (e for e in cand.get("experience", [])
#                  if e.get("ended") is None or e.get("current")),
#                 {}
#             )

#             pos = exp.get("position", "N/A")
#             co = exp.get("company", "N/A")
#             loc = exp.get("location", "N/A")
#             start = exp.get("started", "N/A")

#             contacts = cand.get("contacts", [])

#             emails = [
#                 f"{c['value']} ({c.get('subType','')})"
#                 for c in contacts
#                 if c.get("type","").upper()=="EMAIL"
#                 and "personal" not in c.get("subType","").lower()
#             ]

#             phones = [
#                 f"{c['value']} ({c.get('subType','')})"
#                 for c in contacts
#                 if c.get("type","").upper()=="PHONE"
#             ]

#             results_cache[name] = {
#                 "pos":pos, "co":co, "loc":loc,
#                 "start":start, "emails":emails, "phones":phones
#             }

#             print(f"DETAILS READY → {name}")
#             print(" Type the number to see full info!\n")

#     except Exception as e:
#         print("Callback error:", str(e))

#     return {"status":"ok"}, 200


# def run_flask():
#     app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)


# if __name__ == "__main__":
#     threading.Thread(target=run_flask, daemon=True).start()
#     time.sleep(2)

#     print("\nSignalHire Enricher - TOP 10 (STRICT FINANCE + INDIA)")
#     company = input("Company name: ").strip()

#     profiles = search_finance_treasury(company)

#     if not profiles:
#         print("No accurate finance profiles found.")
#         print("Small startups often don’t have structured data in SignalHire.")
#     else:
#         print(f"\nTop 10 senior finance people for {company}:\n")

#         person_map = {}
#         uids = []

#         for i, p in enumerate(profiles, 1):
#             name = p.get("fullName", "N/A")
#             title = p.get("experience", [{}])[0].get("title", "N/A")
#             uid = p.get("uid")

#             print(f"{i}. {name} - {title}")

#             person_map[i] = {"name":name, "title":title}
#             if uid:
#                 uids.append(uid)

#         if uids:
#             print(f"\nRequesting contacts for {len(uids)} people...")
#             headers = {"apikey": API_KEY, "Content-Type": "application/json"}
#             payload = {"items": uids, "callbackUrl": CALLBACK_URL}
#             resp = requests.post(BASE_URL + PERSON_ENDPOINT, headers=headers, json=payload)
#             print(f"Status: {resp.status_code} | {resp.text}")
#             print("Waiting for callbacks...\n")

#         while True:
#             inp = input("Number (1-10) or 'exit': ").strip()

#             if inp.lower() == 'exit':
#                 break

#             if not inp.isdigit() or int(inp) not in person_map:
#                 print("Invalid, try 1-10 or 'exit'")
#                 continue

#             num = int(inp)
#             p = person_map[num]

#             print(f"\n{p['name']} - {p['title']}")

#             if p['name'] in results_cache:
#                 d = results_cache[p['name']]

#                 print("Current experience:")
#                 print(f" Position: {d['pos']}")
#                 print(f" Company : {d['co']}")
#                 print(f" Location: {d['loc']}")
#                 print(f" Started : {d['start']}")

#                 print("\nWork emails:")
#                 print(" " + "\n ".join(d['emails']) if d['emails'] else "None")

#                 print("\nPhones:")
#                 print(" " + "\n ".join(d['phones']) if d['phones'] else "None")

#                 print("─"*60)
#             else:
#                 print("Not received yet. Wait a bit and try again.")








# import requests
# import json
# import time
# import threading
# from flask import Flask, request

# API_KEY = "202.M3D7xK6FykhOIHuKoFGLLjMI8jwW"
# BASE_URL = "https://www.signalhire.com/api/v1"
# SEARCH_ENDPOINT = "/candidate/searchByQuery"
# PERSON_ENDPOINT = "/candidate/search"

# CALLBACK_URL = "https://uninwrapped-celinda-subcranially.ngrok-free.dev"

# app = Flask(__name__)
# results_cache = {}

# def get_seniority_rank(title):
#     if not title:
#         return 999

#     t = title.lower()

#     if any(x in t for x in ['cfo', 'chief financial officer', 'group cfo']):
#         return 1

#     if any(x in t for x in ['svp', 'senior vice president']):
#         return 2

#     if any(x in t for x in ['vp', 'vice president', 'avp', 'assistant vice president', 'dvp']):
#         return 3

#     if any(x in t for x in ['director', 'finance director', 'treasury director', 'head']):
#         return 4

#     if any(x in t for x in ['sgm', 'gm', 'dgm', 'agm', 'general manager']):
#         return 5

#     if any(x in t for x in ['senior manager']):
#         return 6

#     if any(x in t for x in ['manager', 'am', 'dm']):
#         return 7

#     return 999



# # 🔥 STRONG SENIORITY LOGIC
# def search_finance_treasury(company_name, size=40):
#     headers = {"apikey": API_KEY, "Content-Type": "application/json"}

#     # 🔥 PRIMARY SEARCH
#     payload = {
#         "keywords": "finance OR treasury OR accounts OR FP&A OR audit OR controller",
#         "currentCompany": f"\"{company_name}\"",
#         "size": size,
#     }

#     r = requests.post(BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload)

#     if r.status_code != 200:
#         print("Search error:", r.text)
#         return []

#     profiles = r.json().get("profiles", [])

#     # 🔥 FALLBACK IF EMPTY
#     if not profiles:
#         print("⚠️ No data → retrying broader search...")
#         payload["keywords"] = "finance OR accounts OR treasury OR manager"
#         r = requests.post(BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload)
#         profiles = r.json().get("profiles", [])

#     if not profiles:
#         return []

#     # ================= FILTERS =================
#     indian_keywords = [
#         'india', 'mumbai', 'delhi', 'bangalore', 'pune',
#         'hyderabad', 'chennai', 'navi mumbai',
#         'ahmedabad', 'kolkata', 'gurgaon', 'noida'
#     ]

#     finance_keywords = [
#         'finance', 'treasury', 'accounts', 'fp&a',
#         'financial', 'controller', 'audit'
#     ]

#     strict_titles = [
#         'cfo', 'chief financial officer',
#         'finance director', 'treasury director',
#         'head of finance', 'finance head',
#         'financial controller', 'group cfo'
#     ]

#     bad_keywords = [
#         'hr', 'human resources', 'marketing',
#         'sales', 'legal', 'recruitment'
#     ]

#     strict = []
#     medium = []

#     for p in profiles:
#         exp = p.get("experience", [{}])[0]

#         title = exp.get("title", "").lower()
#         location = exp.get("location", "").lower()
#         is_current = (exp.get("ended") is None or exp.get("current") is True)

#         if not is_current:
#             continue

#         # ❌ remove junk roles
#         if any(bad in title for bad in bad_keywords):
#             continue

#         # ❌ STRICT FINANCE ONLY
#         if not any(fin in title for fin in finance_keywords):
#             continue

#         # ❌ India filter (but allow blank)
#         if not location:
#             continue  # remove profiles with no location

#         if not (
#             'india' in location or
#             any(city in location for city in indian_keywords)
#         ):
#             continue

#         # ✅ BUCKETING (FIXED - INSIDE LOOP)
#         if any(x in title for x in strict_titles):
#             strict.append(p)
#         else:
#             medium.append(p)

#     # 🔥 FINAL SELECTION LOGIC
#     final = strict if len(strict) >= 3 else strict + medium

#     # 🚀 LAST FALLBACK (NEVER EMPTY)
#     if not final:
#         print("⚠️ Using raw fallback (no strict finance found)")
#         final = profiles

#     def get_title(p):
#         return p.get("experience", [{}])[0].get("title", "")

#     sorted_profiles = sorted(
#         final,
#         key=lambda p: get_seniority_rank(get_title(p))
#     )

#     return sorted_profiles[:10]

# # ====================== REST SAME ======================
# @app.route('/', methods=['POST', 'GET'])
# def callback():
#     print("\n" + "═"*80)
#     print(f"CALLBACK RECEIVED {time.strftime('%Y-%m-%d %H:%M:%S')}")

#     try:
#         data = request.get_json(force=True)
#         items = data if isinstance(data, list) else [data]

#         for item in items:
#             if item.get("status") != "success":
#                 continue

#             cand = item.get("candidate", {})
#             name = cand.get("fullName", "N/A")

#             exp = next(
#                 (e for e in cand.get("experience", [])
#                  if e.get("ended") is None or e.get("current")),
#                 {}
#             )

#             pos = exp.get("position", "N/A")
#             co = exp.get("company", "N/A")
#             loc = exp.get("location", "N/A")
#             start = exp.get("started", "N/A")

#             contacts = cand.get("contacts", [])

#             emails = [
#                 f"{c['value']} ({c.get('subType','')})"
#                 for c in contacts
#                 if c.get("type","").upper()=="EMAIL"
#                 and "personal" not in c.get("subType","").lower()
#             ]

#             phones = [
#                 f"{c['value']} ({c.get('subType','')})"
#                 for c in contacts
#                 if c.get("type","").upper()=="PHONE"
#             ]

#             results_cache[name] = {
#                 "pos":pos, "co":co, "loc":loc,
#                 "start":start, "emails":emails, "phones":phones
#             }

#             print(f"DETAILS READY → {name}")
#             print(" Type the number to see full info!\n")

#     except Exception as e:
#         print("Callback error:", str(e))

#     return {"status":"ok"}, 200


# def run_flask():
#     app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)


# if __name__ == "__main__":
#     threading.Thread(target=run_flask, daemon=True).start()
#     time.sleep(2)

#     print("\nSignalHire Enricher - TOP 10 (STRICT FINANCE + INDIA)")
#     company = input("Company name: ").strip()

#     profiles = search_finance_treasury(company)

#     if not profiles:
#         print("No accurate finance profiles found.")
#         print("Small startups often don’t have structured data in SignalHire.")
#     else:
#         print(f"\nTop 10 senior finance people for {company}:\n")

#         person_map = {}
#         uids = []

#         for i, p in enumerate(profiles, 1):
#             name = p.get("fullName", "N/A")
#             title = p.get("experience", [{}])[0].get("title", "N/A")
#             uid = p.get("uid")

#             print(f"{i}. {name} - {title}")

#             person_map[i] = {"name":name, "title":title}
#             if uid:
#                 uids.append(uid)

#         if uids:
#             print(f"\nRequesting contacts for {len(uids)} people...")
#             headers = {"apikey": API_KEY, "Content-Type": "application/json"}
#             payload = {"items": uids, "callbackUrl": CALLBACK_URL}
#             resp = requests.post(BASE_URL + PERSON_ENDPOINT, headers=headers, json=payload)
#             print(f"Status: {resp.status_code} | {resp.text}")
#             print("Waiting for callbacks...\n")

#         while True:
#             inp = input("Number (1-10) or 'exit': ").strip()

#             if inp.lower() == 'exit':
#                 break

#             if not inp.isdigit() or int(inp) not in person_map:
#                 print("Invalid, try 1-10 or 'exit'")
#                 continue

#             num = int(inp)
#             p = person_map[num]

#             print(f"\n{p['name']} - {p['title']}")

#             if p['name'] in results_cache:
#                 d = results_cache[p['name']]

#                 print("Current experience:")
#                 print(f" Position: {d['pos']}")
#                 print(f" Company : {d['co']}")
#                 print(f" Location: {d['loc']}")
#                 print(f" Started : {d['start']}")

#                 print("\nWork emails:")
#                 print(" " + "\n ".join(d['emails']) if d['emails'] else "None")

#                 print("\nPhones:")
#                 print(" " + "\n ".join(d['phones']) if d['phones'] else "None")

#                 print("─"*60)
#             else:
#                 print("Not received yet. Wait a bit and try again.")




































# import requests
# import json
# import time
# import threading
# from flask import Flask, request

# API_KEY = "202.M3D7xK6FykhOIHuKoFGLLjMI8jwW"
# BASE_URL = "https://www.signalhire.com/api/v1"
# SEARCH_ENDPOINT = "/candidate/searchByQuery"
# PERSON_ENDPOINT = "/candidate/search"

# CALLBACK_URL = "https://uninwrapped-celinda-subcranially.ngrok-free.dev"

# app = Flask(__name__)
# results_cache = {}

# def get_seniority_rank(title):
#     if not title:
#         return 999

#     t = title.lower()

#     if any(x in t for x in ['cfo', 'chief financial officer', 'group cfo']):
#         return 1

#     if any(x in t for x in ['svp', 'senior vice president']):
#         return 2

#     if any(x in t for x in ['vp', 'vice president', 'avp', 'assistant vice president', 'dvp']):
#         return 3

#     if any(x in t for x in ['director', 'finance director', 'treasury director', 'head']):
#         return 4

#     if any(x in t for x in ['sgm', 'gm', 'dgm', 'agm', 'general manager']):
#         return 5

#     if any(x in t for x in ['senior manager']):
#         return 6

#     if any(x in t for x in ['manager', 'am', 'dm']):
#         return 7

#     return 999



# # 🔥 STRONG SENIORITY LOGIC
# def search_finance_treasury(company_name, size=40):
#     headers = {"apikey": API_KEY, "Content-Type": "application/json"}

#     # 🔥 PRIMARY SEARCH
#     payload = {
#         "keywords": "finance OR financial OR treasury OR accounting OR FP&A OR controller OR audit OR tax OR compliance OR risk",
#         "currentCompany": f"\"{company_name}\"",
#         "size": size,
#     }

#     r = requests.post(BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload)

#     if r.status_code != 200:
#         print("Search error:", r.text)
#         return []

#     profiles = r.json().get("profiles", [])

#     # 🔥 FALLBACK IF EMPTY
#     if not profiles:
#         print("⚠️ No data → retrying broader search...")
#         payload["keywords"] = "finance OR accounts OR treasury OR manager"
#         r = requests.post(BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload)
#         profiles = r.json().get("profiles", [])

#     if not profiles:
#         return []

#     # ================= FILTERS =================
#     indian_keywords = [
#         'india', 'mumbai', 'delhi', 'bangalore', 'pune',
#         'hyderabad', 'chennai', 'navi mumbai',
#         'ahmedabad', 'kolkata', 'gurgaon', 'noida'
#     ]

#     finance_keywords = [
#     'finance', 'financial', 'treasury',
#     'accounts', 'accounting',
#     'fp&a', 'controller',
#     'audit', 'tax',
#     'payroll', 'compliance',
#     'risk'
#     ]

#     strict_titles = [
#         'cfo', 'chief financial officer',
#         'finance director', 'treasury director',
#         'head of finance', 'finance head',
#         'financial controller', 'group cfo'
#     ]

#     bad_keywords = [
#         'hr', 'human resources', 'marketing',
#         'sales', 'legal', 'recruitment'
#     ]

#     strict = []
#     medium = []

#     for p in profiles:
#         exp = p.get("experience", [{}])[0]

#         title = exp.get("title", "").lower()
#         location = exp.get("location", "").lower()
#         is_current = (exp.get("ended") is None or exp.get("current") is True)

#         if not is_current:
#             continue

#         # ❌ remove junk roles
#         if any(bad in title for bad in bad_keywords):
#             continue

#         # ❌ STRICT FINANCE ONLY
#         if not any(fin in title for fin in finance_keywords):
#             continue

#         # ❌ India filter (but allow blank)
#         if not location:
#             continue  # remove profiles with no location

#         if not (
#             'india' in location or
#             any(city in location for city in indian_keywords)
#         ):
#             continue

#         # ✅ BUCKETING (FIXED - INSIDE LOOP)
#         if any(x in title for x in strict_titles):
#             strict.append(p)
#         else:
#             medium.append(p)

#     # 🔥 FINAL SELECTION LOGIC
#     final = strict if len(strict) >= 3 else strict + medium

#     # 🚀 LAST FALLBACK (NEVER EMPTY)
#     if not final:
#         print("⚠️ Using raw fallback (no strict finance found)")
#         final = profiles

#     def get_title(p):
#         return p.get("experience", [{}])[0].get("title", "")

#     sorted_profiles = sorted(
#         final,
#         key=lambda p: get_seniority_rank(get_title(p))
#     )

#     return sorted_profiles[:10]

# # ====================== REST SAME ======================
# @app.route('/', methods=['POST', 'GET'])
# def callback():
#     print("\n" + "═"*80)
#     print(f"CALLBACK RECEIVED {time.strftime('%Y-%m-%d %H:%M:%S')}")

#     try:
#         data = request.get_json(force=True)
#         items = data if isinstance(data, list) else [data]

#         for item in items:
#             if item.get("status") != "success":
#                 continue

#             cand = item.get("candidate", {})
#             name = cand.get("fullName", "N/A")

#             exp = next(
#                 (e for e in cand.get("experience", [])
#                  if e.get("ended") is None or e.get("current")),
#                 {}
#             )

#             pos = exp.get("position", "N/A")
#             co = exp.get("company", "N/A")
#             loc = exp.get("location", "N/A")
#             start = exp.get("started", "N/A")

#             contacts = cand.get("contacts", [])

#             emails = [
#                 f"{c['value']} ({c.get('subType','')})"
#                 for c in contacts
#                 if c.get("type","").upper()=="EMAIL"
#                 and "personal" not in c.get("subType","").lower()
#             ]

#             phones = [
#                 f"{c['value']} ({c.get('subType','')})"
#                 for c in contacts
#                 if c.get("type","").upper()=="PHONE"
#             ]

#             results_cache[name] = {
#                 "pos":pos, "co":co, "loc":loc,
#                 "start":start, "emails":emails, "phones":phones
#             }

#             print(f"DETAILS READY → {name}")
#             print(" Type the number to see full info!\n")

#     except Exception as e:
#         print("Callback error:", str(e))

#     return {"status":"ok"}, 200


# def run_flask():
#     app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)


# if __name__ == "__main__":
#     threading.Thread(target=run_flask, daemon=True).start()
#     time.sleep(2)

#     print("\nSignalHire Enricher - TOP 10 (STRICT FINANCE + INDIA)")
#     company = input("Company name: ").strip()

#     profiles = search_finance_treasury(company)

#     if not profiles:
#         print("No accurate finance profiles found.")
#         print("Small startups often don’t have structured data in SignalHire.")
#     else:
#         print(f"\nTop 10 senior finance people for {company}:\n")

#         person_map = {}
#         uids = []

#         for i, p in enumerate(profiles, 1):
#             name = p.get("fullName", "N/A")
#             title = p.get("experience", [{}])[0].get("title", "N/A")
#             uid = p.get("uid")

#             print(f"{i}. {name} - {title}")

#             person_map[i] = {"name":name, "title":title}
#             if uid:
#                 uids.append(uid)

#         if uids:
#             print(f"\nRequesting contacts for {len(uids)} people...")
#             headers = {"apikey": API_KEY, "Content-Type": "application/json"}
#             payload = {"items": uids, "callbackUrl": CALLBACK_URL}
#             resp = requests.post(BASE_URL + PERSON_ENDPOINT, headers=headers, json=payload)
#             print(f"Status: {resp.status_code} | {resp.text}")
#             print("Waiting for callbacks...\n")

#         while True:
#             inp = input("Number (1-10) or 'exit': ").strip()

#             if inp.lower() == 'exit':
#                 break

#             if not inp.isdigit() or int(inp) not in person_map:
#                 print("Invalid, try 1-10 or 'exit'")
#                 continue

#             num = int(inp)
#             p = person_map[num]

#             print(f"\n{p['name']} - {p['title']}")

#             if p['name'] in results_cache:
#                 d = results_cache[p['name']]

#                 print("Current experience:")
#                 print(f" Position: {d['pos']}")
#                 print(f" Company : {d['co']}")
#                 print(f" Location: {d['loc']}")
#                 print(f" Started : {d['start']}")

#                 print("\nWork emails:")
#                 print(" " + "\n ".join(d['emails']) if d['emails'] else "None")

#                 print("\nPhones:")
#                 print(" " + "\n ".join(d['phones']) if d['phones'] else "None")

#                 print("─"*60)
#             else:
#                 print("Not received yet. Wait a bit and try again.")













# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# import requests
# import json
# import time
# import threading
# from flask import Flask, request

# API_KEY = "202.M3D7xK6FykhOIHuKoFGLLjMI8jwW"
# BASE_URL = "https://www.signalhire.com/api/v1"
# SEARCH_ENDPOINT = "/candidate/searchByQuery"
# PERSON_ENDPOINT = "/candidate/search"

# CALLBACK_URL = "https://uninwrapped-celinda-subcranially.ngrok-free.dev"

# app = Flask(__name__)
# results_cache = {}

# # ================= SENIORITY =================
# def get_seniority_rank(title):
#     if not title:
#         return 999

#     t = title.lower()

#     if any(x in t for x in ['cfo', 'chief financial officer', 'group cfo']):
#         return 1
#     if any(x in t for x in ['svp', 'senior vice president']):
#         return 2
#     if any(x in t for x in ['vp', 'vice president', 'avp', 'assistant vice president', 'dvp', 'deputy vice president']):
#         return 3
#     if any(x in t for x in ['director', 'finance director', 'treasury director', 'head']):
#         return 4
#     if any(x in t for x in ['sgm', 'senior general manager', 'gm', 'general manager', 'dgm', 'deputy general manager', 'agm', 'assistant general manager', 'general manager']):
#         return 5
#     if 'senior manager' in t:
#         return 6
#     if any(x in t for x in ['manager']):
#         return 7

#     return 999


# # ================= MAIN SEARCH =================
# def search_finance_treasury(company_name, size=80):
#     headers = {"apikey": API_KEY, "Content-Type": "application/json"}

#     payload = {
#     "keywords": f"{company_name} AND (finance OR financial OR treasury OR accounting OR FP&A)",
#     "size": size,
#     }  

#     r = requests.post(BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload)

#     if r.status_code != 200:
#         print("Search error:", r.text)
#         return []

#     profiles = r.json().get("profiles", [])

#     # fallback search (still finance-only)
#     if not profiles:
#         print("⚠️ No data → retrying broader finance search...")
#         payload["keywords"] = "finance OR accounts OR treasury OR audit OR tax"
#         r = requests.post(BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload)
#         profiles = r.json().get("profiles", [])

#     if not profiles:
#         return []

#     # ================= FILTERS =================

#     indian_keywords = [
#         'india', 'mumbai', 'delhi', 'bangalore', 'pune',
#         'hyderabad', 'chennai', 'navi mumbai',
#         'ahmedabad', 'kolkata', 'gurgaon', 'noida' ,'thane', 'gujarat', 'kerala', 'coimbatore', 'jaipur', 'lucknow', 'kanpur', 'nagpur', 'vadodara'
#     ]

#     finance_keywords = [
#         'finance', 'financial', 'treasury',
#         'accounts', 'accounting',
#         'fp&a', 'financial planning and analysis'
#     ]

#     strict_titles = [
#         'cfo', 'chief financial officer',
#         'finance director', 'treasury director',
#         'head of finance', 'finance head',
#         'financial controller', 'group cfo', 'sgm', 'senior general manager', 'gm', 'general manager', 'dgm', 'deputy general manager', 'agm', 'assistant general manager'
#     ]

#     filtered = []

#     for p in profiles:
#         exp = p.get("experience", [{}])[0]

#         title = exp.get("title", "").lower()
#         location = exp.get("location", "").lower()
#         is_current = (exp.get("ended") is None or exp.get("current") is True)

#         # ✅ only current roles
#         if not is_current:
#             continue

#         # ❌ STRICT FINANCE ONLY
#         if not any(fin in title for fin in finance_keywords):
#             continue

#         # ❌ STRICT INDIA ONLY (no blank allowed now)
#         if location:
#             if not ('india' in location or any(city in location for city in indian_keywords)):
#                 continue

#         filtered.append(p)

#     if not filtered:
#         return []

#     # ================= SORT =================
#     def get_title(p):
#         return p.get("experience", [{}])[0].get("title", "")

#     sorted_profiles = sorted(
#         filtered,
#         key=lambda p: get_seniority_rank(get_title(p))
#     )

#     # ✅ RETURN ONLY WHAT EXISTS (MAX 10)
#     return sorted_profiles[:10]


# # ================= CALLBACK =================
# @app.route('/', methods=['POST', 'GET'])
# def callback():
#     print("\n" + "═"*80)
#     print(f"CALLBACK RECEIVED {time.strftime('%Y-%m-%d %H:%M:%S')}")

#     try:
#         data = request.get_json(force=True)
#         items = data if isinstance(data, list) else [data]

#         for item in items:
#             if item.get("status") != "success":
#                 continue

#             cand = item.get("candidate", {})
#             name = cand.get("fullName", "N/A")

#             exp = next(
#                 (e for e in cand.get("experience", [])
#                  if e.get("ended") is None or e.get("current")),
#                 {}
#             )

#             pos = exp.get("position", "N/A")
#             co = exp.get("company", "N/A")
#             loc = exp.get("location", "N/A")
#             start = exp.get("started", "N/A")

#             contacts = cand.get("contacts", [])

#             emails = [
#                 f"{c['value']} ({c.get('subType','')})"
#                 for c in contacts
#                 if c.get("type","").upper()=="EMAIL"
#                 and "personal" not in c.get("subType","").lower()
#             ]

#             phones = [
#                 f"{c['value']} ({c.get('subType','')})"
#                 for c in contacts
#                 if c.get("type","").upper()=="PHONE"
#             ]

#             results_cache[name] = {
#                 "pos":pos, "co":co, "loc":loc,
#                 "start":start, "emails":emails, "phones":phones
#             }

#             print(f"DETAILS READY → {name}")

#     except Exception as e:
#         print("Callback error:", str(e))

#     return {"status":"ok"}, 200


# # ================= MAIN =================
# def run_flask():
#     app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)


# if __name__ == "__main__":
#     threading.Thread(target=run_flask, daemon=True).start()
#     time.sleep(2)

#     print("\nSignalHire Enricher - STRICT INDIAN FINANCE ONLY")
#     company = input("Company name: ").strip()

#     profiles = search_finance_treasury(company)

#     if not profiles:
#         print("❌ No STRICT Indian finance profiles found.")
#     else:
#         print(f"\nStrict finance people for {company}:\n")

#         person_map = {}
#         uids = []

#         for i, p in enumerate(profiles, 1):
#             name = p.get("fullName", "N/A")
#             title = p.get("experience", [{}])[0].get("title", "N/A")
#             uid = p.get("uid")

#             print(f"{i}. {name} - {title}")

#             person_map[i] = {"name":name, "title":title}
#             if uid:
#                 uids.append(uid)

#         if uids:
#             print(f"\nRequesting contacts for {len(uids)} people...")
#             headers = {"apikey": API_KEY, "Content-Type": "application/json"}
#             payload = {"items": uids, "callbackUrl": CALLBACK_URL}
#             resp = requests.post(BASE_URL + PERSON_ENDPOINT, headers=headers, json=payload)
#             print(f"Status: {resp.status_code}")
#             print("Waiting for callbacks...\n")

#         while True:
#             inp = input("Number or 'exit': ").strip()

#             if inp.lower() == 'exit':
#                 break

#             if not inp.isdigit() or int(inp) not in person_map:
#                 print("Invalid, try again")
#                 continue

#             num = int(inp)
#             p = person_map[num]

#             print(f"\n{p['name']} - {p['title']}")

#             if p['name'] in results_cache:
#                 d = results_cache[p['name']]

#                 print("Current experience:")
#                 print(f" Position: {d['pos']}")
#                 print(f" Company : {d['co']}")
#                 print(f" Location: {d['loc']}")
#                 print(f" Started : {d['start']}")

#                 print("\nWork emails:")
#                 print(" " + "\n ".join(d['emails']) if d['emails'] else "None")

#                 print("\nPhones:")
#                 print(" " + "\n ".join(d['phones']) if d['phones'] else "None")

#                 print("─"*60)
#             else:
#                 print("Not received yet. Wait a bit and try again.")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



# import streamlit as st
# import requests
# from queue import Queue
# import json
# import time
# import threading
# from flask import Flask, request

# # ────────────────────────────────────────────────
# #   CONFIG & GLOBALS
# # ────────────────────────────────────────────────

# API_KEY = API_KEY
# BASE_URL = "https://www.signalhire.com/api/v1"
# SEARCH_ENDPOINT = "/candidate/searchByQuery"
# PERSON_ENDPOINT = "/candidate/search"


# app = Flask(__name__)
# results_cache = {}           # global — shared with flask callback
# status_queue = Queue()       # thread-safe way to send status from flask → streamlit


# # ================= SENIORITY =================
# def get_seniority_rank(title):
#     if not title:
#         return 999

#     t = title.lower()

#     if any(x in t for x in ['cfo', 'chief financial officer', 'group cfo']):
#         return 1
#     if any(x in t for x in ['svp', 'senior vice president']):
#         return 2
#     if any(x in t for x in ['vp', 'vice president', 'avp', 'assistant vice president', 'dvp', 'deputy vice president']):
#         return 3
#     if any(x in t for x in ['director', 'finance director', 'treasury director', 'head']):
#         return 4
#     if any(x in t for x in ['sgm', 'senior general manager', 'gm', 'general manager', 'dgm', 'deputy general manager', 'agm', 'assistant general manager', 'general manager']):
#         return 5
#     if 'senior manager' in t:
#         return 6
#     if any(x in t for x in ['manager']):
#         return 7

#     return 999

# # ================= STRICT ROLE FILTER =================
# allowed_roles = [
#     'cfo', 'chief financial officer',
#     'svp finance', 'senior vice president finance',
#     'vp finance', 'vice president finance',
#     'avp finance', 'assistant vice president finance',
#     'director finance', 'finance director',
#     'treasury director', 'head of finance', 'head finance',
#     'head of treasury', 'treasury head',
#     'fp&a head', 'head fp&a',
#     'general manager finance', 'gm finance',
#     'senior manager finance', 'finance manager',
#     'manager finance', 'manager accounts'
# ]

# def is_strict_finance_role(title):
#     t = title.lower()

#     for role in allowed_roles:
#         if role in t:
#             return True

#     return False


# # ================= MAIN SEARCH =================
# def search_finance_treasury(company_name, size=80):
#     headers = {"apikey": API_KEY, "Content-Type": "application/json"}

#     payload = {
#         "keywords": f"{company_name} AND (finance OR financial OR treasury OR accounting OR FP&A)",
#         "size": size,
#     }

#     try:
#         r = requests.post(BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload, timeout=20)
#         r.raise_for_status()
#         profiles = r.json().get("profiles", [])
#     except Exception as e:
#         st.error(f"Search failed: {str(e)}")
#         return []

#     if not profiles:
#         st.warning("No results with strict keywords → trying broader search...")
#         payload["keywords"] = f"{company_name} (finance OR accounts OR treasury OR audit OR tax)"
#         try:
#             r = requests.post(BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload, timeout=20)
#             profiles = r.json().get("profiles", [])
#         except Exception as e:
#             st.error(f"Fallback search failed: {str(e)}")
#             return []

#     if not profiles:
#         return []

#     # FILTERS
#     indian_keywords = [
#         'india', 'mumbai', 'delhi', 'bangalore', 'pune',
#         'hyderabad', 'chennai', 'navi mumbai',
#         'ahmedabad', 'kolkata', 'gurgaon', 'noida', 'thane', 'gujarat', 'kerala',
#         'coimbatore', 'jaipur', 'lucknow', 'kanpur', 'nagpur', 'vadodara'
#     ]

#     finance_keywords = [
#         'finance', 'financial', 'treasury',
#         'accounts', 'accounting',
#         'fp&a', 'financial planning and analysis'
#     ]

#     filtered = []

#     for p in profiles:
#         if not p.get("experience"):
#             continue
#         exp = p["experience"][0]
#         title = exp.get("title", "").lower()
#         location = exp.get("location", "").lower()
#         is_current = (exp.get("ended") is None or exp.get("current") is True)

#         if not is_current:
#             continue
#         if not any(fk in title for fk in finance_keywords):
#             continue
#         if location and not ('india' in location or any(k in location for k in indian_keywords)):
#             continue

#         filtered.append(p)

#     if not filtered:
#         return []

#     # SORT by seniority
#     def get_title(p):
#         return p.get("experience", [{}])[0].get("title", "")

#     sorted_profiles = sorted(
#         filtered,
#         key=lambda p: get_seniority_rank(get_title(p))
#     )

#     return sorted_profiles[:10]


# # ================= CALLBACK – FIXED (no st.session_state here!) =================
# @app.route('/', methods=['POST', 'GET'])
# def callback():
#     print("\n" + "═"*70)
#     print(f"CALLBACK RECEIVED {time.strftime('%Y-%m-%d %H:%M:%S')}")

#     try:
#         data = request.get_json(force=True)
#         items = data if isinstance(data, list) else [data]

#         for item in items:
#             if item.get("status") != "success":
#                 print(f"  → Skipping: status = {item.get('status')}")
#                 continue

#             cand = item.get("candidate", {})
#             name = cand.get("fullName", "N/A")

#             exp = next(
#                 (e for e in cand.get("experience", [])
#                  if e.get("ended") is None or e.get("current")),
#                 {}
#             )

#             pos = exp.get("position", "N/A")
#             co = exp.get("company", "N/A")
#             loc = exp.get("location", "N/A")
#             start = exp.get("started", "N/A")

#             contacts = cand.get("contacts", [])

#             emails = [
#                 f"{c['value']} ({c.get('subType','')})"
#                 for c in contacts
#                 if c.get("type", "").upper() == "EMAIL"
#                 and "personal" not in c.get("subType", "").lower()
#             ]

#             phones = [
#                 f"{c['value']} ({c.get('subType','')})"
#                 for c in contacts
#                 if c.get("type", "").upper() == "PHONE"
#             ]

#             results_cache[name] = {
#                 "pos": pos, "co": co, "loc": loc,
#                 "start": start, "emails": emails, "phones": phones
#             }

#             print(f"DETAILS READY → {name}")
#             status_queue.put(f"✅ Details ready for: {name}")

#     except Exception as e:
#         print("Callback error:", str(e))
#         status_queue.put(f"Callback error: {str(e)}")

#     return {"status": "ok"}, 200


# def run_flask():
#     app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)


# # ────────────────────────────────────────────────
# #   STREAMLIT MAIN
# # ────────────────────────────────────────────────

# def main():
#     st.set_page_config(page_title="SignalHire Indian Finance", layout="wide")

#     st.title("SignalHire – Strict Indian Finance Profiles")
#     st.caption("Enter company name → see list → enter number to view details (when ready)")

#     # Start Flask server once
#     if "flask_started" not in st.session_state:
#         threading.Thread(target=run_flask, daemon=True).start()
#         time.sleep(1.8)  # give flask time to start
#         st.session_state.flask_started = True

#     # Company input
#     company = st.text_input("Company name", placeholder="e.g. Reliance, TCS, HDFC", key="company_input")

#     if st.button("Search", type="primary", use_container_width=True):
#         if not company.strip():
#             st.error("Please enter a company name")
#             st.stop()

#         # Reset state
#         results_cache.clear()
#         st.session_state.profiles = None
#         st.session_state.person_map = {}
#         st.session_state.uids_requested = False

#         while not status_queue.empty():
#             status_queue.get()  # clear old messages

#         with st.spinner("Searching profiles..."):
#             profiles = search_finance_treasury(company.strip())

#         if not profiles:
#             st.error("❌ No matching strict Indian finance profiles found.")
#             st.stop()

#         st.success(f"Found {len(profiles)} matching profiles")

#         person_map = {}
#         uids = []

#         st.subheader(f"Results for **{company.strip()}**")

#         for i, p in enumerate(profiles, 1):
#             name = p.get("fullName", "N/A")
#             title = p.get("experience", [{}])[0].get("title", "N/A")
#             uid = p.get("uid")

#             st.markdown(f"**{i}.** {name} — {title}")

#             person_map[i] = {"name": name, "title": title}
#             if uid:
#                 uids.append(uid)

#         st.session_state.profiles = profiles
#         st.session_state.person_map = person_map

#         if uids and not st.session_state.get("uids_requested", False):
#             with st.spinner("Requesting contact details..."):
#                 headers = {"apikey": API_KEY, "Content-Type": "application/json"}
#                 payload = {"items": uids, "callbackUrl": CALLBACK_URL}
#                 try:
#                     resp = requests.post(BASE_URL + PERSON_ENDPOINT, headers=headers, json=payload, timeout=15)
#                     st.write(f"Request status: **{resp.status_code}**")
#                     if 200 <= resp.status_code < 300:
#                         st.info("Contacts requested – waiting for SignalHire callbacks (usually 10–90 seconds per person)")
#                         st.session_state.uids_requested = True
#                     else:
#                         st.error(f"Request failed with status {resp.status_code}")
#                 except Exception as e:
#                     st.error(f"Error sending request: {str(e)}")

#     # Show recent status messages from queue
#     if "person_map" in st.session_state and st.session_state.person_map:
#         st.markdown("**Status updates:**")
#         temp_msgs = []
#         while not status_queue.empty():
#             msg = status_queue.get()
#             temp_msgs.append(msg)

#         if temp_msgs:
#             for msg in temp_msgs:
#                 if "error" in msg.lower():
#                     st.error(msg)
#                 else:
#                     st.success(msg)
#         else:
#             st.caption("(no new updates yet)")

#     # Detail viewer
#     if "person_map" in st.session_state and st.session_state.person_map:
#         st.markdown("---")
#         inp = st.text_input(
#             "Enter number (1–10) to see details, or type 'new' to search again",
#             key="detail_input"
#         ).strip()

#         if inp:
#             if inp.lower() in ['new', 'n', 'exit']:
#                 # Reset for new search
#                 keys_to_clear = ["profiles", "person_map", "uids_requested"]
#                 for k in keys_to_clear:
#                     if k in st.session_state:
#                         del st.session_state[k]
#                 st.rerun()

#             if inp.isdigit():
#                 num = int(inp)
#                 if num in st.session_state.person_map:
#                     p = st.session_state.person_map[num]
#                     name = p["name"]
#                     st.subheader(f"{num}. {name} — {p['title']}")

#                     if name in results_cache:
#                         d = results_cache[name]
#                         st.markdown(f"**Position:** {d['pos']}")
#                         st.markdown(f"**Company:** {d['co']}")
#                         st.markdown(f"**Location:** {d['loc']}")
#                         st.markdown(f"**Started:** {d['start']}")

#                         st.markdown("**Work emails:**")
#                         if d['emails']:
#                             for e in d['emails']:
#                                 st.write(f"• {e}")
#                         else:
#                             st.write("None")

#                         st.markdown("**Phones:**")
#                         if d['phones']:
#                             for ph in d['phones']:
#                                 st.write(f"• {ph}")
#                         else:
#                             st.write("None")
#                     else:
#                         st.info("⏳ Details not received yet. SignalHire callback is still pending. Click 'Refresh' below after a minute.")
#                 else:
#                     st.warning("Invalid number – please enter 1 to 10")

#     # Manual refresh button (recommended instead of auto-rerun loop)
#     if "person_map" in st.session_state:
#         if st.button("Refresh / Check for new details"):
#             st.rerun()


# if __name__ == "__main__":
#     main()
import json
import os
import time

import requests
import streamlit as st

# ────────────────────────────────────────────────
#   CONFIG
# ────────────────────────────────────────────────

# API_KEY         = "YOUR_API_KEY_HERE"
BASE_URL        = "https://www.signalhire.com/api/v1"
SEARCH_ENDPOINT = "/candidate/searchByQuery"
PERSON_ENDPOINT = "/candidate/search"

# CALLBACK_URL  = "https://your-public-domain.com/signal_hire"   # ← your live webhook
RESULTS_FILE  = "/tmp/signalhire_results.json"                  # shared with webhook_server.py




API_KEY = "202.M3D7xK6FykhOIHuKoFGLLjMI8jwW"
BASE_URL = "https://www.signalhire.com/api/v1"
SEARCH_ENDPOINT = "/candidate/searchByQuery"
PERSON_ENDPOINT = "/candidate/search"

# CALLBACK_URL = "https://uninwrapped-celinda-subcranially.ngrok-free.dev"  # ← must be public & active!
CALLBACK_URL = "https://192.168.1.108:5000/signal_hire"  # ← must be public & active!




# ────────────────────────────────────────────────
#   SHARED-FILE HELPERS
# ────────────────────────────────────────────────
RESULTS_API_URL = "https://192.168.1.108:5000/get_results"  # ← your webserver

def load_results() -> dict:
    try:
        resp = requests.get(RESULTS_API_URL, timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return {}

def clear_results() -> None:
    try:
        requests.post("https://192.168.1.108:5000/clear_results", timeout=5)
    except Exception:
        pass

# ────────────────────────────────────────────────
#   SENIORITY RANKING
# ────────────────────────────────────────────────

def get_seniority_rank(title: str) -> int:
    if not title:
        return 999
    t = title.lower()
    if any(x in t for x in ["cfo", "chief financial officer", "group cfo"]):
        return 1
    if any(x in t for x in ["svp", "senior vice president"]):
        return 2
    if any(x in t for x in ["vp", "vice president", "avp", "assistant vice president",
                              "dvp", "deputy vice president"]):
        return 3
    if any(x in t for x in ["director", "finance director", "treasury director", "head"]):
        return 4
    if any(x in t for x in ["sgm", "senior general manager", "gm", "general manager",
                              "dgm", "deputy general manager", "agm",
                              "assistant general manager"]):
        return 5
    if "senior manager" in t:
        return 6
    if "manager" in t:
        return 7
    return 999


# ────────────────────────────────────────────────
#   STRICT ROLE FILTER
# ────────────────────────────────────────────────

ALLOWED_ROLES = [
    "cfo", "chief financial officer",
    "svp finance", "senior vice president finance",
    "vp finance", "vice president finance",
    "avp finance", "assistant vice president finance",
    "director finance", "finance director",
    "treasury director", "head of finance", "head finance",
    "head of treasury", "treasury head",
    "fp&a head", "head fp&a",
    "general manager finance", "gm finance",
    "senior manager finance", "finance manager",
    "manager finance", "manager accounts",
]


def is_strict_finance_role(title: str) -> bool:
    t = title.lower()
    return any(role in t for role in ALLOWED_ROLES)


# ────────────────────────────────────────────────
#   MAIN SEARCH
# ────────────────────────────────────────────────

INDIAN_KEYWORDS = [
    "india", "mumbai", "delhi", "bangalore", "pune",
    "hyderabad", "chennai", "navi mumbai",
    "ahmedabad", "kolkata", "gurgaon", "noida", "thane", "gujarat", "kerala",
    "coimbatore", "jaipur", "lucknow", "kanpur", "nagpur", "vadodara",
]

FINANCE_KEYWORDS = [
    "finance", "financial", "treasury",
    "accounts", "accounting",
    "fp&a", "financial planning and analysis",
]


def search_finance_treasury(company_name: str, size: int = 80) -> list:
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}

    payload = {
        "keywords": (
            f"{company_name} AND "
            "(finance OR financial OR treasury OR accounting OR FP&A)"
        ),
        "size": size,
    }

    try:
        r = requests.post(
            BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload, timeout=20
        )
        r.raise_for_status()
        profiles = r.json().get("profiles", [])
    except Exception as exc:
        st.error(f"Search failed: {exc}")
        return []

    if not profiles:
        st.warning("No results with strict keywords → trying broader search…")
        payload["keywords"] = (
            f"{company_name} (finance OR accounts OR treasury OR audit OR tax)"
        )
        try:
            r = requests.post(
                BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload, timeout=20
            )
            profiles = r.json().get("profiles", [])
        except Exception as exc:
            st.error(f"Fallback search failed: {exc}")
            return []

    if not profiles:
        return []

    # ── Filters ──────────────────────────────────
    filtered = []
    for p in profiles:
        if not p.get("experience"):
            continue
        exp      = p["experience"][0]
        title    = exp.get("title", "").lower()
        location = exp.get("location", "").lower()
        is_current = exp.get("ended") is None or exp.get("current") is True

        if not is_current:
            continue
        if not any(fk in title for fk in FINANCE_KEYWORDS):
            continue
        if location and not (
            "india" in location or any(k in location for k in INDIAN_KEYWORDS)
        ):
            continue
        filtered.append(p)

    if not filtered:
        return []

    # ── Sort by seniority ─────────────────────────
    def _get_title(p):
        return p.get("experience", [{}])[0].get("title", "")

    sorted_profiles = sorted(filtered, key=lambda p: get_seniority_rank(_get_title(p)))
    return sorted_profiles[:5]


# ────────────────────────────────────────────────
#   STREAMLIT UI
# ────────────────────────────────────────────────

def main():
    st.set_page_config(page_title="SignalHire Indian Finance", layout="wide")
    st.title("SignalHire – Strict Indian Finance Profiles")
    st.caption(
        "Enter a company name → see the ranked list → "
        "click **Refresh** after ~30–90 s to load contact details."
    )

    # ── Company input ─────────────────────────────
    company = st.text_input(
        "Company name",
        placeholder="e.g. Reliance, TCS, HDFC",
        key="company_input",
    )

    if st.button("Search", type="primary", use_container_width=True):
        if not company.strip():
            st.error("Please enter a company name.")
            st.stop()

        # Reset state and wipe old results
        clear_results()
        st.session_state.profiles   = None
        st.session_state.person_map = {}
        st.session_state.uids_requested = False

        with st.spinner("Searching profiles…"):
            profiles = search_finance_treasury(company.strip())

        if not profiles:
            st.error("❌ No matching strict Indian finance profiles found.")
            st.stop()

        st.success(f"Found {len(profiles)} matching profiles")

        person_map = {}
        uids       = []

        st.subheader(f"Results for **{company.strip()}**")
        display_lines = []
        for i, p in enumerate(profiles, 1):
            name  = p.get("fullName", "N/A")
            title = p.get("experience", [{}])[0].get("title", "N/A")
            uid   = p.get("uid")

            line = f"**{i}.** {name} — {title}"
            st.markdown(line)
            display_lines.append(line)
            person_map[i] = {"name": name, "title": title}
            if uid:
                uids.append(uid)

        st.session_state.display_lines = display_lines
        st.session_state.search_company = company.strip()

        st.session_state.profiles   = profiles
        st.session_state.person_map = person_map

        # ── Request contact details from SignalHire ──
        if uids and not st.session_state.get("uids_requested", False):
            with st.spinner("Requesting contact details from SignalHire…"):
                headers = {"apikey": API_KEY, "Content-Type": "application/json"}
                payload = {"items": uids, "callbackUrl": CALLBACK_URL}
                try:
                    resp = requests.post(
                        BASE_URL + PERSON_ENDPOINT,
                        headers=headers,
                        json=payload,
                        timeout=15,
                    )
                    st.write(f"Request status: **{resp.status_code}**")
                    if 200 <= resp.status_code < 300:
                        st.info(
                            "Contact details requested. "
                            "SignalHire will call back in ~10–90 s per person. "
                            "Click **Refresh** below to check."
                        )
                        st.session_state.uids_requested = True
                    else:
                        st.error(f"Request failed: HTTP {resp.status_code}")
                except Exception as exc:
                    st.error(f"Error sending request: {exc}")

    # ── Detail viewer ─────────────────────────────
    if st.session_state.get("person_map"):
        st.markdown("---")
        inp = st.text_input(
            "Enter number (1–5) to view details, or type 'new' to search again",
            key="detail_input",
        ).strip()

        if inp:
            if inp.lower() in ("new", "n", "exit"):
                for k in ("profiles", "person_map", "uids_requested"):
                    st.session_state.pop(k, None)
                st.rerun()

            if inp.isdigit():
                num = int(inp)
                pm  = st.session_state.person_map
                if num in pm:
                    p    = pm[num]
                    name = p["name"]
                    st.subheader(f"{num}. {name} — {p['title']}")

                    # Read from shared file (written by webhook server)
                    results = load_results()

                    if name in results:
                        d = results[name]
                        st.markdown(f"**Position:** {d['pos']}")
                        st.markdown(f"**Company:**  {d['co']}")
                        st.markdown(f"**Location:** {d['loc']}")
                        st.markdown(f"**Started:**  {d['start']}")

                        st.markdown("**Work emails:**")
                        if d["emails"]:
                            for e in d["emails"]:
                                st.write(f"• {e}")
                        else:
                            st.write("None found")

                        st.markdown("**Phones:**")
                        if d["phones"]:
                            for ph in d["phones"]:
                                st.write(f"• {ph}")
                        else:
                            st.write("None found")
                    else:
                        st.info(
                            "⏳ Details not received yet — "
                            "SignalHire callback is still pending. "
                            "Click **Refresh** in a moment."
                        )
                else:
                    st.warning("Invalid number – please enter 1 to 5.")

    # ── How many results have arrived so far ─────
    if st.session_state.get("person_map"):
        results = load_results()
        arrived = len(results)
        total   = len(st.session_state.person_map)
        if arrived:
            st.caption(f"Details received so far: {arrived} / {total}")

    # ── Manual refresh ────────────────────────────
    if st.session_state.get("person_map"):
        if st.button("🔄 Refresh / check for new details"):
            st.rerun()


if __name__ == "__main__":
    main()
