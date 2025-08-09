## Introduction
**DeployFlow** is a cloud-native platform designed as proof of concept for deploying html files to object storage using workflows. It integrates various services such as RabbitMQ, PostgreSQL, MinIO, and Prometheus to provide a simple html file deployment solution :))

## Topology
![screenshot](docs/topology.png)

The platform is built using Docker and Docker Compose, enabling easy deployment and management of microservices. It also includes a pre-configured NGINX proxy for serving static files on object storage.

## Features
- **API Services**: Provides RESTful APIs for deploying html files and getting status of workflows.
![screenshot](docs/api.png)
- **Workers**: Listens related message queues and handles background tasks such as file uploads and validations using Celery.
- **Monitoring**: Includes Prometheus and Grafana for real-time monitoring and visualization.
![screenshot](docs/grafana.png)
- **Message Queue**: RabbitMQ for reliable message delivery between services.
- **Object Storage**: 2 MinIO instances for scalable and secure object storage. It replicates files from minio1's **source bucket** to minio2's **target bucket**.
- **Database**: PostgreSQL for persistent data storage.
- **Dashboard**: Celery Flower dashboard and Celery Insights for monitoring tasks, task queues and workers.


## Getting Started
### Prerequisites
- Docker (version 20.10 or later)
- Docker Compose (version 1.29 or later)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/haidouks/DeployFlow
   cd DeployFlow
   ```

2. Start the services:
   ```bash
   docker-compose up --build
   ```

3. Access the services:
   - API: `http://localhost:8000/docs`
   - NGINX Proxy: `http://localhost:8082`
   - Grafana: `http://localhost:3000`
   - Prometheus: `http://localhost:9090`
   - Flower Dashboard: `http://localhost:5555`
   - Celery Insights: `http://localhost:8555`

## Usage
- Upload files to MinIO via the `mc` CLI or API.
- Monitor tasks and workers using the Flower dashboard.
- Visualize metrics and logs in Grafana and Prometheus.

## Out of Scope
- Authentication and Authorization of components are out of scopes
- High availability
- Pre-Deployment pipeline tasks such as vulnerability, unit tests, code coverages, ...
- ...
