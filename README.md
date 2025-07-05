# Stock Market Analytics System

A comprehensive real-time stock market analytics platform built with Python, Next.js, Django, Kafka, Redis, PostgreSQL, and AWS.

## Features

- Real-time stock price streaming and analysis
- WebSocket-based real-time alerts
- Advanced market trend detection
- High-performance data caching
- Scalable architecture with Kubernetes
- AWS deployment

## Tech Stack

- Backend: Python/Django
- Frontend: Next.js
- Real-time Processing: Kafka
- Caching: Redis
- Database: PostgreSQL
- Cloud: AWS
- Container Orchestration: Kubernetes

## Project Structure

```
stock-market-analytics/
├── stock_market_backend/     # Django backend
├── stock_analytics/         # Django app containing business logic
├── scripts/                # Utility scripts
├── docker/                # Docker configuration
├── k8s/                  # Kubernetes configuration
└── frontend/             # Next.js frontend
```

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8+
- Node.js 16+
- Docker and Docker Compose
- PostgreSQL
- Redis
- Kafka
- pipenv (recommended for Python virtual environment)

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stock-market-analytics.git
cd stock-market-analytics
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file and configure it:
```bash
cp .env.example .env
```
Edit `.env` with your desired configuration:
- Set your Django secret key
- Configure database settings
- Set Redis and Kafka connection details

5. Initialize the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

8. Start Kafka and Redis using Docker Compose:
```bash
docker-compose up -d
```

9. Run the stock data population script:
```bash
python scripts/populate_stocks.py
```

10. Start the Kafka consumer:
```bash
python manage.py run_consumer
```

11. Start the stock price simulation script:
```bash
python scripts/simulate_prices.py
```

## Running with Docker

1. Build and start all services:
```bash
docker-compose up --build
```

2. Access the application:
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- Admin panel: http://localhost:8000/admin
- Kafka UI: http://localhost:8080
- Redis UI: http://localhost:8081

## Production Deployment

1. Build Docker images:
```bash
docker-compose -f docker-compose.prod.yml build
```

2. Deploy to Kubernetes:
```bash
kubectl apply -f k8s/
```

3. Configure AWS services:
- RDS for PostgreSQL
- ElastiCache for Redis
- MSK for Kafka
- EKS for Kubernetes

## API Documentation

The API is documented using OpenAPI/Swagger and can be accessed at:
- http://localhost:8000/api/docs

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
