#!/bin/bash
# Startup script for Insurance Notification Agent All-in-One FastAPI Server

echo "================================================================================"
echo "🚀 Starting Insurance Notification Agent - All-in-One FastAPI Server"
echo "================================================================================"
echo ""

# Set the port
export AGENT_SERVER_PORT=8086

# Navigate to the parent directory (hitl-adk) so Python can find the module
cd "$(dirname "$0")/.."

# Start the unified FastAPI server (includes both agent and approval API)
python -m insurance_notification.server
