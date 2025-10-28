# Insurance Notification Agent

An AI-powered insurance customer service agent built with Google's Agent Development Kit (ADK) that automatically sends email notifications to customers about claims, policy renewals, and other insurance matters.

## Features

🔔 **Email Notifications** - Send formatted HTML email notifications to customers
📋 **Claim Status Tracking** - Check and update customers on insurance claim status
📄 **Policy Management** - Monitor policy status and send renewal reminders
🤖 **AI-Powered** - Uses Gemini 2.0 Flash model for intelligent customer service
💼 **Professional Templates** - Beautiful HTML email templates for all notification types

## Notification Types

- **claim_update**: Claim status changes and approvals
- **policy_renewal**: Policy renewal reminders
- **payment_reminder**: Payment due notices
- **general**: General insurance communications

## Project Structure

```
insurance_notification_agent/
├── agent.py          # Agent configuration and setup
├── tools.py          # Email notification and data retrieval tools
├── main.py           # Demo script
├── README.md         # This file
└── .env.example      # Environment variables template
```

## Prerequisites

1. **Python 3.9+**
2. **Google Cloud Project** with Vertex AI API enabled
3. **Gmail Account** (optional - for sending real emails)
4. **ADK Python SDK** installed

## Setup Instructions

### 1. Install Dependencies

```bash
pip install google-adk python-dotenv
```

### 2. Configure Environment Variables

Create a `.env` file in the `insurance_notification_agent` directory:

```bash
# Required for ADK
GOOGLE_CLOUD_PROJECT=your-project-id

# Optional - For sending real emails (leave empty for demo mode)
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-specific-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**Note:** If you leave `SENDER_PASSWORD` empty, the agent will run in **demo mode** and print email notifications to the console instead of sending real emails.

### 3. Set Up Gmail App Password (Optional)

To send real emails via Gmail:

1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Generate an App Password: https://myaccount.google.com/apppasswords
4. Use the generated password in your `.env` file

### 4. Authenticate with Google Cloud

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

## Usage

### Running the Demo

```bash
cd insurance_notification_agent
python main.py
```

This will run four demo scenarios:
1. Claim status update email
2. Policy renewal reminder
3. General notification about new mobile app
4. Pending claim status update

### Running with ADK Web Interface

```bash
# From the parent directory
adk web .
```

Then navigate to the insurance notification agent in the web UI.

### Example Interactions

**Claim Status Update:**
```
User: "Check claim CLM-001 and send an email to analyticsrepo@gmail.com"

Agent:
- Retrieves claim details
- Sends formatted email with claim status
- Confirms notification sent
```

**Policy Renewal Reminder:**
```
User: "Check policy POL-67890 and send renewal reminder to analyticsrepo@gmail.com"

Agent:
- Checks policy status
- Detects upcoming renewal (4 days)
- Sends urgent renewal reminder email
```

**Custom Notification:**
```
User: "Send an email to analyticsrepo@gmail.com about our customer satisfaction survey"

