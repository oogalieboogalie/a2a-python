# Simple Echo Agent

This is the perfect starting point for learning A2A development. The Echo Agent demonstrates the fundamental concepts:

- 🔄 Message handling patterns
- 📋 Agent card configuration
- 🚀 HTTP JSON-RPC transport
- ✨ Artifact creation and responses
- 🧪 Client usage examples

## 🎯 What This Agent Does

The Echo Agent receives messages and responds with the same content prefixed by "Echo: ". It's simple but demonstrates all the core A2A patterns you'll use in more complex agents.

## 🚀 Quick Start

### 1. Install Dependencies

From the project root:
```bash
pip install -e ".[http-server]"
```

### 2. Run the Agent

```bash
cd examples/simple-echo-agent
python agent.py
```

The agent will start on `http://localhost:8000` and display:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 3. Test the Agent

In another terminal:
```bash
# Test with the provided client
python test_client.py

# Or check the agent card
curl http://localhost:8000/agent-card
```

## 📁 Files in This Example

- **`agent.py`** - Main agent implementation
- **`test_client.py`** - Example client that sends test messages
- **`README.md`** - This documentation
- **`requirements.txt`** - Additional dependencies (none for this example)

## 🔍 Key Concepts Demonstrated

### 1. Agent Card Configuration

```python
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
```

### 2. Message Handler Pattern

```python
async def handle_message(self, task: Task) -> AsyncIterator[Message]:
    """Handle incoming messages and echo them back."""
    try:
        # Extract text from message
        text_content = self.extract_text_from_task(task)
        
        # Process and create response
        echo_text = f"Echo: {text_content}"
        response_artifact = new_text_artifact(
            name="echo_response",
            text=echo_text,
            description="Echoed message response"
        )
        
        # Yield response
        yield Message(
            artifacts=[response_artifact],
            parts=[]
        )
        
    except Exception as e:
        # Handle errors gracefully
        yield self.create_error_response(str(e))
```

### 3. Client Usage Pattern

```python
async def test_echo_agent():
    # Create client
    client_factory = ClientFactory()
    client = await client_factory.create_client("http://localhost:8000")
    
    # Send message
    message = Message(artifacts=[test_artifact])
    
    # Process responses
    async for response in client.send_message(message):
        print(f"Received: {response}")
    
    # Clean up
    await client.close()
```

## 🧪 Testing and Validation

### Manual Testing

```bash
# 1. Start agent
python agent.py

# 2. Test with curl
curl -X POST http://localhost:8000/message/send \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": {
      "parts": [{"text": "Hello World"}]
    }
  }'
```

### Programmatic Testing

```python
# Run the test client
python test_client.py

# Expected output:
# Sending message: Hello, A2A World!
# Received response: Echo: Hello, A2A World!
```

### Agent Card Validation

```bash
# Check if agent card is valid
curl -s http://localhost:8000/agent-card | python -m json.tool
```

## 🚀 Next Steps

Once you understand this example, try:

1. **Modify the echo logic** - Add timestamps, formatting, or transformations
2. **Add error handling** - Implement different error scenarios
3. **Extend with skills** - Add multiple capabilities
4. **Try different transports** - Experiment with gRPC or REST
5. **Add authentication** - Secure your agent
6. **Process files** - Handle binary artifacts

## 🔧 Customization Ideas

### Add Timestamp to Echo

```python
from datetime import datetime

echo_text = f"Echo [{datetime.now()}]: {text_content}"
```

### Add Message Counter

```python
class EchoAgent:
    def __init__(self):
        self.message_count = 0
        # ... rest of init
    
    async def handle_message(self, task: Task):
        self.message_count += 1
        echo_text = f"Echo #{self.message_count}: {text_content}"
        # ... rest of handler
```

### Add Message Validation

```python
def validate_message(self, text: str) -> bool:
    """Validate incoming message."""
    if len(text) > 1000:
        raise ValueError("Message too long")
    if not text.strip():
        raise ValueError("Empty message")
    return True
```

## 🐛 Troubleshooting

**Port already in use**
```bash
# Find process using port 8000
lsof -i :8000
# Kill the process if needed
kill -9 <PID>
```

**Import errors**
```bash
# Make sure you installed with http-server extra
pip install -e ".[http-server]"
```

**Agent not responding**
```bash
# Check if agent is running
curl http://localhost:8000/agent-card
# Check logs for errors in the terminal running agent.py
```

## 📚 Related Examples

- 📄 [File Processing Agent](../file-processor/) - Handle binary data
- 🎯 [Multi-Skill Agent](../multi-skill-agent/) - Multiple capabilities
- 🔐 [Authenticated Agent](../auth-agent/) - Add security

---

**Ready to echo your way into A2A development?** 🔊