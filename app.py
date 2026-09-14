from flask import Flask, request, jsonify, render_template
import africastalking
import os

app = Flask(__name__)

# --- CONFIG SIRI - HAKUNA NAMBA HAPA PUBLIC ---
YOUR_MPESA = os.getenv("MPESA_NUMBER", "0701XXXXXX") # namba iko kwa Render Environment pekee
PRICE_TOTAL = 2
YOUR_CUT = 1
CALL_COST = 1

# Africa's Talking - weka keys zako kwa Render Environment pia
AT_USERNAME = os.getenv("AT_USERNAME", "sandbox")
AT_API_KEY = os.getenv("AT_API_KEY", "your_api_key")
africastalking.initialize(AT_USERNAME, AT_API_KEY)
voice = africastalking.Voice

@app.route('/')
def home():
    # Sasa inaonyesha page mzuri, si namba yako
    try:
        return render_template('index.html')
    except:
        return "PleaseCall App Iko Live! 2 bob = 1 kwako + 1 call"

@app.route('/call', methods=['POST'])
def make_call():
    data = request.get_json()
    mum_number = data.get('mum_number')
    message = data.get('message', 'Mum ni mimi, tafadhali nipigie')
    amount_paid = data.get('amount', 2)

    if not mum_number:
        return jsonify({"status": "failed", "message": "Weka namba ya Mum"})

    # LOGIC YA 2 BOB
    if amount_paid >= PRICE_TOTAL:
        print(f"Comrade amelipa {PRICE_TOTAL} bob! {YOUR_CUT} kwenda kwa {YOUR_MPESA}")
        try:
            # Hapa ndio call ya 1 bob inapigwa
            # Badilisha callFrom na namba yako ya Africa's Talking ukiwa live
            call_from = os.getenv("AT_PHONE_NUMBER", "+254...")

            # Kwa sandbox test, haitapiga kweli lakini ita-log
            print(f"Tunampigia {mum_number} ujumbe: {message}")
            
            # Uncomment ukiwa na credit ya AT
            # response = voice.call(callFrom=call_from, callTo=[mum_number])

            return jsonify({
                "status": "success",
                "message": f"Asante comrade! Tunampigia {mum_number} sasa RING RING... 1 bob imebaki kwako!",
                "your_profit": YOUR_CUT
            })
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)})
    else:
        return jsonify({"status": "failed", "message": "Tuma 2 bob kwanza"})

if __name__ == '__main__':
    app.run(debug=True)
