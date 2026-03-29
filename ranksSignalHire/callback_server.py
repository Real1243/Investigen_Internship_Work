import os
import threading

from flask import Flask, logging, request
import json
import time

app = Flask(__name__)


RESULTS_FILE = "/tmp/signalhire_results.json"   # shared with Streamlit app

_file_lock = threading.Lock()


# ────────────────────────────────────────────────
#   HELPERS
# ────────────────────────────────────────────────
 
def _write_result(name: str, record: dict) -> None:
    """Append / update one candidate in the shared JSON results file."""
    with _file_lock:
        try:
            with open(RESULTS_FILE, "r") as fh:
                data = json.load(fh)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
 
        data[name] = record
 
        with open(RESULTS_FILE, "w") as fh:
            json.dump(data, fh, indent=2)
 
 
def _parse_candidate(item: dict) -> None:
    """Extract fields from one callback item and persist them."""
    if item.get("status") != "success":
        logging.info(f"  → Skipping: status = {item.get('status')}")
        return
 
    cand = item.get("candidate", {})
    full_name = cand.get("fullName", "Not found")
 
    # Latest / current experience (ended is null or current=True)
    current_exp = {}
    for exp in cand.get("experience", []):
        if exp.get("ended") is None or exp.get("current") is True:
            current_exp = exp
            break
 
    position = current_exp.get("position", "Not found")
    company  = current_exp.get("company",  "Not found")
    location = current_exp.get("location", "Not found")
    started  = current_exp.get("started",  "Not found")
 
    # Contacts — work emails + all phones
    emails = []
    phones = []
    for c in cand.get("contacts", []):
        val     = c.get("value", "N/A")
        typ     = c.get("type", "").upper()
        subtype = (c.get("subType") or "").lower()

        if typ == "PHONE":
            phones.append(f"{val} ({subtype})" if subtype else val)
        elif typ == "EMAIL" and "personal" not in subtype:
            emails.append(f"{val} ({subtype})" if subtype else val)
 
    # Log
    logging.info(f"FULL NAME  : {full_name}")
    logging.info(f"Position   : {position}")
    logging.info(f"Company    : {company}")
    logging.info(f"Location   : {location}")
    logging.info(f"Started    : {started}")
    if emails:
        for e in emails:
            logging.info(f"  Email : {e}")
    else:
        logging.info("  No work emails found")
    if phones:
        for ph in phones:
            logging.info(f"  Phone : {ph}")
    else:
        logging.info("  No phones found")
 
    # Persist so Streamlit can read it
    _write_result(full_name, {
        "pos":    position,
        "co":     company,
        "loc":    location,
        "start":  started,
        "emails": emails,
        "phones": phones,
    })
    logging.info(f"  ✅ Saved to {RESULTS_FILE}")
 
 
# ────────────────────────────────────────────────
#   ROUTE
# ────────────────────────────────────────────────
 
@app.route("/signal_hire", methods=["POST", "GET"])
def signal_hire():
    logging.info("\n" + "═" * 80)
    logging.info(f"CALLBACK RECEIVED  {time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"From IP : {request.remote_addr}")
 
    try:
        data = request.get_json(force=True)
 
        if not data:
            logging.info("No JSON body received.")
            logging.info(f"Raw body: {request.data}")
            return {"status": "no data"}, 200
 
        # SignalHire sends a list — process every item
        items = data if isinstance(data, list) else [data]
        logging.info(f"Items in payload: {len(items)}")
 
        for item in items:
            _parse_candidate(item)
 
    except Exception as exc:
        logging.error(f"ERROR: {exc}")
        logging.error(f"Raw body: {request.data}")
        return {"status": "error"}, 500
 
    logging.info("═" * 80 + "\n")
    return {"status": "received"}, 200


@app.route("/get_results", methods=["GET"])
def get_results():
    try:
        with open(RESULTS_FILE, "r") as fh:
            data = json.load(fh)
        return data, 200
    except (FileNotFoundError, json.JSONDecodeError):
        return {}, 200

@app.route("/clear_results", methods=["POST"])
def clear_results_endpoint():
    try:
        os.remove(RESULTS_FILE)
    except FileNotFoundError:
        pass
    return {"status": "cleared"}, 200

if __name__ == '__main__':
    print("Starting callback server on http://127.0.0.1:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)