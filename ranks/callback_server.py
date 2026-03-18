from flask import Flask, request
import time

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_callback():

    print("\n" + "="*80)
    print("CALLBACK RECEIVED:", time.strftime('%Y-%m-%d %H:%M:%S'))

    data = request.get_json(force=True)

    if isinstance(data, list):
        data = data[0]

    candidate = data.get("candidate", {})

    full_name = candidate.get("fullName", "N/A")

    # Latest experience (ended = null)
    latest = None
    for exp in candidate.get("experience", []):
        if exp.get("ended") is None:
            latest = exp
            break

    emails = []
    phones = []

    for c in candidate.get("contacts", []):
        t = c.get("type")
        subtype = c.get("subType", "")
        val = c.get("value")

        if t == "EMAIL" and "personal" not in subtype:
            emails.append(val)

        if t == "PHONE":
            phones.append(val)

    print("\nFULL NAME")
    print(full_name)

    print("\nLATEST EXPERIENCE (ended = null)")

    if latest:
        print("Title   :", latest.get("position"))
        print("Company :", latest.get("company"))
        print("Started :", latest.get("started"))

    print("\nCONTACTS")

    for e in emails:
        print("Work Email:", e)

    for p in phones:
        print("Phone:", p)

    print("="*80)

    return {"status":"received"},200


if __name__ == "__main__":
    print("Callback server running at http://127.0.0.1:5000")
    app.run(port=5000)