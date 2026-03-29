# from flask import Flask, request
# import json
# import time

# app = Flask(__name__)

# @app.route('/', methods=['POST'])
# def handle_callback():
#     print("\n" + "═" * 80)
#     print(f"CALLBACK RECEIVED AT {time.strftime('%Y-%m-%d %H:%M:%S')}")
#     print(f"From IP: {request.remote_addr}")
    
#     try:
#         data = request.get_json(force=True)
#         if not data:
#             print("No data received!")
#             print("Raw body:", request.data)
#             return {"status": "no data"}, 200
        
#         # SignalHire wraps in list → take first item
#         if isinstance(data, list) and len(data) > 0:
#             data = data[0]
        
#         if not isinstance(data, dict):
#             print("Unexpected format:", type(data))
#             return {"status": "invalid"}, 200
        
#         candidate = data.get("candidate", {})
#         full_name = candidate.get("fullName", "Not found")
        
#         # Latest/current experience
#         current_exp = {}
#         for exp in candidate.get("experience", []):
#             if exp.get("ended") is None or exp.get("current") is True:
#                 current_exp = exp
#                 break
        
#         position = current_exp.get("position", "Not found")
#         company = current_exp.get("company", "Not found")
#         location = current_exp.get("location", "Not found")
#         started = current_exp.get("started", "Not found")
        
#         # Contacts — filter out personal emails
#         contacts_list = candidate.get("contacts", [])
#         emails = []
#         phones = []
#         for c in contacts_list:
#             val = c.get("value", "N/A")
#             typ = c.get("type", "").upper()
#             subtype = c.get("subType", "").lower()
            
#             if typ == "PHONE":
#                 phones.append(f"{val} ({subtype})")
#             elif typ == "EMAIL" and "personal" not in subtype:
#                 emails.append(f"{val} ({subtype})")  # only non-personal emails
        
#         # Clean print - only what Akshat wants
#         print("FULL NAME:")
#         print(f"  {full_name}")
#         print("\nCURRENT EXPERIENCE (latest / ended is null):")
#         print(f"  Position : {position}")
#         print(f"  Company  : {company}")
#         print(f"  Location : {location}")
#         print(f"  Started  : {started}")
#         print("\nCONTACTS (work emails + phones only):")
#         if emails:
#             for e in emails:
#                 print(f"  Email : {e}")
#         else:
#             print("  No work emails found")
#         if phones:
#             for ph in phones:
#                 print(f"  Phone : {ph}")
#         else:
#             print("  No phones found")
        
#         print("═" * 80 + "\n")
        
#         return {"status": "received"}, 200
    
#     except Exception as e:
#         print("ERROR:", str(e))
#         print("Raw body:", request.data)
#         return {"status": "error"}, 500

# if __name__ == '__main__':
#     print("Starting callback server on http://127.0.0.1:5000 ...")
#     app.run(host='0.0.0.0', port=5000, debug=True)



from flask import Flask, request
import json
import time

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_callback():
    print("\n" + "═" * 80)
    print(f"CALLBACK RECEIVED AT {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"From IP: {request.remote_addr}")
    
    try:
        data = request.get_json(force=True)
        if not data:
            print("No data received!")
            print("Raw body:", request.data)
            return {"status": "no data"}, 200
        
        # SignalHire wraps in list → take first item
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
        
        if not isinstance(data, dict):
            print("Unexpected format:", type(data))
            return {"status": "invalid"}, 200
        
        candidate = data.get("candidate", {})
        full_name = candidate.get("fullName", "Not found")
        
        # Latest/current experience (ended is null or current=true)
        current_exp = {}
        for exp in candidate.get("experience", []):
            if exp.get("ended") is None or exp.get("current") is True:
                current_exp = exp
                break
        
        position = current_exp.get("position", "Not found")
        company = current_exp.get("company", "Not found")
        location = current_exp.get("location", "Not found")
        started = current_exp.get("started", "Not found")
        
        # Contacts — only work emails + phones
        contacts_list = candidate.get("contacts", [])
        emails = []
        phones = []
        for c in contacts_list:
            val = c.get("value", "N/A")
            typ = c.get("type", "").upper()
            subtype = c.get("subType", "").lower()
            
            if typ == "PHONE":
                phones.append(f"{val} ({subtype})")
            elif typ == "EMAIL" and "personal" not in subtype:
                emails.append(f"{val} ({subtype})")
        
        # Clean, non-repeated output
        print("FULL NAME:")
        print(f"  {full_name}")
        
        print("\nCURRENT EXPERIENCE (latest / ended is null):")
        print(f"  Position : {position}")
        print(f"  Company  : {company}")
        print(f"  Location : {location}")
        print(f"  Started  : {started}")
        
        print("\nCONTACTS (work emails + phones only):")
        if emails:
            for e in emails:
                print(f"  Email : {e}")
        else:
            print("  No work emails found")
        
        if phones:
            for ph in phones:
                print(f"  Phone : {ph}")
        else:
            print("  No phones found")
        
        print("═" * 80 + "\n")
        
        return {"status": "received"}, 200
    
    except Exception as e:
        print("ERROR:", str(e))
        print("Raw body:", request.data)
        return {"status": "error"}, 500

if __name__ == '__main__':
    print("Starting callback server on http://127.0.0.1:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)