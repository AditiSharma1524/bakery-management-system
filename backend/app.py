from flask import Flask, request, jsonify
from flask_cors import CORS  # 🔥 Added for frontend-backend communication
import psycopg2
import pika  # Import pika for RabbitMQ communication

app = Flask(__name__)
CORS(app)  # 🔓 Enables CORS for all routes

def get_db_connection():
    return psycopg2.connect(
        dbname="bakery_db",
        user="bakery_user",
        password="bakery_pass",
        host="db",  # docker-compose service name
        port="5432"
    )

def publish_order_to_rabbitmq(order_id, product_id):
    # Use the correct credentials for RabbitMQ
    credentials = pika.PlainCredentials('bakery', 'bakery123')  # Correct credentials
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',
            credentials=credentials  # Pass credentials to the connection
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='orders_queue')  # Declare the queue (if not already declared)
    message = f"Order ID: {order_id}, Product ID: {product_id}"
    channel.basic_publish(exchange='',
                          routing_key='orders_queue', 
                          body=message)  # Send the message to the queue
    connection.close()

@app.route('/products', methods=['GET'])
def list_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route('/order', methods=['POST'])
def place_order():
    data = request.json
    product_id = data['product_id']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (product_id, quantity, status) VALUES (%s, %s, %s) RETURNING id;",
                (product_id, 1, 'pending'))  # Assuming 1 quantity for simplicity
    order_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    # Publish order to RabbitMQ after saving it to the DB
    publish_order_to_rabbitmq(order_id, product_id)

    return jsonify({"order_id": order_id})

@app.route('/order/<int:order_id>', methods=['GET'])
def check_order_status(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT status FROM orders WHERE id = %s;", (order_id,))
    status = cur.fetchone()
    cur.close()
    conn.close()
    if status:
        return jsonify({"status": status[0]})
    else:
        return jsonify({"error": "Order not found"}), 404

@app.route('/health', methods=['GET'])
def health_check():
    # This route will be used for the health check in Docker Compose
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
