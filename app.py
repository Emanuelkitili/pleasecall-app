from flask import Flask, request, jsonify, render_template
import africastalking
import requests
import base64
from datetime import datetime as dt
import os

app = Flask(__name__)

# --- CONFIG YA MBOKA - 2 BOB ---
YOUR_MPESA_NUMBER = "0701295634"
MY_MBOKA_PHONE = "254701295634"
PRICE_TOTAL = 2
YOUR_CUT = 1
BASE_URL = "https://6c926d363ae88f.lhr.life"

MPESA_SHORTCODE = "174379"
MPESA_CONSUMER_KEY = "PASTE_YOUR_CONSUMER_KEY_HERE"
MPESA_CONSUMER_SECRET = "PASTE_YOUR_CONSUMER_SECRET_HERE"
MPESA_PASSKEY = "PASTE_YOUR_PASSKEY_HERE"
AT_USERNAME = "sandbox"
AT_API_KEY = "PASTE_YOUR_AT_API_KEY"

africastalking.initialize(AT_USERNAME, AT_API_KEY)
voice = africastalking.Voice

payments_db = {}

@app.route('/')
def home():
    return render_template('index.html') if os.path.exists('templates/index.html') else f"PleaseCall App Iko Live! 2 bob = 1 kwako ({YOUR_MPESA_NUMBER}) + 1 call - {BASE_URL}"

@app.route('/call', methods=['POST'])
def make_call():
    data = request.get_json()
    mum_number = data.get('mum_number')
    message = data.get('message', 'Mum ni mimi')
    
    if not mum_number.startswith("+"):
        mum_number = "+254" + mum_number[-9:]

    try:
        response = voice.call(
            callFrom="+254711082000",
            callTo=[mum_number]
        )
        return jsonify({
            "status": "success",
            "message": f"Call inaenda kwa {mum_number}. Profit yako {YOUR_CUT} bob!",
            "your_profit": YOUR_CUT
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

# USSD + MPESA LOGIC
def get_mpesa_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(url, auth=(MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET))
    return r.json().get('access_token')

@app.route('/ussd', methods=['POST'])
def ussd():
    phone = request.values.get("phoneNumber")
    text = request.values.get("text", "")
    if text == "":
        return "CON PleaseCall 2BOB - Mboka 0701295634\nWeka namba ya mum:\n"
    
    receiver = "254" + text[-9:]
    sender_clean = phone.replace("+", "")
    # hapa ndio unge-tuma STK ya 2 bob
    payments_db[sender_clean] = {"to": "+" + receiver}
    return "END Sawa! Lipa 2 bob kwa Till. Tutakupigia."

@app.route('/mpesa/callback', methods=['POST'])
def mpesa_callback():
    return "OK"

@app.route('/voice/callback', methods=['POST'])
def voice_callback():
    is_active = request.values.get('isActive')
    if is_active == '1':
        xml = f'<Response><Say>Ujumbe kutoka kwa mwanao.</Say><Record maxLength="240" finishOnKey="#" callbackUrl="{BASE_URL}/voice/recording"/></Response>'
        return app.response_class(xml, mimetype='text/xml')
    return app.response_class('<Response><Say>Subiri</Say></Response>', mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
