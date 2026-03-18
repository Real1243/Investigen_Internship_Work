import requests
import json

# === PRIVATE KEY ===
API_KEY = "202.M3D7xK6FykhOIHuKoFGLLjMI8jwW"  # NEVER share!

BASE_URL = "https://www.signalhire.com/api/v1"
SEARCH_ENDPOINT = "/candidate/searchByQuery"

# Seniority rank: lower = more senior (parse from title)
def get_seniority_rank(title):
    if not title:
        return 999
    title_lower = title.lower()
    if any(w in title_lower for w in ['chief', 'cfo', 'chief financial', 'chief treasury']):
        return 1
    if any(w in title_lower for w in ['vp', 'vice president', 'svp', 'evp']):
        return 2
    if any(w in title_lower for w in ['director', 'head of', 'group head']):
        return 3
    if any(w in title_lower for w in ['senior manager', 'lead', 'principal']):
        return 4
    if any(w in title_lower for w in ['manager']):
        return 5
    return 6

# Search function
def search_finance_treasury(company_name, size=10):
    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Payload: Use Boolean for titles/companies, keywords for finance/treasury
    payload = {
        "keywords": "finance OR treasury",  # or add more like "banking OR financial"
        "currentTitle": "(CFO OR \"Vice President Finance\" OR \"Finance Director\" OR \"Treasury Director\" OR \"Group Treasurer\" OR Manager OR Director) NOT intern NOT junior",
        "currentCompany": f"\"{company_name}\" OR {company_name.replace(' ', '')}",  # exact + variation
        "size": size,
        # Optional: "location": "India", "industry": "Banking" (check allowed values)
    }
    
    print("Payload:")
    print(json.dumps(payload, indent=2))
    print("Requesting SearchByQuery...")
    
    try:
        response = requests.post(BASE_URL + SEARCH_ENDPOINT, headers=headers, json=payload)
        
        print(f"Status: {response.status_code}")
        print(f"Credits Left: {response.headers.get('X-Credits-Left', 'Unknown')}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response keys:", list(data.keys()))
            
            profiles = data.get("profiles", [])
            if not profiles:
                print("No profiles. Full response:", json.dumps(data, indent=2))
                return []
            
            # Extract current title (usually first in experience)
            def get_current_title(profile):
                exp = profile.get("experience", [])
                if exp:
                    return exp[0].get("title", "")
                return ""
            
            # Sort: most senior first
            sorted_profiles = sorted(profiles, key=lambda p: get_seniority_rank(get_current_title(p)))
            
            return sorted_profiles, data.get("scrollId"), data.get("requestId"), data.get("total")
        else:
            print("Error:", response.text)
            return [], None, None, None
    
    except Exception as e:
        print("Exception:", str(e))
        return [], None, None, None

# Run example
target_company = "HDFC Bank"
profiles, scroll_id, req_id, total = search_finance_treasury(target_company, size=10)

print(f"\n=== Found {len(profiles)} / {total or 'Unknown'} Finance/Treasury People (Sorted Most Senior First) ===\n")

for idx, p in enumerate(profiles, 1):
    name = p.get("fullName", "N/A")
    loc = p.get("location", "N/A")
    skills = ", ".join(p.get("skills", []))[:100] + "..." if p.get("skills") else "N/A"
    open_to_work = p.get("openToWork", "N/A")
    
    # Current title/company from experience[0]
    current_exp = p.get("experience", [{}])[0]
    title = current_exp.get("title", "N/A")
    company = current_exp.get("company", "N/A")
    rank = get_seniority_rank(title)
    
    print(f"{idx}. Rank {rank} | {name}")
    print(f"   Title: {title} @ {company}")
    print(f"   Location: {loc}")
    print(f"   Open to Work: {open_to_work}")
    print(f"   Skills: {skills}")
    print("-" * 70)

# If scroll_id: To fetch next batch 
if scroll_id:
    print(f"\nMore results available (total {total}). Use scrollId '{scroll_id}' with requestId {req_id} for next page.")