# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types
import agent

load_dotenv(override=True)

APP_NAME = "insurance_notification"
USER_ID = "customer_001"
SESSION_ID = "session_001"

session_service = InMemorySessionService()


async def main():
    """Demonstrate the insurance notification agent."""

    print("=" * 70)
    print("🏢 INSURANCE NOTIFICATION AGENT - DEMO")
    print("=" * 70)
    print()

    # Create session
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    # Create runner
    runner = Runner(
        agent=agent.root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    async def call_agent(query: str):
        """Helper function to call the agent and display results."""
        print(f"👤 Customer Query: {query}")
        print("-" * 70)

        content = types.Content(role="user", parts=[types.Part(text=query)])

        events_async = runner.run_async(
            session_id=session.id, user_id=USER_ID, new_message=content
        )

        async for event in events_async:
            if event.content and event.content.parts:
                for i, part in enumerate(event.content.parts):
                    if part.text:
                        print(f"🤖 Agent: {part.text.strip()}")
                    if part.function_call:
                        print(f"   🔧 Tool Call: {part.function_call.name}()")
                        print(f"      Args: {part.function_call.args}")
                    if part.function_response:
                        print(f"   ✅ Tool Response: {part.function_response.response}")

        print()

    # Demo Scenario 1: Check claim status and send notification
    print("\n📋 SCENARIO 1: Claim Status Update")
    print("=" * 70)
    await call_agent(
        "Please check the status of claim CLM-001 and send an email notification "
        "to analyticsrepo@gmail.com with the details."
    )

    # Demo Scenario 2: Policy renewal reminder
    print("\n📋 SCENARIO 2: Policy Renewal Reminder")
    print("=" * 70)
    await call_agent(
        "Check policy POL-67890 and send a renewal reminder email to "
        "analyticsrepo@gmail.com if renewal is coming up soon."
    )

    # Demo Scenario 3: General notification
    print("\n📋 SCENARIO 3: Custom Notification")
    print("=" * 70)
    await call_agent(
        "Send a general notification email to analyticsrepo@gmail.com "
        "about our new mobile app that allows customers to file claims easily."
    )

    # Demo Scenario 4: Pending claim check
    print("\n📋 SCENARIO 4: Pending Claim Status")
    print("=" * 70)
    await call_agent(
        "What's the status of claim CLM-002? Send the update to analyticsrepo@gmail.com"
    )

    print("=" * 70)
    print("✨ Demo completed!")
    print("=" * 70)


if __name__ == "__main__":
    # Check for required environment variable
    if not os.getenv("GOOGLE_CLOUD_PROJECT"):
        print("⚠️  Warning: GOOGLE_CLOUD_PROJECT environment variable not set.")
        print("   Setting a default value for demo purposes...")
        os.environ["GOOGLE_CLOUD_PROJECT"] = "demo-project"

    asyncio.run(main())
