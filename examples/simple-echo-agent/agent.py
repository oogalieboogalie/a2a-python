#!/usr/bin/env python3
"""
Simple Echo Agent - A basic A2A agent that echoes back messages.

This agent demonstrates the fundamental concepts of A2A development:
- Agent card configuration
- Request handler implementation
- HTTP JSON-RPC transport
- Message processing and responses

Usage:
    python agent.py

The agent will start on http://localhost:8000
"""

import asyncio
import logging
import uuid
from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Union

from a2a.server.apps import A2AFastAPIApplication
from a2a.server.context import ServerCallContext
from a2a.server.events.event_queue import Event
from a2a.server.request_handlers.request_handler import RequestHandler
from a2a.types import (
    AgentCard,
    AgentCapabilities, 
    AgentSkill,
    DeleteTaskPushNotificationConfigParams,
    GetTaskPushNotificationConfigParams,
    ListTaskPushNotificationConfigParams,
    Message,
    MessageSendParams,
    Part,
    Task,
    TaskIdParams,
    TaskPushNotificationConfig,
    TaskQueryParams,
    TextPart,
    TransportProtocol
)
from a2a.utils.artifact import new_text_artifact
from a2a.utils.errors import ServerError
from a2a.types import UnsupportedOperationError

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EchoRequestHandler(RequestHandler):
    """Request handler for the Echo Agent that implements the A2A protocol."""
    
    def __init__(self):
        self.message_count = 0
        self.tasks = {}  # Simple in-memory task storage
    
    async def on_get_task(
        self,
        params: TaskQueryParams,
        context: ServerCallContext | None = None,
    ) -> Task | None:
        """Get task by ID."""
        return self.tasks.get(params.task_id)
    
    async def on_cancel_task(
        self,
        params: TaskIdParams,
        context: ServerCallContext | None = None,
    ) -> bool:
        """Cancel a task."""
        if params.task_id in self.tasks:
            # Mark task as cancelled (simplified)
            return True
        return False
    
    async def on_message_send(
        self,
        params: MessageSendParams,
        context: ServerCallContext | None = None,
    ) -> Union[Task, Message]:
        """Handle non-streaming message send."""
        # For simplicity, we'll create a task and return a final message
        task_id = str(uuid.uuid4())
        
        # Process the message
        text_content = self._extract_text_content(params.message)
        response_message = await self._create_echo_response(text_content)
        
        # Store task
        task = Task(
            task_id=task_id,
            message=response_message
        )
        self.tasks[task_id] = task
        
        return response_message
    
    async def on_message_send_stream(
        self,
        params: MessageSendParams,
        context: ServerCallContext | None = None,
    ) -> AsyncGenerator[Event, None]:
        """Handle streaming message send."""
        # This is the main method for streaming responses
        task_id = str(uuid.uuid4())
        
        try:
            # Process the message
            text_content = self._extract_text_content(params.message)
            response_message = await self._create_echo_response(text_content)
            
            # Create and store task
            task = Task(
                task_id=task_id,
                message=response_message
            )
            self.tasks[task_id] = task
            
            # Yield task creation event (simplified - real implementation would use proper Event types)
            # For now, we'll just yield the message directly
            # In a real implementation, you'd yield proper Event objects
            logger.info(f"Streaming response for task {task_id}")
            
            # Since we don't have the exact Event types available, we'll simulate
            # by yielding a simple response. In practice, you'd import and use
            # the specific event types from a2a.server.events
            
        except Exception as e:
            logger.exception(f"Error in streaming handler: {e}")
            raise ServerError(error=UnsupportedOperationError())
        
        # This is a placeholder - real implementation needs proper Event types
        yield  # pragma: no cover
    
    async def on_set_task_push_notification_config(
        self,
        params: TaskPushNotificationConfig,
        context: ServerCallContext | None = None,
    ) -> TaskPushNotificationConfig:
        """Set task push notification config - not supported in this example."""
        raise ServerError(error=UnsupportedOperationError())
    
    async def on_get_task_push_notification_config(
        self,
        params: GetTaskPushNotificationConfigParams,
        context: ServerCallContext | None = None,
    ) -> TaskPushNotificationConfig | None:
        """Get task push notification config - not supported in this example."""
        raise ServerError(error=UnsupportedOperationError())
    
    async def on_list_task_push_notification_config(
        self,
        params: ListTaskPushNotificationConfigParams,
        context: ServerCallContext | None = None,
    ) -> list[TaskPushNotificationConfig]:
        """List task push notification configs - not supported in this example."""
        raise ServerError(error=UnsupportedOperationError())
    
    async def on_delete_task_push_notification_config(
        self,
        params: DeleteTaskPushNotificationConfigParams,
        context: ServerCallContext | None = None,
    ) -> bool:
        """Delete task push notification config - not supported in this example."""
        raise ServerError(error=UnsupportedOperationError())
    
    async def on_resubscribe_to_task(
        self,
        params: TaskIdParams,
        context: ServerCallContext | None = None,
    ) -> AsyncGenerator[Event, None]:
        """Resubscribe to task - not supported in this example."""
        raise ServerError(error=UnsupportedOperationError())
        yield  # pragma: no cover
    
    def _extract_text_content(self, message: Message) -> str:
        """Extract all text content from a message."""
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
        
        return ' '.join(text_parts) or "[empty message]"
    
    async def _create_echo_response(self, text_content: str) -> Message:
        """Create an echo response message."""
        self.message_count += 1
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        logger.info(f"Processing message #{self.message_count}: {text_content[:50]}...")
        
        # Create enhanced echo response
        echo_text = (
            f"Echo #{self.message_count} at {current_time}:\n"
            f"Received: {text_content}\n"
            f"Characters: {len(text_content)}"
        )
        
        # Create response artifact
        response_artifact = new_text_artifact(
            name=f"echo_response_{self.message_count}",
            text=echo_text,
            description="Enhanced echo response with metadata"
        )
        
        # Create response message
        response_message = Message(
            artifacts=[response_artifact],
            parts=[
                Part(root=TextPart(
                    text=echo_text,
                    metadata={
                        "message_count": self.message_count,
                        "timestamp": current_time,
                        "original_length": len(text_content)
                    }
                ))
            ]
        )
        
        logger.info(f"Created echo response #{self.message_count}")
        return response_message


