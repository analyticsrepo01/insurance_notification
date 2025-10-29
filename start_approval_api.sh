#!/bin/bash
# Startup script for Approval API Server

echo "="
echo "🚀 Starting Insurance Notification Approval API Server"
echo "="
echo ""

# Set the port
export APPROVAL_API_PORT=8085

# Navigate to the parent directory (hitl-adk) so Python can find the module
cd "$(dirname "$0")/.."

# Start the approval API server
python -m insurance_notification.approval_api
