from flask import Flask, render_template, redirect, url_for, request
import threading
import time
from datetime import datetime

from classes import Hardware

app = Flask(__name__)

# Use the same relay pin as existing scripts
RELAY = Hardware.Relay(12, False)

# Simple state to show on the UI
state = {
    'watering': False,
    'last_watered': None
}
state_lock = threading.Lock()


def _do_watering(seconds):
    with state_lock:
        state['watering'] = True
    try:
        RELAY.on()
        time.sleep(seconds)
        RELAY.off()
        with state_lock:
            state['last_watered'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    finally:
        with state_lock:
            state['watering'] = False


@app.route('/')
def index():
    with state_lock:
        current = dict(state)
    return render_template('index.html', state=current)


@app.route('/start', methods=['POST'])
def start():
    seconds = int(request.form.get('seconds', 10))
    with state_lock:
        if state['watering']:
            # already watering; just redirect
            return redirect(url_for('index'))
    t = threading.Thread(target=_do_watering, args=(seconds,), daemon=True)
    t.start()
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Run on all interfaces so you can access from other devices on the LAN
    app.run(host='0.0.0.0', port=5000, debug=True)
