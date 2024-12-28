from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# List to store orders
orders = []
order_id = 0

@app.route('/')
def home():
    return render_template('client.html')  # Client order page

@app.route('/admin')
def admin():
    return render_template('admin.html')  # Admin panel to see orders

@app.route('/submit_order', methods=['POST'])
def submit_order():
    global order_id
    order = request.json
    order_id += 1
    order['id'] = order_id
    order['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
    orders.append(order)

    # Emit the new order to all connected clients (admin panel)
    socketio.emit('new_order', order, broadcast=True)
    return jsonify({"message": "Order submitted successfully!"})

@app.route('/get_orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/get_order_details/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    order = next((order for order in orders if order['id'] == order_id), None)
    if order:
        return jsonify(order)
    else:
        return jsonify({"message": "Order not found!"}), 404

@socketio.on('connect')
def handle_connect():
    print("New client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, debug=True)
