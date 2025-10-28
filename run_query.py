#!/usr/bin/env python3
"""Run a single query against the insurance notification agent."""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types
from insurance_notification_agent import root_agent

load_dotenv(override=True)

APP_NAME = "insurance_notification"
USER_ID = "customer_001"
SESSION_ID = "test_session"

session_service = InMemorySessionService()


async def run_query(query: str):
    """Run a single query against the agent."""

    print("=" * 70)
    print("🏢 INSURANCE NOTIFICATION AGENT")
    print("=" * 70)
    print()

    # Create session
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    # Create runner
    runner = Runner(
        agent=root_agent.root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print(f"👤 Query: {query}")
    print("-" * 70)
    print()

    content = types.Content(role="user", parts=[types.Part(text=query)])

    events_async = runner.run_async(
        session_id=session.id, user_id=USER_ID, new_message=content
    )

    async for event in events_async:
        if event.content and event.content.parts:
            for i, part in enumerate(event.content.parts):
                if part.text:
                    print(f"🤖 Agent Response:")
                    print(f"   {part.text.strip()}")
                    print()
                if part.function_call:
                    print(f"🔧 Tool Called: {part.function_call.name}")
                    print(f"   Arguments: {dict(part.function_call.args)}")
                    print()
                if part.function_response:
                    print(f"✅ Tool Result:")
                    for key, value in part.function_response.response.items():
                        print(f"   {key}: {value}")
                    print()

    print("=" * 70)
    print("✨ Query completed!")
    print("=" * 70)


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Check claim CLM-001 and send status update email to analyticsrepo@gmail.com"
    asyncio.run(run_query(query))
