#!/usr/bin/env python3
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

"""
FastAPI server for the Insurance Notification Agent.
Wraps the ADK agent in a FastAPI application for production deployment.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from pydantic import BaseModel
from typing import Literal
from google.cloud import logging as google_cloud_logging


# Load environment variables from .env file
load_dotenv()

logging_client = google_cloud_logging.Client()
logger = logging_client.logger(__name__)

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Get session service URI from environment variables
session_uri = os.getenv("SESSION_SERVICE_URI", None)

# Prepare arguments for get_fast_api_app
app_args = {"agents_dir": AGENT_DIR, "web": True, "trace_to_cloud": True}

# Only include session_service_uri if it's provided
if session_uri:
    app_args["session_service_uri"] = session_uri
else:
    logger.log_text(
        "SESSION_SERVICE_URI not provided. Using in-memory session service instead. "
        "All sessions will be lost when the server restarts.",
        severity="WARNING",
    )

# Create FastAPI app with appropriate arguments
app: FastAPI = get_fast_api_app(**app_args)

app.title = "insurance-notification-agent"
app.description = (
    "API for interacting with the Insurance Notification Agent. "
    "This agent provides email notifications, claim status tracking, "
    "policy management, and human-in-the-loop approval workflows."
)


class Feedback(BaseModel):
    """Represents feedback for a conversation."""

    score: int | float
    text: str | None = ""
    invocation_id: str
    log_type: Literal["feedback"] = "feedback"
    service_name: Literal["insurance-notification-agent"] = "insurance-notification-agent"
    user_id: str = ""


class ApprovalStatus(BaseModel):
    """Status of pending approvals."""

    ticket_id: str
    claim_id: str
    user_email: str
    status: str
    created_at: str


# Example custom endpoint for feedback
@app.post("/feedback")
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    """Collect and log feedback.

    Args:
        feedback: The feedback data to log

    Returns:
        Success message
    """
    logger.log_struct(feedback.model_dump(), severity="INFO")
    return {"status": "success"}


# Custom endpoint to check pending approvals
@app.get("/api/approvals/pending")
def get_pending_approvals() -> dict[str, list[ApprovalStatus]]:
    """Get all pending approval requests.

    Returns:
        List of pending approval requests
    """
    from .approval_manager import approval_manager

    pending = approval_manager.get_all_pending()
    return {
        "count": len(pending),
        "pending_approvals": [
            ApprovalStatus(
                ticket_id=req.ticket_id,
                claim_id=req.claim_id,
                user_email=req.user_email,
                status=req.status,
                created_at=req.created_at,
            )
            for req in pending
        ],
    }


# Health check endpoint
@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Service status
    """
    return {
        "status": "healthy",
        "service": "insurance-notification-agent",
        "version": "1.0.0",
    }


# Main execution
if __name__ == "__main__":
    import uvicorn

    # Get port from environment or use default
    port = int(os.getenv("AGENT_SERVER_PORT", "8080"))

    print("=" * 70)
    print("🚀 Starting Insurance Notification Agent - FastAPI Server")
    print("=" * 70)
    print(f"")
    print(f"Server running at: http://0.0.0.0:{port}")
    print(f"")
    print(f"Endpoints:")
    print(f"  - POST /run                       - Run the agent")
    print(f"  - GET  /apps                      - List available apps")
    print(f"  - GET  /health                    - Health check")
    print(f"  - POST /feedback                  - Submit feedback")
    print(f"  - GET  /api/approvals/pending     - Get pending approvals")
    print(f"")
    print(f"Note: Make sure the Approval API is running on port 8085")
    print("=" * 70)
    print()

    uvicorn.run(app, host="0.0.0.0", port=port)
