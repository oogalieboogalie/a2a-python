# Getting Started with A2A Python SDK

## 🌟 Welcome to A2A Development!

This guide will walk you through building your first Agent-to-Agent (A2A) applications using the Python SDK. Whether you're creating a simple echo agent or a complex multi-service system, this guide provides patterns and examples to get you started quickly.

## 📋 Prerequisites

- **Python 3.10+** (Python 3.12+ recommended)
- **uv** (recommended) or **pip**
- Basic understanding of async/await in Python

## 🚀 Quick Setup

### 1. Install the SDK

Choose your installation based on the features you need:

```bash
# Core SDK only
pip install a2a-sdk

# HTTP server support (most common)
pip install "a2a-sdk[http-server]"

# gRPC support
pip install "a2a-sdk[grpc]"

# Everything included
pip install "a2a-sdk[all]"
```

### 2. Verify Installation

```python
import a2a
from a2a.client import Client
from a2a.server.apps import A2AFastAPIApplication

print("A2A SDK installed successfully!")
```

## 🎯 Core Concepts

### Agent Card
Every A2A agent must provide an **Agent Card** - a manifest describing the agent's capabilities, supported transport protocols, and available skills.

### Skills
**Skills** are the individual capabilities your agent provides. Each skill defines:
- Input/output formats (MIME types)
- Description and usage information
- Implementation logic

### Transport Protocols
A2A supports multiple transport mechanisms:
- **JSON-RPC over HTTP** (most common)
- **REST API** 
- **gRPC** (for high-performance scenarios)

### Artifacts
**Artifacts** are structured data objects that agents exchange. They can contain:
- Text content
- Structured data (JSON)
- Binary data
- Mixed content types

## 📁 Project Structure

Here's the recommended structure for A2A projects:

```
my-a2a-agent/
├── pyproject.toml          # Project configuration
├── README.md               # Agent documentation
├── src/
│   └── my_agent/
│       ├── __init__.py
│       ├── agent.py        # Main agent implementation
│       ├── skills/         # Individual skill implementations
│       │   ├── __init__.py
│       │   └── my_skill.py
│       └── config.py       # Configuration
├── tests/
│   ├── __init__.py
│   └── test_agent.py
├── examples/
│   ├── client_example.py   # Example client usage
│   └── run_server.py       # Development server
└── docker/
    ├── Dockerfile
    └── docker-compose.yml
```

## 🏗️ Building Your First Agent

Let's create a simple echo agent that demonstrates core A2A patterns:

### 1. Create the Project

```bash
mkdir my-echo-agent
cd my-echo-agent
```

### 2. Set up pyproject.toml

```toml
[project]
name = "my-echo-agent"
version = "0.1.0"
description = "A simple A2A echo agent"
requires-python = ">=3.10"
dependencies = [
    "a2a-sdk[http-server]>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 3. Implement the Agent

```python
# src/my_echo_agent/agent.py
import asyncio
import logging
from typing import AsyncIterator

from a2a.server.apps import A2AFastAPIApplication
from a2a.types import (
    AgentCard, 
    AgentCapabilities, 
    Message, 
    Skill, 
    Task,
    TransportProtocol
)
from a2a.utils.artifact import new_text_artifact

logger = logging.getLogger(__name__)

class EchoAgent:
    """A simple echo agent that repeats back messages."""
    
    def __init__(self):
        self.app = A2AFastAPIApplication()
        self._setup_agent()
    
    def _setup_agent(self):
        """Configure the agent with its capabilities and skills."""
        # Define agent card
        agent_card = AgentCard(
            name="Echo Agent",
            description="A simple agent that echoes back messages",
            url="http://localhost:8000",
            version="1.0.0",
            capabilities=AgentCapabilities(
                streaming=True,
                push_notifications=False
            ),
            skills=[
                Skill(
                    name="echo",
                    description="Echoes back the input message",
                    input_modes=["text/plain"],
                    output_modes=["text/plain"]
                )
            ],
            default_input_modes=["text/plain"],
            default_output_modes=["text/plain"],
            preferred_transport=TransportProtocol.jsonrpc
        )
        
        # Set the agent card
        self.app.agent_card = agent_card
        
        # Register message handler
        self.app.set_message_handler(self.handle_message)
    
    async def handle_message(self, task: Task) -> AsyncIterator[Message]:
        """Handle incoming messages and echo them back."""
        try:
            logger.info(f"Received task: {task.task_id}")
            
            # Extract text from the message
            text_content = ""
            if task.message and task.message.parts:
                for part in task.message.parts:
                    if hasattr(part.root, 'text'):
                        text_content += part.root.text
            
            # Create echo response
            echo_text = f"Echo: {text_content}"
            
            # Create response artifact
            response_artifact = new_text_artifact(
                name="echo_response",
                text=echo_text,
                description="Echoed message response"
            )
            
            # Yield the response message
            yield Message(
                artifacts=[response_artifact],
                parts=[]
            )
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            # Yield error response
            error_artifact = new_text_artifact(
                name="error_response",
                text=f"Error: {str(e)}",
                description="Error response"
            )
            yield Message(
                artifacts=[error_artifact],
                parts=[]
            )

