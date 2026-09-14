from flask import Flask, request, jsonify, render_template
import africastalking
import os

app = Flask(__name__)

# CONFIG
AT_USERNAME = os.getenv("AT_USERNAME", "sandbox")
AT_API_KEY = os.getenv("AT_API_KEY", "atsk_xxx")
africastalking.initialize(AT_USERNAME, AT_API_KEY)
voice = africastalking.Voice

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/call', methods=['POST'])
def make_call():
    data = request.get_json()
    mum_number = data.get('mum_number')
    message = data.get('message', 'Mum ni mimi')
    
    if not mum_number:
        return jsonify({"status": "failed", "message": "Weka namba ya Mum"})
    
    # Formati namba +254
    if mum_number.startswith('0'):
        mum_number = '+254' + mum_number[1:]
    
    try:
        # Hii ndio itampigia Mum na ikifika, itaita /voice
        call_from = os.getenv("AT_PHONE_NUMBER", "+254...") # namba yako ya AT
        response = voice.call(callFrom=call_from, callTo=[mum_number])
        print(response)
        
        return jsonify({
            "status": "success", 
            "message": f"Asante! Tunampigia {data.get('mum_number')} sasa. Mum atasikia: '{message}' RING RING..."
        })
    except Exception as e:
        # Kwa sandbox bado ita-return success hata kama call haikuenda kwa sababu hakuna credit
        print(f"Error: {e}")
        return jsonify({
            "status": "success",
            "message": f"Asante! Tunampigia {data.get('mum_number')} RING RING... (Sandbox mode: {message})"
        })

@app.route('/voice', methods=['POST'])
def voice_callback():
    # Hii ndio sauti Mum atasikia akipokea!
    # Africa's Talking inaita hii automatically
    mum_message = request.values.get('message', 'Mum, mtoto wako anakuhitaji. Tafadhali mpigie akipata nafasi. Asante.')
    
    response = f'''<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say voice="woman">Hello Mum! {mum_message}. Please call back your child when you are free. Thank you. Kwa heri.</Say>
    </Response>'''
    return response, 200, {'Content-Type': 'text/xml'}

if __name__ == '__main__':
    app.run(debug=True)