Agent:
- Composes professional email
- Uses general notification template
- Sends email with survey information
```

## Tools Available

### 1. `send_email_notification()`
Sends HTML-formatted email notifications to customers.

**Parameters:**
- `recipient_email` (str): Email address of recipient
- `subject` (str): Email subject line
- `message` (str): Email body content
- `notification_type` (str): Type of notification (claim_update, policy_renewal, payment_reminder, general)

**Returns:**
- Status, recipient, subject, and send confirmation

### 2. `get_claim_status()`
Retrieves current status of an insurance claim.

**Parameters:**
- `claim_id` (str): Claim ID to look up

**Returns:**
- Claim details including status, amounts, and dates

**Demo Claims:**
- `CLM-001`: Approved auto accident claim ($4,500 approved)
- `CLM-002`: Pending property damage claim ($12,000 claimed)

### 3. `check_policy_status()`
Checks status of an insurance policy.

**Parameters:**
- `policy_number` (str): Policy number to look up

**Returns:**
- Policy details including status, premium, coverage, and renewal date

**Demo Policies:**
- `POL-12345`: Active auto insurance policy (65 days until renewal)
- `POL-67890`: Home insurance pending renewal (4 days until renewal)

## Demo Mode vs. Production Mode

### Demo Mode (Default)
When `SENDER_PASSWORD` is not set, emails are **printed to console** instead of sent:

```
📧 EMAIL NOTIFICATION (Demo Mode - Not Actually Sent)
To: analyticsrepo@gmail.com
Subject: Claim Status Update - CLM-001
Type: claim_update
Message: Your claim has been approved...
```

### Production Mode
When SMTP credentials are configured, real emails are sent via Gmail:

```
✅ Email notification sent successfully
Recipient: analyticsrepo@gmail.com
Subject: Claim Status Update
Status: Delivered
```

## Email Template

All emails use a professional HTML template with:
- Insurance company branding header
- Notification type badge
- Formatted message content
- Automated disclaimer footer

Example email structure:
```
┌─────────────────────────────────┐
│   Insurance Notification        │  ← Header
├─────────────────────────────────┤
│ Notification Type: Claim Update │  ← Type
│ ──────────────────────────────  │
│                                 │
│ [Your message content here]     │  ← Message
│                                 │
│ ──────────────────────────────  │
│ Automated notification...       │  ← Footer
└─────────────────────────────────┘
```

## Customization

### Adding New Notification Types

Edit `tools.py` to add custom notification types in the email template.

### Adding More Claims/Policies

Edit the simulated databases in `tools.py`:
- `claims` dictionary in `get_claim_status()`
- `policies` dictionary in `check_policy_status()`

### Changing Email Recipient

The default recipient is `analyticsrepo@gmail.com`. To change:
- Modify the agent instruction in `agent.py`, or
- Specify a different email in your query

### Customizing Agent Behavior

Edit the `instruction` field in `agent.py` to change how the agent handles different scenarios.

## Troubleshooting

**Email Not Sending:**
- Check `SENDER_EMAIL` and `SENDER_PASSWORD` in `.env`
- Verify Gmail App Password is correct
- Ensure "Less secure app access" is enabled (if not using App Password)
- Check SMTP server and port settings

**Agent Not Responding:**
- Verify `GOOGLE_CLOUD_PROJECT` is set correctly
- Ensure you've authenticated with `gcloud auth application-default login`
- Check that Vertex AI API is enabled in your project

**Import Errors:**
- Make sure you're running from the correct directory
- Install missing dependencies: `pip install google-adk python-dotenv`

## Extending the Agent

You can extend this agent by:

1. **Integrating with Real Databases**: Replace simulated data with actual database queries
2. **Adding More Tools**: Create tools for premium calculations, policy modifications, etc.
3. **Multi-Channel Notifications**: Add SMS, push notifications, or webhooks
4. **Advanced Workflows**: Implement approval workflows for claim processing
5. **Customer Authentication**: Add user verification before sharing sensitive information
6. **Scheduled Reminders**: Set up automated renewal reminders using cron jobs

## Security Considerations

⚠️ **Important Security Notes:**

- Never commit `.env` file with real credentials to version control
- Use Google Cloud Secret Manager for production credentials
- Implement rate limiting to prevent email spam
- Validate recipient email addresses before sending
- Add authentication for customer data access
- Use encryption for sensitive claim/policy information

## License

Copyright 2025 Google LLC

Licensed under the Apache License, Version 2.0

## Support

For issues or questions:
- Check the ADK documentation: https://google.github.io/adk-python/
- Review ADK samples: https://github.com/google/adk-python/tree/main/samples
- File an issue in your project repository

## Example Output

```bash
$ python main.py

======================================================================
🏢 INSURANCE NOTIFICATION AGENT - DEMO
======================================================================

📋 SCENARIO 1: Claim Status Update
======================================================================
👤 Customer Query: Please check the status of claim CLM-001...
----------------------------------------------------------------------
🤖 Agent: I'll check the claim status and send a notification.
   🔧 Tool Call: get_claim_status()
   ✅ Tool Response: {'status': 'found', 'claim': {...}}
   🔧 Tool Call: send_email_notification()
   ✅ Tool Response: {'status': 'success', 'demo_mode': True}
🤖 Agent: I've sent the claim update email to analyticsrepo@gmail.com

📧 EMAIL NOTIFICATION (Demo Mode - Not Actually Sent)
To: analyticsrepo@gmail.com
Subject: Claim CLM-001 - Approved
Type: claim_update
Message: Good news! Your auto accident claim has been approved...
============================================================
```

---

Built with ❤️ using Google Agent Development Kit (ADK)
