#!/usr/bin/env python3
"""Simple test script to send one test email notification."""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from insurance_notification.agent import send_email_notification

load_dotenv()

async def send_test_email():
    """Send a single test email to verify configuration."""

    print("=" * 70)
    print("📧 INSURANCE NOTIFICATION AGENT - EMAIL TEST")
    print("=" * 70)
    print()
    print("Sending test email...")
    print(f"From: {os.getenv('SENDER_EMAIL')}")
    print(f"To: analyticsrepo@gmail.com")
    print()

    result = send_email_notification(
        recipient_email="analyticsrepo@gmail.com",
        subject="Test - Insurance Notification System",
        message="""
        <h3>Hello from your Insurance Notification Agent!</h3>

        <p>This is a test email to verify that your insurance notification system is working correctly.</p>

        <p><strong>System Details:</strong></p>
        <ul>
            <li>Agent: Insurance Notification Agent</li>
            <li>Model: Gemini 2.5 Flash</li>
            <li>Email Service: SMTP (Gmail)</li>
            <li>Status: Operational ✓</li>
        </ul>

        <p>If you received this email, your notification system is configured correctly and ready to send:</p>
        <ul>
            <li>Claim status updates</li>
            <li>Policy renewal reminders</li>
            <li>Payment reminders</li>
            <li>General insurance communications</li>
        </ul>

        <p>Thank you for testing!</p>
        """,
        notification_type="general"
    )

    print("-" * 70)
    print("📬 Result:")
    print(f"   Status: {result['status']}")
    print(f"   Recipient: {result['recipient']}")
    print(f"   Subject: {result['subject']}")
    if result.get('demo_mode'):
        print(f"   Mode: DEMO (email printed above, not actually sent)")
    else:
        print(f"   Mode: PRODUCTION (email sent via SMTP)")

    if result['status'] == 'success':
        print()
        print("✅ Test email sent successfully!")
        if not result.get('demo_mode'):
            print("   Check your inbox at analyticsrepo@gmail.com")
    else:
        print()
        print(f"❌ Error: {result.get('message')}")
        if result.get('error'):
            print(f"   Details: {result['error']}")

    print("=" * 70)

    return result

if __name__ == "__main__":
    asyncio.run(send_test_email())
