#!/bin/bash
# Startup script for Approval API Server
#
# IMPORTANT: Run this from the hitl-adk/ directory (parent directory):
#   cd /path/to/hitl-adk
#   bash insurance_notification/start_approval_api.sh
#
# NOTE: This script is DEPRECATED. Use the all-in-one server instead:
#   bash insurance_notification/start_agent_server.sh
#
# The all-in-one server includes both agent and approval endpoints on port 8086.

echo "========================================================================"
echo "🚀 Starting Insurance Notification Approval API Server"
echo "========================================================================"
echo ""
echo "⚠️  DEPRECATION WARNING:"
echo "   This standalone approval API is deprecated."
echo "   Please use the all-in-one server instead:"
echo "   bash insurance_notification/start_agent_server.sh"
echo ""
echo "   Continuing with standalone approval API on port 8085..."
echo ""

# Check if we're in the correct directory
if [ ! -d "insurance_notification" ]; then
    echo "❌ Error: Must run from hitl-adk/ directory (parent directory)"
    echo ""
    echo "Current directory: $(pwd)"
    echo ""
    echo "Please run:"
    echo "  cd /path/to/hitl-adk"
    echo "  bash insurance_notification/start_approval_api.sh"
    echo ""
    exit 1
fi

echo "✅ Working directory: $(pwd)"
echo ""

# Set the port
export APPROVAL_API_PORT=8085

# Start the approval API server
python -m insurance_notification.approval_api