class EchoAgent:
    """A simple echo agent that repeats back messages with enhancements."""
    
    def __init__(self):
        self.request_handler = EchoRequestHandler()
        self.app = self._create_app()
    
    def _create_app(self) -> A2AFastAPIApplication:
        """Create and configure the A2A FastAPI application."""
        # Define agent capabilities
        agent_card = AgentCard(
            name="Simple Echo Agent",
            description="A friendly agent that echoes back your messages with additional context",
            url="http://localhost:8000",
            version="1.0.0",
            capabilities=AgentCapabilities(
                streaming=True,
                push_notifications=False
            ),
            skills=[
                AgentSkill(
                    id="echo",
                    name="Echo Messages",
                    description="Echoes back input messages with timestamp and count",
                    inputModes=["text/plain"],
                    outputModes=["text/plain"],
                    tags=["echo", "communication", "test"]
                )
            ],
            default_input_modes=["text/plain"],
            default_output_modes=["text/plain"],
            preferred_transport=TransportProtocol.jsonrpc
        )
        
        # Create the FastAPI application with our request handler
        app = A2AFastAPIApplication(
            agent_card=agent_card,
            http_handler=self.request_handler
        )
        
        return app
    
    def get_fastapi_app(self):
        """Get the FastAPI application instance for running with uvicorn."""
        return self.app.build()


# Create the agent instance
echo_agent = EchoAgent()

# FastAPI app instance for uvicorn
app = echo_agent.get_fastapi_app()


async def main():
    """Run the agent server."""
    try:
        import uvicorn
        logger.info("🚀 Starting Echo Agent on http://localhost:8000")
        logger.info("📋 Agent card available at http://localhost:8000/.well-known/a2a")
        logger.info("🔄 Send messages to http://localhost:8000/a2a/v1")
        logger.info("💡 Use Ctrl+C to stop the server")
        
        uvicorn.run(
            "agent:app",  # Reference to the app variable
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")


if __name__ == "__main__":
    asyncio.run(main())