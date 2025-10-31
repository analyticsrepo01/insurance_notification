#!/bin/bash
# Startup script for Insurance Notification Agent FastAPI Server

echo "========================================================================"
echo "🚀 Starting Insurance Notification Agent - FastAPI Server"
echo "========================================================================"
echo ""

# Set the port
export AGENT_SERVER_PORT=8080

# Navigate to the parent directory (hitl-adk) so Python can find the module
cd "$(dirname "$0")/.."

# Start the FastAPI agent server
python -m insurance_notification.server
