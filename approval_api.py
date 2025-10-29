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
FastAPI server for handling approval/rejection callbacks.
This server provides endpoints that are called when users click approve/reject buttons in emails.
Automatically pushes FunctionResponse back to ADK to resume agent execution.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
import httpx
import os
from dotenv import load_dotenv
from .approval_manager import approval_manager

# Load environment variables
load_dotenv()

app = FastAPI(title="Insurance Notification Approval API")


async def push_response_to_adk(approval_request: dict, approval_status: str):
    """
    Push the FunctionResponse back to ADK to resume agent execution.

    Args:
        approval_request: The approval request data
        approval_status: "approved" or "rejected"
    """
    try:
        session_info = approval_request.get("metadata", {}).get("session_info", {})
        function_call_id = approval_request.get("function_call_id")

        if not function_call_id or not session_info:
            print(f"⚠️  Missing session info, cannot resume agent automatically")
            return False

        # Get ADK API server URL (usually port 8000)
        adk_api_url = os.getenv("ADK_API_URL", "http://localhost:8000")

        # Prepare the function response
        function_response = {
            "status": "success",
            "approval_status": approval_status,
            "ticket_id": approval_request.get("ticket_id"),
            "claim_id": approval_request.get("claim_id"),
            "message": f"Claim verification {approval_status} by user"
        }

        # Push the response to ADK to resume the agent
        # Note: adk api_server uses /run endpoint
        push_url = f"{adk_api_url}/run"
        payload = {
            "app_name": session_info.get("app_name"),
            "user_id": session_info.get("user_id"),
            "session_id": session_info.get("session_id"),
            "new_message": {
                "role": "function",
                "parts": [{
                    "function_response": {
                        "name": "request_claim_approval",
                        "id": function_call_id,
                        "response": function_response
                    }
                }]
            }
        }

        print(f"📤 Pushing FunctionResponse to ADK: {push_url}")
        print(f"   Session: {session_info.get('user_id')}/{session_info.get('session_id')}")
        print(f"   Function Call ID: {function_call_id}")
        print(f"   Status: {approval_status}")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(push_url, json=payload)

            if response.status_code == 200:
                print(f"✅ Successfully resumed agent with approval status: {approval_status}")
                return True
            else:
                print(f"❌ Failed to resume agent: {response.status_code} - {response.text}")
                return False

    except Exception as e:
        print(f"❌ Error pushing response to ADK: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "Insurance Notification Approval API",
        "status": "running",
        "endpoints": {
            "approve": "/api/approve/{ticket_id}",
            "reject": "/api/reject/{ticket_id}",
            "status": "/api/status/{ticket_id}"
        }
    }


@app.get("/api/approve/{ticket_id}")
async def approve_request(ticket_id: str):
    """
    Approve an approval request.
    This endpoint is called when a user clicks the APPROVE button in their email.
    Automatically pushes the response back to ADK to resume the agent.
    """
    # Get the approval request before updating it
    approval_request = approval_manager.get_approval(ticket_id)
    if not approval_request:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")

    # Convert to dict for easier handling
    from dataclasses import asdict
    approval_dict = asdict(approval_request)

    # Update approval status
    result = approval_manager.approve(ticket_id, approver_notes="Approved via email link")

    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])

    # Push the response back to ADK to resume the agent
    await push_response_to_adk(approval_dict, "approved")

    # Return a nice HTML response
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Claim Approved</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                text-align: center;
            }}
            .success {{
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .checkmark {{
                font-size: 48px;
                color: #28a745;
            }}
            .details {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <div class="checkmark">✓</div>
        <div class="success">
            <h2>Claim Approved Successfully</h2>
            <p>Thank you for verifying your claim submission.</p>
        </div>
        <div class="details">
            <p><strong>Ticket ID:</strong> {ticket_id}</p>
            <p><strong>Claim ID:</strong> {result.get('claim_id', 'N/A')}</p>
            <p><strong>Status:</strong> Approved</p>
            <p><strong>Next Steps:</strong> You will receive a confirmation email shortly with the claim processing details.</p>
        </div>
        <p style="color: #666; margin-top: 30px;">
            You may now close this window.
        </p>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)


@app.get("/api/reject/{ticket_id}")
async def reject_request(ticket_id: str):
    """
    Reject an approval request.
    This endpoint is called when a user clicks the REJECT button in their email.
    Automatically pushes the response back to ADK to resume the agent.
    """
    # Get the approval request before updating it
    approval_request = approval_manager.get_approval(ticket_id)
    if not approval_request:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")

    # Convert to dict for easier handling
    from dataclasses import asdict
    approval_dict = asdict(approval_request)

    # Update approval status
    result = approval_manager.reject(ticket_id, rejection_reason="Rejected via email link")

    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])

    # Push the response back to ADK to resume the agent
    await push_response_to_adk(approval_dict, "rejected")

    # Return a nice HTML response
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Claim Rejected</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                text-align: center;
            }}
            .warning {{
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                color: #721c24;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .xmark {{
                font-size: 48px;
                color: #dc3545;
            }}
            .details {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <div class="xmark">✗</div>
        <div class="warning">
            <h2>Claim Submission Rejected</h2>
            <p>You have indicated that you did not submit this claim.</p>
        </div>
        <div class="details">
            <p><strong>Ticket ID:</strong> {ticket_id}</p>
            <p><strong>Claim ID:</strong> {result.get('claim_id', 'N/A')}</p>
            <p><strong>Status:</strong> Rejected</p>
            <p><strong>Next Steps:</strong> Our security team will investigate this matter. You will receive a follow-up email within 24 hours.</p>
        </div>
        <p style="color: #666; margin-top: 30px;">
            If you have any concerns, please contact our customer service immediately.
        </p>
        <p style="color: #666;">
            You may now close this window.
        </p>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)


@app.get("/api/status/{ticket_id}")
async def get_status(ticket_id: str):
    """
    Get the status of an approval request.
    """
    request = approval_manager.get_approval(ticket_id)

    if not request:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")

    return {
        "ticket_id": request.ticket_id,
        "claim_id": request.claim_id,
        "status": request.status,
        "request_type": request.request_type,
        "created_at": request.created_at,
        "updated_at": request.updated_at
    }


@app.get("/api/pending")
async def get_pending_approvals():
    """
    Get all pending approval requests.
    """
    pending = approval_manager.get_all_pending()
    return {
        "count": len(pending),
        "pending_approvals": [
            {
                "ticket_id": req.ticket_id,
                "claim_id": req.claim_id,
                "user_email": req.user_email,
                "request_type": req.request_type,
                "created_at": req.created_at
            }
            for req in pending
        ]
    }


if __name__ == "__main__":
    import os

    # Get port from environment or use default
    port = int(os.getenv("APPROVAL_API_PORT", "8085"))

    print("=" * 70)
    print("🚀 Starting Insurance Notification Approval API")
    print("=" * 70)
    print(f"")
    print(f"Server running at: http://0.0.0.0:{port}")
    print(f"")
    print(f"Endpoints:")
    print(f"  - GET  /api/approve/{{ticket_id}}  - Approve a request")
    print(f"  - GET  /api/reject/{{ticket_id}}   - Reject a request")
    print(f"  - GET  /api/status/{{ticket_id}}   - Get request status")
    print(f"  - GET  /api/pending               - List pending requests")
    print("=" * 70)
    print()

    uvicorn.run(app, host="0.0.0.0", port=port)
