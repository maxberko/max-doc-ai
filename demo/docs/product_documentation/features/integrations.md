# Integrations

## Overview

Connect FlowState to 100+ tools your team already uses. Integrations enable workflows to interact with external services, sync data between tools, and automate cross-platform tasks.

Access integrations at: `https://app.flowstate.example.com/integrations`

## Key Capabilities

- **100+ Pre-Built Integrations**: Connect to popular tools without custom code
- **OAuth Authentication**: Secure, easy authorization flows
- **Real-Time Sync**: Bi-directional data synchronization
- **Custom Webhooks**: Integrate with any API-enabled service
- **Connection Management**: Centralized control over all integrations
- **Team Sharing**: Share connections across your workspace

## Available Integrations

### Communication & Collaboration

**Slack**: Send messages, create channels, manage users
- Triggers: New message, reaction added, user joined
- Actions: Send message, update message, create channel

**Microsoft Teams**: Post messages, manage teams
- Triggers: New message in channel
- Actions: Send message, create team, add member

**Gmail**: Send emails, manage labels, search inbox
- Triggers: New email received, label added
- Actions: Send email, create draft, add label

### Developer Tools

**GitHub**: Manage repositories, issues, pull requests
- Triggers: Push event, new issue, PR opened/merged
- Actions: Create issue, comment, merge PR, create release

**GitLab**: CI/CD pipelines, merge requests, issues
- Triggers: Pipeline status, MR events, issue updates
- Actions: Create issue, trigger pipeline, add comment

**Jira**: Issues, projects, sprints
- Triggers: Issue created/updated, sprint started
- Actions: Create/update issue, add comment, transition status

### Project Management

**Asana**: Tasks, projects, teams
- Triggers: Task completed, project created
- Actions: Create task, update project, assign task

**Linear**: Issues, cycles, projects
- Triggers: Issue created, status changed
- Actions: Create issue, update status, add comment

**Trello**: Boards, lists, cards
- Triggers: Card created, moved, due date approaching
- Actions: Create card, move card, add member

### Data & Storage

**Google Sheets**: Spreadsheets, data management
- Triggers: New row added, cell updated
- Actions: Add row, update cell, create sheet

**Airtable**: Databases, views, records
- Triggers: New record, record updated
- Actions: Create record, update record, search

**Dropbox**: File storage and sharing
- Triggers: New file, folder created
- Actions: Upload file, create folder, share link

### CRM & Sales

**Salesforce**: Leads, opportunities, accounts
- Triggers: New lead, opportunity stage changed
- Actions: Create lead, update account, log activity

**HubSpot**: Contacts, deals, companies
- Triggers: Contact created, deal stage changed
- Actions: Create contact, update deal, send email

**Stripe**: Payments, customers, subscriptions
- Triggers: Payment succeeded, subscription created
- Actions: Create customer, send invoice

## How It Works

### Connecting an Integration

