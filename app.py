from flask import Flask, request, render_template_string
import africastalking
import os

app = Flask(__name__)

# Africa's Talking setup
username = os.environ.get("AT_USERNAME", "sandbox")
api_key = os.environ.get("AT_API_KEY", "atsk_xxx")
africastalking.initialize(username, api_key)
sms = africastalking.SMS

HTML = """
<h2>Please Call Me App</h2>
<form method="POST" action="/pleasecall">
  Namba ya kumtumia: <input name="phone" placeholder="0712345678"><br><br>
  Namba yako: <input name="from" placeholder="0700000000"><br><br>
  <button type="submit">Tuma Please Call</button>
</form>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/pleasecall', methods=['POST'])
def pleasecall():
    phone_to = request.form.get('phone')
    phone_from = request.form.get('from', '0700000000')
    if not phone_to:
        return "Weka namba!"
    try:
        msg = f"Please call me. From {phone_from}"
        response = sms.send(msg, [phone_to])
        return f"Imetumwa kwa {phone_to}! {response}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
