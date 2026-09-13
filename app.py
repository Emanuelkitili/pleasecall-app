from flask import Flask, request, jsonify
import africastalking
import os

app = Flask(__name__)

# --- CONFIG YAKO YA 2 BOB ---
YOUR_MPESA_NUMBER = "0701295634"
PRICE_TOTAL = 2  # Comrade analipa 2
YOUR_CUT = 1     # 1 kwako
CALL_COST = 1    # 1 kwa call

# Africa's Talking - weka keys zako hapa
AT_USERNAME = "sandbox" # badilisha ukiwa live
AT_API_KEY = "your_api_key_hapa"
africastalking.initialize(AT_USERNAME, AT_API_KEY)
voice = africastalking.Voice

@app.route('/')
def home():
    return "PleaseCall App Iko Live! 2 bob = 1 kwako + 1 call"

@app.route('/call', methods=['POST'])
def make_call():
    data = request.get_json()
    mum_number = data.get('mum_number') # namba ya kabambe
    message = data.get('message', 'Mum ni mimi, tafadhali nipigie')
    amount_paid = data.get('amount', 2) # tumeshapokea 2 bob?

    # LOGIC YA 2 BOB
    if amount_paid >= PRICE_TOTAL:
        print(f"Pesa imeingia! {YOUR_CUT} bob kwenda kwa {YOUR_MPESA_NUMBER}")
        
        # Piga call sasa
        try:
            # Hii ndio itapigia mum
            response = voice.call(
                callFrom="+254...AT_NUMBER_YAKO",
                callTo=[mum_number]
            )
            return jsonify({
                "status": "success",
                "message": f"Asante comrade! Call inaenda kwa {mum_number}. 1 bob kwako imebaki!",
                "your_profit": YOUR_CUT
            })
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)})
    else:
        return jsonify({"status": "failed", "message": "Tuma 2 bob kwanza"})

if __name__ == '__main__':
    app.run(debug=True)
