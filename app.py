from flask import Flask, request

app = Flask(__name__)

# Ujumbe wa mwisho
last_msg = "Mum nipigie sina credit, nataka chakula"

@app.route('/')
def home():
    return f"""
    <h2>🎤 PleaseCall VOICE - Live</h2>
    <p>App iko sawa! Voice message: <b>{last_msg}</b></p>
    <form method="POST" action="/set">
        <label>Namba ya Mum: <input name="to" value="0722..." required></label><br><br>
        <label>Ujumbe wa sauti:</label><br>
        <select name="msg">
            <option>Mum nipigie sina credit, nataka chakula</option>
            <option>Mum niko danger, nipigie haraka</option>
            <option>Baba niko shambani, niletee maji</option>
        </select><br><br>
        <button type="submit">Mpigie Sasa</button>
    </form>
    <p><a href="/voice" target="_blank">Test Sauti (Voice XML)</a></p>
    """

@app.route('/set', methods=['POST'])
def set_msg():
    global last_msg
    to = request.form.get("to")
    msg = request.form.get("msg")
    last_msg = msg
    # Hapa baadaye tutaongeza voice.call(to)
    return f"<h3>✅ Sawa! Tutampigia {to} akisikia: '{msg}'</h3><a href='/'>Rudi nyuma</a>"

@app.route('/voice', methods=['GET','POST'])
def voice():
    # Hii ndio Mum atasikia akipokea simu
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="woman" playBeep="false">{last_msg}</Say>
    <Say>Please call back your child immediately.</Say>
    <Hangup/>
</Response>"""
    return xml, 200, {'Content-Type': 'text/xml'}

if __name__ == '__main__':
    app.run()
