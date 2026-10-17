# AgentOS Deployment Guide

## Production Deployment Checklist

### Pre-Deployment

- [ ] Change all default passwords and secrets
- [ ] Generate strong SECRET_KEY for JWT (use `openssl rand -hex 32`)
- [ ] Configure proper CORS origins
- [ ] Set up SSL/TLS certificates
- [ ] Configure production database with proper backups
- [ ] Set up Redis with persistence
- [ ] Configure OPA with production policies
- [ ] Set up monitoring and alerting
- [ ] Configure log aggregation
- [ ] Set up error tracking (Sentry, etc.)

### Security Hardening

1. **Secrets Management**
   - Use HashiCorp Vault or AWS Secrets Manager
   - Never commit secrets to git
   - Rotate secrets regularly
   - Use environment-specific secrets

2. **Network Security**
   - Use private networks for internal services
   - Configure firewall rules
   - Enable TLS 1.3 for all communications
   - Use internal load balancers

3. **Database Security**
   - Enable SSL for database connections
   - Use read replicas for scaling
   - Configure connection pooling
   - Enable query logging
   - Set up automated backups

4. **API Security**
   - Enable rate limiting
   - Configure API key management
   - Set up authentication (OAuth 2.0, SAML)
   - Enable request validation
   - Configure CORS properly

### Kubernetes Deployment

#### Namespace Configuration

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: agentos
```

#### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: agentos-config
  namespace: agentos
data:
  DATABASE_URL: "postgresql+asyncpg://user:pass@postgres:5432/agentos"
  REDIS_URL: "redis://redis:6379/0"
  OPA_URL: "http://opa:8181"
  OTEL_EXPORTER_JAEGER_ENDPOINT: "http://jaeger:4317"
```

#### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: agentos-secrets
  namespace: agentos
type: Opaque
stringData:
  SECRET_KEY: "your-production-secret-key"
  OPENAI_API_KEY: "your-openai-key"
  ANTHROPIC_API_KEY: "your-anthropic-key"
```

#### API Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentos-api
  namespace: agentos
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agentos-api
  template:
    metadata:
      labels:
        app: agentos-api
    spec:
      containers:
      - name: api
        image: agentos-backend:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: agentos-config
        - secretRef:
            name: agentos-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
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

#### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: agentos-api
  namespace: agentos
spec:
  selector:
    app: agentos-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Monitoring Setup

#### Prometheus Configuration

```yaml
scrape_configs:
  - job_name: 'agentos-api'
    static_configs:
      - targets: ['agentos-api:8000']
    metrics_path: /metrics
```

#### Grafana Dashboards

Import dashboards for:
- API performance
- Database performance
- Redis metrics
- Policy enforcement metrics
- Budget utilization
- Execution statistics

### Backup Strategy

#### Database Backups

```bash
# Daily backup
0 2 * * * pg_dump -U agentos agentos | gzip > /backups/agentos_$(date +\%Y\%m\%d).sql.gz

# Keep 30 days
find /backups -name "agentos_*.sql.gz" -mtime +30 -delete
```

#### Redis Persistence

```yaml
# In redis.conf
save 900 1
save 300 10
save 60 10000
appendonly yes
```

### Scaling Strategy

#### Horizontal Pod Autoscaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutautoscaler
metadata:
  name: agentos-api-hpa
  namespace: agentos
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agentos-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Disaster Recovery

1. **Multi-region deployment**
2. **Database replication**
3. **Redis clustering**
4. **Regular backup verification**
5. **Failover testing**
6. **Runbook documentation**

### Performance Tuning

#### Database

- Increase connection pool size
- Enable query caching
- Add appropriate indexes
- Tune work_mem and shared_buffers
- Use connection pooling (PgBouncer)

#### Redis

- Enable maxmemory-policy
- Configure persistence (AOF + RDB)
- Use Redis Cluster for scaling
- Tune connection pool size

#### Application

- Adjust worker count
- Configure async task queue
- Enable response caching
- Optimize database queries
- Use CDN for static assets

### Compliance

#### SOC 2 Type II

- Implement access controls
- Enable audit logging
- Set up change management
- Configure incident response
- Regular security assessments

#### GDPR

- Data residency
- Right to deletion
- Data portability
- Consent management
- Data breach notification

### Rollback Procedure

1. **Tag current deployment**
```bash
kubectl tag deployment agentos-api agentos-api:stable
```

2. **Rollback to previous version**
```bash
kubectl rollout undo deployment/agentos-api
```

3. **Verify rollback**
```bash
kubectl rollout status deployment/agentos-api
```

### Health Checks

```bash
# API health
curl https://api.agentos.com/health

# Database health
kubectl exec -it postgres-0 -- pg_isready

# Redis health
kubectl exec -it redis-0 -- redis-cli ping

# OPA health
curl http://opa:8181/health
```

### Log Aggregation

Use Loki or ELK stack:
- Centralized log collection
- Log retention policies
- Log analysis and alerting
- Log-based troubleshooting

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Check database is running
   - Verify connection string
   - Check network policies
   - Review connection pool settings

2. **High memory usage**
   - Check for memory leaks
   - Adjust resource limits
   - Review query patterns
   - Check caching configuration

3. **Slow API responses**
   - Check database query performance
   - Review N+1 query issues
   - Check external API latency
   - Review caching strategy

4. **Policy evaluation errors**
   - Check OPA is running
   - Verify policy syntax
   - Review policy logs
   - Test policy with OPA CLI

## Support and Maintenance

### Regular Tasks

- Daily: Review error logs and alerts
- Weekly: Review performance metrics
- Monthly: Security updates and patches
- Quarterly: Backup verification and DR testing
- Annually: Security audit and compliance review

### Emergency Contacts

- On-call engineer
- Database administrator
- Security team
- Management

## Upgrade Procedure

1. **Test in staging environment**
2. **Create backup**
3. **Deploy to canary**
4. **Monitor metrics**
5. **Gradual rollout**
6. **Verify functionality**
7. **Complete rollout**
