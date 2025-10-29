  How It Works Now:

  1. Agent calls request_claim_approval()
     ↓
  2. Agent pauses, returns pending status
     ↓
  3. Email sent to user with approve/reject buttons
     ↓
  4. User clicks button → hits approval API
     ↓
  5. Approval API:
     - Updates approval status in /tmp/approval_requests.json
     - Pushes FunctionResponse to ADK API server
     ↓
  6. ADK receives FunctionResponse
     ↓
  7. Agent automatically resumes with approval result
     ↓
  8. Agent can then send final confirmation email