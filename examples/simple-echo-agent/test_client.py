#!/usr/bin/env python3
"""
Test client for the Simple Echo Agent.

This script demonstrates how to interact with an A2A agent programmatically.
It sends test messages and displays the responses.

Usage:
    python test_client.py

Make sure the echo agent is running on http://localhost:8000 first.
"""

import asyncio
import logging
from a2a.client import ClientFactory
from a2a.utils.artifact import new_text_artifact
from a2a.types import Message, Part, TextPart

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_echo_agent():
    """Test the echo agent with various messages."""
    try:
        # Create client factory and connect to agent
        logger.info("🔗 Connecting to Echo Agent at http://localhost:8000")
        client_factory = ClientFactory()
        client = await client_factory.create_client("http://localhost:8000")
        
        # Get agent card to verify connection
        logger.info("📋 Getting agent card...")
        agent_card = await client.get_agent_card()
        logger.info(f"✅ Connected to: {agent_card.name} v{agent_card.version}")
        logger.info(f"📝 Description: {agent_card.description}")
        
        # Test messages
        test_cases = [
            "Hello, A2A World!",
            "This is a longer message to test how the echo agent handles different text lengths and content.",
            "🚀 Testing with emojis and special characters! 🎉",
            "",  # Empty message test
            "Multiple\nLine\nMessage\nTest"
        ]
        
        for i, test_text in enumerate(test_cases, 1):
            logger.info(f"\n📤 Test {i}: Sending message")
            logger.info(f"   Content: {repr(test_text)}")
            
            # Create test message with both artifact and parts (showing different ways)
            if i % 2 == 0:
                # Use artifact approach
                test_artifact = new_text_artifact(
                    name=f"test_message_{i}",
                    text=test_text,
                    description=f"Test message #{i}"
                )
                message = Message(
                    artifacts=[test_artifact],
                    parts=[]
                )
                logger.info("   Method: Using artifact")
            else:
                # Use parts approach
                message = Message(
                    artifacts=[],
                    parts=[Part(root=TextPart(text=test_text))]
                )
                logger.info("   Method: Using text parts")
            
            # Send message and collect responses
            logger.info("📥 Receiving responses...")
            response_count = 0
            
            try:
                async for response in client.send_message(message):
                    response_count += 1
                    logger.info(f"   Response {response_count}: {type(response).__name__}")
                    
                    # Extract and display response text
                    response_text = extract_text_from_message(response)
                    logger.info(f"   Content: {response_text}")
                    
                    # Show metadata if available
                    if response.parts:
                        for part in response.parts:
                            if hasattr(part.root, 'metadata') and part.root.metadata:
                                logger.info(f"   Metadata: {part.root.metadata}")
                
                logger.info(f"✅ Test {i} completed with {response_count} response(s)")
                
            except Exception as e:
                logger.error(f"❌ Test {i} failed: {e}")
            
            # Add delay between tests
            await asyncio.sleep(0.5)
        
        # Clean up
        logger.info("\n🧹 Cleaning up...")
        await client.close()
        logger.info("✅ All tests completed successfully!")
        
    except Exception as e:
        logger.exception(f"❌ Test failed with error: {e}")
        logger.info("\n💡 Troubleshooting tips:")
        logger.info("   1. Make sure the echo agent is running: python agent.py")
        logger.info("   2. Check if port 8000 is accessible")
        logger.info("   3. Verify the agent card is available: curl http://localhost:8000/.well-known/a2a")


def extract_text_from_message(message: Message) -> str:
    """Extract all text content from a message for display."""
    text_parts = []
    
    # Extract from message parts
    if message.parts:
        for part in message.parts:
            if hasattr(part.root, 'text'):
                text_parts.append(part.root.text)
    
    # Extract from artifacts
    if message.artifacts:
        for artifact in message.artifacts:
            for part in artifact.parts:
                if hasattr(part.root, 'text'):
                    text_parts.append(part.root.text)
    
    return '\n'.join(text_parts) if text_parts else "[No text content]"


async def quick_test():
    """Quick single-message test for debugging."""
    try:
        logger.info("🔗 Quick test: Connecting to Echo Agent...")
        client_factory = ClientFactory()
        client = await client_factory.create_client("http://localhost:8000")
        
        # Simple message
        message = Message(
            parts=[Part(root=TextPart(text="Quick test message"))],
            artifacts=[]
        )
        
        logger.info("📤 Sending quick test message...")
        async for response in client.send_message(message):
            logger.info(f"📥 Response: {extract_text_from_message(response)}")
        
        await client.close()
        logger.info("✅ Quick test completed!")
        
    except Exception as e:
        logger.error(f"❌ Quick test failed: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        print("Running quick test...")
        asyncio.run(quick_test())
    else:
        print("Running full test suite...")
        print("Use --quick flag for a simple single-message test")
        asyncio.run(test_echo_agent())