from flask import Flask, request, render_template, redirect, url_for, jsonify
# from flask_socketio import SocketIO, emit
from flask_sock import Sock
import sqlite3
import json

app = Flask(__name__)
sock = Sock(app)

database = "local_control_db.db"

# example: <esp_id>: <WebSocket>
    # "001": <WebSocket>
    # "002": <Websocket>
clients = {}

def get_db():
    return sqlite3.connect(database)

# @app.route("/data", methods=['POST'])
# def receive_espdata():
#     payload = request.json
#     temperature = payload.get("temperature")

#     with get_db() as conn:
#         cur = conn.cursor()
#         cur.execute(
#             "INSERT INTO readings (temperature) VALUES (?)", (temperature,)
#         )
#         conn.commit()

#     return jsonify({"status":"ok"}), 200

# @app.route("/data", methods=['POST'])
# def receive_dbdata():

#     with get_db() as conn:
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM readings")
#         rows = cur.fetchall()

#     return jsonify(rows)

# <esp-id> this notation is like passing a parameter into the function via the url path that you put into the browser
@app.route('/device/<esp_id>/change_state', methods=['GET', 'POST'])
def change_state(esp_id):
    if request.method == "POST":
        data = request.json

        device_id = data["device_id"]
        desired_state = data["desired_state"]
        # actual_state = data["actual_state"]

        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("""INSERT INTO device_state (device_id, desired_state)
                            VALUES (?, ?)
                            ON CONFLICT(device_id)
                            DO UPDATE SET desired_state=?, updated_at=CURRENT_TIMESTAMP"""
                        , (device_id, desired_state, desired_state))
            conn.commit()

    # we must send the desired state to the esp32
        # the esp_id name is to retrieve the web_socket object from the dictionary and slot it into the
        # the ws variable carries the websocket object that is the destination of the json payload 
        ws = clients.get(esp_id)
        if ws:
            ws.send(json.dumps({
                "device_id": device_id,
                "desired_state": desired_state
            }))
            # ws.close(reason=1000)

        return {"status": "ok", "esp_id": esp_id}
    else:
        return render_template("state_demo.html")
    
@app.route("/device/actual_state", methods=["POST"])
def actual_state():
    # then we must then receive confirmation that the esp32 has updated to the desired state
    data = request.json
    device_id = data["device_id"]
    actual_state = data["actual_state"]

    # then update the data base to reflect the actual state is the desired state 
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE device_state SET actual_state = ? WHERE device_id = ?",
                    (actual_state, device_id))
        conn.commit()

    return jsonify({"status" : "actual_state updated"})

# when esp first registers itself it adds an esp id for itself for future reference
@sock.route("/ws")
def websocket(ws):
    while True:
        data = ws.receive()
        if data is None:
            break

        msg = json.loads(data)

        if msg.get("type") == "register":
            esp_id = msg["esp_id"]
            clients[esp_id] = ws
            print(f"{esp_id} connected")

        elif msg.get("type") == "ping":
            ws.send(json.dumps({"type": "pong"}))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # make a change to the database when the user inputs some info on the web site so that the esp 32 and read that information and make provide
        # an appropiate output>>

        led_switch = request.form['led_switch']
        buzzer_switch = request.form['buzzer_switch']
        lcd_message = request.form['lcd_message']


        return render_template('index.html', led=led_switch, buzz=buzzer_switch, lcd=lcd_message)
    else:
        return render_template('index.html')
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    # Sock.init_app(app) 
    # app.run(debug=True)