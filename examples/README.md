# A2A Python SDK Examples

This directory contains practical examples demonstrating different patterns and use cases for building A2A agents.

## 🚀 Quick Start

1. **Install dependencies** (from project root):
   ```bash
   pip install -e ".[http-server]"
   ```

2. **Choose an example** and follow its README

3. **Run the example**:
   ```bash
   cd examples/simple-echo-agent
   python agent.py
   ```

## 📁 Available Examples

### 🔤 [Simple Echo Agent](./simple-echo-agent/)
**Perfect for beginners** - A basic agent that echoes back messages.
- Single skill implementation
- HTTP JSON-RPC transport
- Basic error handling
- Client usage examples

### 📄 [File Processing Agent](./file-processor/)
**Document handling** - Process and transform files/documents.
- Binary data handling
- Multiple input formats (PDF, TXT, JSON)
- Artifact creation and manipulation
- File upload/download patterns

### 🎯 [Multi-Skill Agent](./multi-skill-agent/)
**Complex capabilities** - Agent with multiple skills and abilities.
- Multiple skill registration
- Skill routing and selection
- Different input/output modes per skill
- Advanced agent card configuration

### ⚡ [gRPC Agent](./grpc-agent/)
**High-performance** - Binary protocol for low-latency communication.
- gRPC transport implementation
- Protocol buffer definitions
- Streaming message handling
- Performance optimization patterns

### 🔐 [Authenticated Agent](./auth-agent/)
**Security patterns** - Secure agent with authentication.
- API key authentication
- OAuth2 integration
- Secure client configuration
- Permission-based access

### 🗄️ [Database Agent](./database-agent/)
**Data integration** - Agent that interacts with databases.
- SQL query execution
- Database connection management
- Data transformation
- Result formatting

### 🔄 [Workflow Agent](./workflow-agent/)
**Process orchestration** - Chain multiple operations together.
- Multi-step workflows
- State management
- Progress tracking
- Error recovery

### 🚀 [Production Template](./production-template/)
**Deployment ready** - Full-featured template for production use.
- Complete project structure
- Docker configuration
- Logging and monitoring
- Health checks
- CI/CD examples

## 🛠️ Development Utilities

### 📋 [Client Examples](./clients/)
Various client patterns for testing and integration:
- Simple message sending
- Streaming response handling
- Batch processing
- Error handling patterns

### 🔧 [Utilities](./utils/)
Helper scripts and tools:
- Agent validator
- Performance benchmarks
- Development server
- Test data generators

## 📖 Usage Patterns

### Running an Example

```bash
# 1. Navigate to example directory
cd examples/simple-echo-agent

# 2. Start the agent server
python agent.py

# 3. In another terminal, test with client
python test_client.py
```

### Testing an Agent

```bash
# Use the agent validator utility
python examples/utils/validate_agent.py http://localhost:8000

# Or test with curl
curl -X GET http://localhost:8000/agent-card
```

### Development Mode

Most examples support development mode with auto-reload:

```bash
# Run with auto-reload
python agent.py --reload

# Or use uvicorn directly
uvicorn agent:app --reload --host 0.0.0.0 --port 8000
```

## 🎯 Choosing the Right Example

| Use Case | Example | Complexity | Features |
|----------|---------|------------|----------|
| Learning A2A basics | Simple Echo | ⭐ | Message handling, basic responses |
| File processing | File Processor | ⭐⭐ | Binary data, artifacts, transformations |
| Multiple capabilities | Multi-Skill | ⭐⭐ | Skill routing, complex agent cards |
| High performance | gRPC Agent | ⭐⭐⭐ | Binary protocol, streaming |
| Security requirements | Auth Agent | ⭐⭐ | Authentication, authorization |
| Data integration | Database Agent | ⭐⭐ | SQL, data transformation |
| Complex workflows | Workflow Agent | ⭐⭐⭐ | State management, orchestration |
| Production deployment | Production Template | ⭐⭐⭐ | Complete setup, monitoring |

## 🤝 Contributing Examples

Have a great A2A pattern or use case? We'd love to see it!

1. **Fork the repository**
2. **Create your example** in a new directory
3. **Include a complete README** with:
   - Purpose and use case
   - Setup instructions
   - Usage examples
   - Key concepts demonstrated
4. **Test thoroughly** with different scenarios
5. **Submit a pull request**

### Example Template Structure

```
examples/my-new-example/
├── README.md           # Detailed documentation
├── agent.py           # Main agent implementation
├── test_client.py     # Client usage example
├── requirements.txt   # Additional dependencies
├── config.py         # Configuration (if needed)
├── docker/           # Docker setup (if applicable)
└── tests/            # Unit tests (optional but encouraged)
```

## 📚 Additional Resources

- 📖 [Getting Started Guide](../GETTING_STARTED.md)
- 🔗 [API Documentation](https://a2a-protocol.org/latest/sdk/python/)
- 🏠 [A2A Protocol Specification](https://a2a-protocol.org)
- 💬 [Community Discussions](https://github.com/a2aproject/a2a-python/discussions)

---

**Ready to build something amazing with A2A?** Start with the Simple Echo Agent and work your way up! 🚀