# Create agent instance
agent = EchoAgent()
app = agent.app.fastapi_app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agent:app", host="0.0.0.0", port=8000, reload=True)
```

### 4. Create a Test Client

```python
# examples/client_example.py
import asyncio
from a2a.client import ClientFactory
from a2a.utils.artifact import new_text_artifact
from a2a.types import Message

async def test_echo_agent():
    """Test the echo agent with a simple message."""
    # Create client
    client_factory = ClientFactory()
    client = await client_factory.create_client("http://localhost:8000")
    
    # Create test message
    test_artifact = new_text_artifact(
        name="test_message",
        text="Hello, A2A World!",
        description="Test message for echo agent"
    )
    
    message = Message(
        artifacts=[test_artifact],
        parts=[]
    )
    
    # Send message and get response
    print("Sending message to echo agent...")
    responses = []
    async for response in client.send_message(message):
        responses.append(response)
        print(f"Received response: {response}")
    
    print(f"Total responses received: {len(responses)}")
    
    # Clean up
    await client.close()

if __name__ == "__main__":
    asyncio.run(test_echo_agent())
```

### 5. Run Your Agent

```bash
# Terminal 1 - Start the agent server
cd my-echo-agent
python src/my_echo_agent/agent.py

# Terminal 2 - Test with the client
python examples/client_example.py
```

## 🛠️ Development Patterns

### Error Handling Pattern

```python
async def robust_message_handler(self, task: Task) -> AsyncIterator[Message]:
    """Message handler with comprehensive error handling."""
    try:
        # Process message
        result = await self.process_task(task)
        yield self.create_success_response(result)
        
    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        yield self.create_error_response(f"Invalid input: {e}")
        
    except ProcessingError as e:
        logger.error(f"Processing error: {e}")
        yield self.create_error_response(f"Processing failed: {e}")
        
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        yield self.create_error_response("Internal server error")
```

### Configuration Management

```python
# src/my_agent/config.py
from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class AgentConfig:
    """Configuration for the agent."""
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    log_level: str = "INFO"
    
    # Agent-specific settings
    max_message_size: int = 1024 * 1024  # 1MB
    timeout_seconds: int = 30
    
    @classmethod
    def from_env(cls) -> 'AgentConfig':
        """Load configuration from environment variables."""
        return cls(
            host=os.getenv('AGENT_HOST', '0.0.0.0'),
            port=int(os.getenv('AGENT_PORT', '8000')),
            debug=os.getenv('AGENT_DEBUG', 'false').lower() == 'true',
            log_level=os.getenv('AGENT_LOG_LEVEL', 'INFO'),
        )
```

### Testing Pattern

```python
# tests/test_agent.py
import pytest
from unittest.mock import AsyncMock

from a2a.types import Task, Message
from my_agent.agent import EchoAgent

@pytest.mark.asyncio
async def test_echo_agent_basic():
    """Test basic echo functionality."""
    agent = EchoAgent()
    
    # Create test task
    task = Task(
        task_id="test-123",
        message=Message(...)  # Your test message
    )
    
    # Process task
    responses = []
    async for response in agent.handle_message(task):
        responses.append(response)
    
    # Verify response
    assert len(responses) == 1
    assert "Echo:" in str(responses[0])
```

## 🎨 Advanced Examples

The `examples/` directory contains more sophisticated patterns:

- **File Processing Agent** - Handle document uploads and transformations
- **Multi-Skill Agent** - Support multiple capabilities in one agent
- **gRPC Agent** - High-performance binary protocol support
- **Authenticated Agent** - Secure agent with API key authentication
- **Database Agent** - Agent that interacts with databases
- **Workflow Agent** - Chain multiple operations together

## 🚢 Deployment

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install -e .

EXPOSE 8000
CMD ["python", "src/my_agent/agent.py"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  echo-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - AGENT_LOG_LEVEL=INFO
      - AGENT_DEBUG=false
    restart: unless-stopped
```

## 📚 Next Steps

1. **Explore Examples** - Check out the `examples/` directory for more patterns
2. **Read the API Docs** - Understand the full SDK capabilities
3. **Join the Community** - Connect with other A2A developers
4. **Build Your Use Case** - Apply these patterns to your specific needs

## 🔧 Troubleshooting

### Common Issues

**Import Errors**
```bash
# Make sure you have the right extras installed
pip install "a2a-sdk[http-server]"
```

**Connection Refused**
```bash
# Check if your agent is running on the correct port
curl http://localhost:8000/agent-card
```

**Async Errors**
```python
# Always use async/await with A2A client methods
response = await client.send_message(message)  # Correct
response = client.send_message(message)         # Wrong
```

### Getting Help

- 📖 [Full Documentation](https://a2a-protocol.org/latest/sdk/python/)
- 🐛 [Report Issues](https://github.com/a2aproject/a2a-python/issues)
- 💬 [Community Discussions](https://github.com/a2aproject/a2a-python/discussions)
- 📧 [Email Support](mailto:support@a2a-protocol.org)

---

**Happy A2A Development!** 🚀