![Integration marketplace](https://placeholder-cloudfront-url.com/integrations-marketplace.png)

1. Navigate to "Integrations" in the main menu
2. Browse or search for the service you want to connect
3. Click "Connect"
4. Authorize FlowState to access your account (OAuth)
5. Configure connection settings (optional)
6. Click "Save Connection"

### Managing Connections

![Connected integrations](https://placeholder-cloudfront-url.com/integrations-connected.png)

View all your connected services:

**Connection details:**
- Service name and account
- Connection status (active, expired, error)
- Last used date
- Permissions granted
- Number of workflows using this connection

**Actions:**
- **Reconnect**: Refresh OAuth token if expired
- **Edit**: Update connection settings
- **Test**: Verify connection is working
- **Delete**: Remove connection (prompts to update workflows)

### Using Integrations in Workflows

Once connected, use integrations in workflow triggers and actions:

1. Create or edit a workflow
2. Add a trigger or action
3. Select the integrated service
4. Choose the specific event or action
5. Configure using data from your connected account

**Example:**
```
Trigger: GitHub - New Issue Created
  Repository: my-company/my-repo
  Labels: bug, urgent

Action: Slack - Send Message
  Channel: #engineering
  Message: "New urgent bug: {{trigger.issue.title}}"
```

### Scopes and Permissions

Each integration requests specific permissions:

**Read permissions:**
- View data (issues, messages, files)
- List resources (repositories, channels, users)
- Search and query

**Write permissions:**
- Create new resources
- Update existing data
- Delete items (if applicable)

**Review permissions** before connecting. You can revoke access anytime.

### Sharing Connections

Share integrations with your team:

![Share integration](https://placeholder-cloudfront-url.com/integrations-share.png)

1. Open a connected integration
2. Click "Share with Team"
3. Select team members or groups
4. Set permission level:
   - **Use Only**: Can use in workflows
   - **Manage**: Can edit and reconnect
5. Click "Share"

**Benefits:**
- Team members don't need individual accounts
- Centralized connection management
- Consistent authentication across workflows

## Configuration

### Connection Settings

| Setting | Description | Example |
|---------|-------------|---------|
| Display Name | Custom name for this connection | "Production Slack" |
| Account | Connected account identifier | team@company.com |
| Scopes | Granted permissions | read:issues, write:comments |
| Auto-reconnect | Automatically refresh tokens | Enabled |
| Notifications | Alert on connection issues | Email |

### Rate Limiting

Respect API limits of integrated services:

- FlowState tracks usage automatically
- Workflows pause if limit reached
- Alerts when approaching limit
- Rate limit info shown in integration details

**Common limits:**
- Slack: 1 message/second
- GitHub: 5,000 requests/hour
- Google Sheets: 100 requests/100 seconds

### Custom Webhooks

![Webhook configuration](https://placeholder-cloudfront-url.com/integrations-webhook.png)

Connect to any API-enabled service:

1. Go to Integrations > Custom Webhook
2. Click "Create Webhook"
3. FlowState generates a unique webhook URL
4. Configure the external service to send data to this URL
5. Use the webhook as a trigger in workflows

**Example use cases:**
- Form submissions from your website
- Alerts from monitoring tools
- Events from custom applications
- Third-party service notifications

## Use Cases

### Use Case 1: DevOps Incident Management

**Integrations**: PagerDuty, Slack, Jira, GitHub

**Workflow:**
1. PagerDuty alert triggers workflow
2. Create Jira P0 ticket
3. Post to #incidents Slack channel
4. Create GitHub issue for tracking
5. Notify on-call engineer

### Use Case 2: Sales Pipeline Automation

**Integrations**: HubSpot, Slack, Google Sheets, Gmail

**Workflow:**
1. New deal created in HubSpot triggers workflow
2. Add deal to sales tracking sheet
3. Notify sales channel in Slack
4. Send personalized follow-up email
5. Schedule reminders for check-ins

### Use Case 3: Content Publishing

**Integrations**: Google Docs, WordPress, Twitter, Slack

**Workflow:**
1. New document in Google Drive triggers workflow
2. Convert to WordPress post
3. Publish to blog
4. Share on Twitter
5. Notify team in Slack

## Troubleshooting

### Connection Issues

**Problem**: "Connection expired" error

**Solution:**
1. Go to Integrations page
2. Click "Reconnect" next to the integration
3. Re-authorize with the service
4. Test the connection

**Problem**: "Permission denied" error

**Solution:**
- Check if you granted necessary scopes during connection
- Reconnect and ensure all required permissions are selected
- Verify your account has access to the resource (repository, channel, etc.)

### API Rate Limits

**Problem**: Workflow paused due to rate limit

**Solution:**
- Wait for rate limit window to reset (shown in error message)
- Reduce workflow execution frequency
- Batch operations when possible
- Contact support for higher limits

### Data Sync Issues

**Problem**: Outdated data in workflows

**Solution:**
- Check integration's cache settings
- Force a connection refresh
- Verify the external service is responding
- Review workflow trigger configuration

## Best Practices

1. **Use descriptive connection names**: Especially if you have multiple accounts
2. **Review permissions regularly**: Remove unnecessary scopes
3. **Monitor connection health**: Check status periodically
4. **Share connections strategically**: Only share with team members who need them
5. **Set up fallbacks**: Handle connection failures gracefully in workflows
6. **Keep tokens secure**: Never share OAuth tokens or expose in logs
7. **Test after reconnecting**: Verify workflows still work after token refresh
8. **Document custom webhooks**: Keep track of webhook URLs and what they're for
9. **Respect rate limits**: Build workflows that stay within API limits
10. **Use official integrations**: Pre-built integrations are more reliable than custom webhooks

## FAQ

**Q: How many integrations can I connect?**

A: Unlimited integrations on all plans.

**Q: Are my credentials secure?**

A: Yes, FlowState uses OAuth tokens (not passwords) and encrypts all credentials at rest and in transit.

**Q: What happens if an integration disconnects?**

A: Workflows using that integration will pause and you'll receive an alert. Reconnect to resume.

**Q: Can I use personal accounts for team integrations?**

A: Yes, but we recommend using service accounts or team-owned accounts for better continuity.

**Q: Do integrations cost extra?**

A: No, all integrations are included in your FlowState plan. However, the external services may have their own pricing.

**Q: How do I request a new integration?**

A: Submit a request at https://flowstate.example.com/integrations/request or contact support.

## Need Help?

If you have questions or need assistance:
- Visit our [Help Center](https://docs.flowstate.example.com)
- Browse [Integration Guides](https://docs.flowstate.example.com/integrations)
- Contact support: support@flowstate.example.com
- Live chat: Available in-app (bottom right corner)
