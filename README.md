🍞 Bakery Management System

📜 Project Overview


The Bakery Management System is a containerized multi-service application designed to manage bakery products, orders, and order statuses.
It showcases Docker containerization, service orchestration, networking, and inter-service communication using PostgreSQL, RabbitMQ, a backend API service, and a worker service.





🛠️ System Architecture
                          
Frontend: User interface to browse products and place orders.

Backend API: Serves APIs for product listing, order placement, and order tracking.

Worker Service: Processes orders asynchronously by consuming messages from RabbitMQ.

PostgreSQL: Stores products and orders.

RabbitMQ: Message broker for decoupling order placement and order processing.

🚀 Setup Instructions
Prerequisites
Docker

Docker Compose

Installation Steps
Clone the repository


git clone <your-repo-link>
cd bakery-system

Build and run the containers:

docker-compose up --build

Access the services:

Frontend: http://localhost:3000

Backend API: http://localhost:8000

RabbitMQ Management UI (Optional): http://localhost:15672
(Username: bakery, Password: bakery123)

To stop the services:
docker-compose down

🧩 API Documentation
1. List Products
Endpoint: GET /products

Description: Fetch all bakery products.

Response:



  {
    "id": 1,
    "name": "Chocolate Cake",
    "price": 500
  }

2. Place an Order
Endpoint: POST /order

Description: Place a new order.

Request Body:


{
  "product_id": 1,
  "quantity": 2
}
Response:

{
  "message": "Order placed successfully!",
  "order_id": 101
}
3. Check Order Status
Endpoint: GET /order/:id

Description: Check the status of an order.

Response:


{
  "order_id": 101,
  "status": "Completed"
}

⚙️ Advanced Features Implemented
Separate Backend API and Worker Containers:

backend/app.py (API Server) → Dockerfile.app

backend/worker.py (Worker Service) → Dockerfile.worker

Health Checks:

Docker Compose monitors PostgreSQL, RabbitMQ, and the backend API using container health checks to improve resilience.

Asynchronous Order Processing:

Orders are processed in the background using a worker service, ensuring fast frontend responsiveness.

RabbitMQ for Decoupling:

Loose coupling between order placement and order processing for better scalability.

Simple Lightweight Frontend:

Minimalistic frontend for quick browsing and order placement without frontend frameworks.

🗂️ Repository Structure
/

backend/              
app.py             # Backend API application

worker.py          # Worker service

Dockerfile.app     # Dockerfile for API service

Dockerfile.worker  # Dockerfile for worker service

requirements.txt   # Python dependencies

frontend/              

index.html         # Frontend UI

docker-compose.yml     # Docker Compose orchestration file

README.md              # Project documentation

.gitignore             # Git ignored files

docs/

architecturual_diagram.png   # Architecture diagram 

🎉 Thank you for checking out the Bakery Management System!
