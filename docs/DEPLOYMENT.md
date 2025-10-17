# Deployment Guide

This guide covers deploying the Mars Landing Backend to various environments.

## Prerequisites

- Docker and Docker Compose installed
- Domain name configured (for production)
- SSL certificates (for production)
- Environment variables configured

## Environment Setup

### 1. Development Environment

```bash
# Clone repository
git clone <repository-url>
cd marslanding

# Copy environment file
cp env.example .env

# Edit configuration
nano .env

# Start services
make docker-run
```

### 2. Staging Environment

```bash
# Copy staging environment
cp env.example .env.staging

# Configure staging settings
nano .env.staging

# Deploy to staging
make deploy-staging
```

### 3. Production Environment

```bash
# Copy production environment
cp env.example .env.production

# Configure production settings
nano .env.production

# Deploy to production
make deploy
```

## Docker Deployment

### Development Deployment

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment

```bash
# Deploy with production configuration
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down
```

## Manual Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
```

### 2. Application Deployment

```bash
# Clone repository
git clone <repository-url>
cd marslanding

# Set up environment
cp env.production .env.production
nano .env.production

# Deploy
make deploy
```

### 3. SSL Certificate Setup

```bash
# Install Certbot
sudo apt install certbot

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates to nginx directory
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/key.pem
```

## Cloud Deployment

### AWS Deployment

#### Using ECS

1. **Create ECS Cluster:**
```bash
aws ecs create-cluster --cluster-name mission-astro
```

2. **Create Task Definition:**
```json
{
  "family": "mission-astro-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "your-account.dkr.ecr.region.amazonaws.com/mission-astro-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ]
    }
  ]
}
```

3. **Create Service:**
```bash
aws ecs create-service \
  --cluster mission-astro \
  --service-name backend-service \
  --task-definition mission-astro-backend:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
```

#### Using EC2

1. **Launch EC2 Instance:**
```bash
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --count 1 \
  --instance-type t3.medium \
  --key-name your-key-pair \
  --security-group-ids sg-12345 \
  --subnet-id subnet-12345
```

2. **Connect and Deploy:**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
# Follow manual deployment steps
```

### Google Cloud Deployment

#### Using Cloud Run

1. **Build and Push Image:**
```bash
gcloud builds submit --tag gcr.io/your-project/mission-astro-backend
```

2. **Deploy to Cloud Run:**
```bash
gcloud run deploy mission-astro-backend \
  --image gcr.io/your-project/mission-astro-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Using GKE

1. **Create Cluster:**
```bash
gcloud container clusters create mission-astro-cluster \
  --num-nodes=3 \
  --zone=us-central1-a
```

2. **Deploy Application:**
```bash
kubectl apply -f k8s/
```

### Azure Deployment

#### Using Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name mission-astro-backend \
  --image your-registry.azurecr.io/mission-astro-backend:latest \
  --dns-name-label mission-astro-backend \
  --ports 8000
```

#### Using AKS

```bash
# Create AKS cluster
az aks create \
  --resource-group myResourceGroup \
  --name mission-astro-cluster \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Deploy application
kubectl apply -f k8s/
```

## Kubernetes Deployment

### 1. Create Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: mission-astro
```

### 2. ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-config
  namespace: mission-astro
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
  MONGODB_DATABASE: "mission_astro"
```

### 3. Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: backend-secrets
  namespace: mission-astro
type: Opaque
data:
  SECRET_KEY: <base64-encoded-secret>
  MONGODB_URL: <base64-encoded-url>
  REDIS_URL: <base64-encoded-url>
```

### 4. Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: mission-astro
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: mission-astro-backend:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: backend-config
        - secretRef:
            name: backend-secrets
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 5. Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: mission-astro
spec:
  selector:
    app: backend
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 6. Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: backend-ingress
  namespace: mission-astro
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - api.your-domain.com
    secretName: backend-tls
  rules:
  - host: api.your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 80
```

