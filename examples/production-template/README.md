# Production Template

A complete template for deploying A2A agents in production environments. This example includes:

- 🐳 Docker containerization
- 🚀 Production-ready server configuration  
- 📊 Health checks and monitoring
- 🔧 Environment-based configuration
- 🔐 Security best practices
- 📝 Comprehensive logging
- ⚡ Performance optimizations

## 🏗️ Project Structure

```
production-template/
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Local development stack
├── docker-compose.prod.yml # Production configuration
├── requirements.txt        # Python dependencies
├── .dockerignore          # Docker ignore file
├── .env.example           # Environment variables template
├── src/
│   ├── __init__.py
│   ├── agent.py           # Production-ready agent
│   ├── config.py          # Configuration management
│   ├── health.py          # Health check endpoints
│   └── middleware.py      # Custom middleware
├── tests/
│   ├── __init__.py
│   ├── test_agent.py      # Unit tests
│   └── test_integration.py # Integration tests
├── deployment/
│   ├── k8s/               # Kubernetes manifests
│   ├── nginx/             # Reverse proxy config
│   └── monitoring/        # Prometheus, Grafana configs
└── scripts/
    ├── start.sh           # Startup script
    ├── health-check.sh    # Health check script
    └── migrate.sh         # Database migrations (if needed)
```

## 🚀 Quick Start

### Local Development with Docker

```bash
# Copy and configure environment
cp .env.example .env
# Edit .env with your settings

# Start development stack
docker-compose up -d

# View logs
docker-compose logs -f

# Run tests
docker-compose exec agent pytest
```

### Production Deployment

```bash
# Build production image
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Check health
curl http://localhost:8000/health
```

## 🔧 Configuration

### Environment Variables

```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000
WORKERS=4
LOG_LEVEL=INFO

# Agent Configuration  
AGENT_NAME="Production Agent"
AGENT_VERSION=1.0.0
MAX_MESSAGE_SIZE=10485760  # 10MB

# Security
API_KEY_HEADER=X-API-Key
CORS_ORIGINS=["http://localhost:3000"]

# Database (optional)
DATABASE_URL=postgresql://user:pass@db:5432/agents

# Monitoring
METRICS_ENABLED=true
HEALTH_CHECK_INTERVAL=30
```

### Production Features

1. **Graceful Shutdown**
2. **Request Rate Limiting**
3. **Comprehensive Error Handling**
4. **Structured Logging**
5. **Health Check Endpoints**
6. **Metrics Collection**
7. **Security Headers**
8. **Request Validation**

## 🐳 Docker Configuration

### Multi-stage Dockerfile

```dockerfile
# Build stage
FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage  
FROM python:3.12-slim
WORKDIR /app

# Copy dependencies
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application
COPY src/ ./src/
COPY scripts/ ./scripts/

# Set up user
RUN groupadd -r agent && useradd -r -g agent agent
RUN chown -R agent:agent /app
USER agent

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \\
  CMD python scripts/health-check.sh

EXPOSE 8000
CMD ["python", "-m", "src.agent"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: a2a-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: a2a-agent
  template:
    metadata:
      labels:
        app: a2a-agent
    spec:
      containers:
      - name: agent
        image: my-registry/a2a-agent:latest
        ports:
        - containerPort: 8000
        env:
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

## 📊 Monitoring & Observability

### Health Checks

- **`/health`** - Basic health status
- **`/ready`** - Readiness for traffic  
- **`/metrics`** - Prometheus metrics
- **`/version`** - Agent version info

### Logging

Structured JSON logging with:
- Request IDs for tracing
- Performance metrics
- Error tracking
- Security events

### Metrics

- Request count and latency
- Agent response times
- Error rates
- Resource usage

## 🔐 Security Features

- Input validation and sanitization
- Rate limiting per client
- API key authentication
- CORS configuration
- Security headers
- Request size limits

## 🧪 Testing

```bash
# Unit tests
pytest tests/test_agent.py

# Integration tests  
pytest tests/test_integration.py

# Load testing
docker-compose run --rm load-test

# Security testing
docker-compose run --rm security-test
```

## 🚀 Deployment Strategies

### Blue-Green Deployment

```bash
# Deploy new version
docker-compose -f docker-compose.prod.yml up -d agent-green

# Health check
./scripts/health-check.sh http://localhost:8001

# Switch traffic
# Update load balancer configuration

# Remove old version
docker-compose -f docker-compose.prod.yml stop agent-blue
```

### Rolling Updates (Kubernetes)

```bash
# Update image
kubectl set image deployment/a2a-agent agent=my-registry/a2a-agent:v2.0.0

# Monitor rollout
kubectl rollout status deployment/a2a-agent

# Rollback if needed
kubectl rollout undo deployment/a2a-agent
```

## 📚 Best Practices Implemented

1. **Configuration Management** - Environment-based config
2. **Logging Strategy** - Structured, searchable logs
3. **Error Handling** - Comprehensive error responses
4. **Performance** - Connection pooling, caching
5. **Security** - Authentication, input validation
6. **Monitoring** - Health checks, metrics
7. **Testing** - Unit, integration, load tests
8. **Documentation** - API docs, deployment guides

---

**Ready for production?** 🚀 This template provides everything you need for a robust, scalable A2A agent deployment.