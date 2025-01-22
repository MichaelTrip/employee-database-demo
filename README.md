# Employee Databas

## Overview
Simple Flask-based employee management web app for demonstration purposes.

## Prerequisites
- Python 3.9+
- Docker
- Kubernetes (optional)

## Local Development
```bash
# Clone & setup
git clone https://github.com/yourusername/employee-management-system.git
cd employee-management-system
python3 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
# Run
python app/app.py
# Docker
# Build & run
docker compose up
# Kubernetes
kubectl apply -f k8s/
```

# 🚨 Note

This is a demonstration project and not intended for production use. Lacks robust security and error handling.

# Technologies

* Python
* Flask
* PostgreSQL
* Docker
* Kubernetes