## CI/CD Pipeline

### GitHub Actions

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Registry
      uses: docker/login-action@v2
      with:
        registry: your-registry.com
        username: ${{ secrets.REGISTRY_USERNAME }}
        password: ${{ secrets.REGISTRY_PASSWORD }}
    
    - name: Build and Push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: your-registry.com/mission-astro-backend:latest
    
    - name: Deploy to Production
      run: |
        ssh ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }} << 'EOF'
          cd /path/to/backend
          docker-compose -f docker-compose.prod.yml pull
          docker-compose -f docker-compose.prod.yml up -d
        EOF
```

### GitLab CI

```yaml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

build:
  stage: build
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE

test:
  stage: test
  script:
    - docker run --rm $DOCKER_IMAGE make test

deploy:
  stage: deploy
  script:
    - docker-compose -f docker-compose.prod.yml up -d
  only:
    - main
```

## Monitoring and Logging

### Health Checks

```bash
# Check application health
curl http://localhost:8000/health

# Check detailed health
curl http://localhost:8000/api/v1/health/detailed
```

### Log Monitoring

```bash
# View application logs
docker-compose logs -f backend

# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f mongodb
```

### Metrics

```bash
# View Prometheus metrics
curl http://localhost:8000/metrics
```

## Backup and Recovery

### Database Backup

```bash
# Create backup
docker-compose exec mongodb mongodump --out /backup

# Copy backup from container
docker cp mission-astro-mongodb:/backup ./backup

# Restore from backup
docker-compose exec mongodb mongorestore /backup
```

### Automated Backups

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/mongodb"
CONTAINER_NAME="mission-astro-mongodb"

# Create backup
docker exec $CONTAINER_NAME mongodump --out /backup_$DATE

# Copy to host
docker cp $CONTAINER_NAME:/backup_$DATE $BACKUP_DIR/

# Compress backup
tar -czf $BACKUP_DIR/backup_$DATE.tar.gz -C $BACKUP_DIR backup_$DATE

# Remove uncompressed backup
rm -rf $BACKUP_DIR/backup_$DATE

# Keep only last 7 days of backups
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete
```

## Troubleshooting

### Common Issues

1. **Container won't start:**
```bash
# Check logs
docker-compose logs backend

# Check container status
docker-compose ps
```

2. **Database connection failed:**
```bash
# Check MongoDB logs
docker-compose logs mongodb

# Test connection
docker-compose exec backend python -c "from app.db.mongodb import connect_to_mongo; import asyncio; asyncio.run(connect_to_mongo())"
```

3. **Port conflicts:**
```bash
# Check what's using the port
sudo netstat -tulpn | grep :8000

# Change port in .env file
echo "PORT=8001" >> .env
```

### Performance Issues

1. **High memory usage:**
```bash
# Check container stats
docker stats

# Increase memory limits in docker-compose.yml
```

2. **Slow database queries:**
```bash
# Check MongoDB logs
docker-compose logs mongodb

# Optimize indexes
docker-compose exec mongodb mongosh
```

## Security Considerations

1. **Environment Variables:**
   - Never commit `.env` files
   - Use strong passwords
   - Rotate secrets regularly

2. **Network Security:**
   - Use HTTPS in production
   - Configure firewall rules
   - Use VPN for database access

3. **Container Security:**
   - Use non-root users
   - Keep images updated
   - Scan for vulnerabilities

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.prod.yml
services:
  backend:
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

### Load Balancing

```yaml
# nginx.conf
upstream backend {
    least_conn;
    server backend_1:8000;
    server backend_2:8000;
    server backend_3:8000;
}
```

### Database Scaling

```yaml
# MongoDB replica set
services:
  mongodb-primary:
    image: mongo:7.0
    command: mongod --replSet rs0
    
  mongodb-secondary:
    image: mongo:7.0
    command: mongod --replSet rs0
```
