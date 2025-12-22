# Workflow Builder

## Overview

The Workflow Builder gives you a visual, no-code interface for creating automated workflows that connect your tools and execute multi-step tasks. Build powerful automations without writing code—just drag, drop, and configure.

Whether you're automating employee onboarding, bug triage, sales lead enrichment, or DevOps deployments, the Workflow Builder helps you eliminate repetitive tasks and focus on what matters.

Access Workflow Builder at: `https://app.flowstate.example.com/workflows`

## Key Capabilities

- **Visual Drag-and-Drop Interface**: Build workflows on an intuitive canvas without coding
- **100+ Integrations**: Connect to Slack, GitHub, Jira, Google Workspace, and more
- **Smart Triggers**: Start workflows automatically based on events, schedules, or webhooks
- **Conditional Logic**: Add if/then rules to control workflow behavior
- **Real-Time Testing**: Test workflows with sample data before activating
- **Error Handling**: Configure retries, fallbacks, and notifications
- **Template Library**: Start from pre-built workflows for common use cases

## How It Works

### Accessing Workflows

![Workflow list](https://placeholder-cloudfront-url.com/workflow-builder-overview.png)

Navigate to Workflows from the main menu to see all your workflows. You can view, edit, toggle workflows on/off, and monitor their execution history.

### Creating a Workflow

![Workflow canvas](https://placeholder-cloudfront-url.com/workflow-builder-canvas.png)

To create a new workflow:

1. Click "Create Workflow" from your workflows page
2. Give your workflow a descriptive name
3. Optionally add tags for organization
4. Click "Start Building" to open the canvas

You'll see a visual canvas where you can build your automation step-by-step.

### Adding Triggers

![Triggers panel](https://placeholder-cloudfront-url.com/workflow-builder-triggers.png)

Triggers determine when your workflow runs. Choose from:

**App-Based Triggers:**
- New issue created (GitHub, Jira, Linear)
- Message posted (Slack, Teams)
- Email received
- Form submitted
- File uploaded
- Calendar event

**Schedule-Based Triggers:**
- Daily, weekly, monthly
- Custom cron expressions
- Recurring intervals

**Webhook Triggers:**
- HTTP POST requests
- Custom webhook URLs
- Real-time API integration

To add a trigger:
1. Click "Add Trigger" on the canvas
2. Select the app or trigger type
3. Authenticate with the service (if needed)
4. Configure trigger conditions

### Adding Actions

![Actions panel](https://placeholder-cloudfront-url.com/workflow-builder-actions.png)

Actions are what your workflow does when triggered. Available actions include:

**Communication:**
- Send Slack messages
- Post to Teams channels
- Send emails (Gmail, Outlook, SendGrid)
- Send SMS via Twilio

**Project Management:**
- Create Jira issues
- Create GitHub issues or PRs
- Create Linear tickets
- Create Asana tasks

**Data & Documents:**
- Update spreadsheets
- Generate PDFs
- Upload files
- Create database records

**Developer Tools:**
- Make HTTP requests
- Run code snippets
- Call APIs
- Transform data

To add an action:
1. Click "Add Action" on the canvas
2. Select the integration
3. Choose the action type
4. Configure action settings
5. Map data from triggers or previous actions

### Using Data Mapping

Reference data from triggers and previous actions using template syntax:

```
{{trigger.issue.title}}
{{trigger.issue.assignee}}
{{action1.response.id}}
{{action2.user.email}}
```

This allows you to pass information between steps dynamically.

### Adding Conditional Logic

Control when actions run with if/then conditions:

1. Click "Add Condition" between steps
2. Set up your rule (e.g., `{{trigger.issue.priority}} equals "High"`)
3. Configure what happens when true (if path)
4. Configure what happens when false (else path)

**Supported operators:**
- Equals, does not equal
- Contains, does not contain
- Greater than, less than
- Is empty, is not empty

### Testing Your Workflow

![Test workflow interface](https://placeholder-cloudfront-url.com/workflow-builder-test.png)

Before activating, test your workflow:

1. Click "Test Workflow" in the top right
2. Choose to use sample data or trigger a real event
3. Watch the execution in real-time
4. Review detailed logs for each step
5. Make adjustments if needed

Testing doesn't count against your execution limits and won't affect live data.

### Activating Your Workflow

Once you're satisfied with testing:

1. Click "Activate Workflow"
2. Your workflow is now live
3. FlowState will monitor for triggers and execute automatically
4. View runs in the "Runs" tab

## Configuration

### Workflow Settings

Access settings via the gear icon:

| Setting | Description | Options |
|---------|-------------|---------|
| Name | Workflow identifier | Custom text |
| Description | Document workflow purpose | Custom text |
| Tags | Organize workflows | Comma-separated labels |
| Enabled | Active status | True/False toggle |
| Execution limit | Max runs per hour | 1-1000 (default: 100) |
| Timeout | Max execution time | 1-30 minutes (default: 5) |
| Error policy | How to handle failures | Notify/Retry/Fallback |
| Concurrency | Execution mode | Single/Parallel/Queued |

### Error Handling

Configure how your workflow handles errors:

**Retry Logic:**
- Number of attempts (1-5)
- Delay between retries (exponential backoff)
- Which errors to retry

**Error Notifications:**
- Email notifications on failure
- Slack alerts
- Webhook calls

**Fallback Workflows:**
- Trigger alternative workflow on failure
- Execute cleanup actions
- Log to external systems

### Rate Limiting

Control workflow execution frequency:

- Per minute limits (prevent API throttling)
- Per hour limits (manage costs)
- Per day limits (budget control)

## Use Cases

### Use Case 1: Automated Employee Onboarding

**Situation:** HR team manually performs 15+ steps to onboard each new employee

**Solution:** Automate the entire process with a single workflow

**Workflow:**
1. Trigger: New employee added to HRIS system
2. Action: Create Google Workspace account
3. Action: Create Slack account and add to channels
4. Action: Send welcome email with getting-started guide
5. Action: Create Jira tickets for IT setup tasks
6. Action: Add to project management tools
7. Action: Schedule first-week meetings

**Result:** Onboarding time reduced from 2 hours to 5 minutes

### Use Case 2: Intelligent Bug Triage

**Situation:** Support team needs to route incoming bugs to the right engineering team

**Solution:** Automatically categorize and assign bugs based on severity and type

**Workflow:**
1. Trigger: New bug reported in issue tracker
2. Condition: Check bug severity level
3. If High/Critical:
   - Create PagerDuty incident
   - Post to #engineering-critical Slack channel
   - Assign to on-call engineer
4. If Medium:
   - Assign to appropriate team based on labels
   - Add to sprint planning board
5. If Low:
   - Add to backlog
   - Schedule for review in weekly triage meeting

**Result:** Critical bugs escalated in under 2 minutes, team response time improved by 75%

### Use Case 3: Sales Lead Enrichment

**Situation:** Sales team receives leads with minimal information

**Solution:** Automatically enrich leads with company data and route to the right salesperson

**Workflow:**
1. Trigger: New lead from website form
2. Action: Lookup company data (Clearbit, ZoomInfo)
3. Action: Calculate lead score based on company size, industry, budget
4. Condition: Check lead score
5. If score > 80:
   - Assign to senior sales rep
   - Create high-priority task
   - Send immediate Slack notification
6. If score 50-80:
   - Assign to appropriate regional rep
   - Add to weekly follow-up list
7. If score < 50:
   - Add to nurture campaign
   - Schedule automated follow-up emails

**Result:** Lead response time reduced from 4 hours to 2 minutes, conversion rate increased by 40%

## FAQ

**Q: How many workflows can I create?**

A: Unlimited workflows on all plans. Create as many as you need to automate your processes.

**Q: What happens if a step fails?**

A: Depends on your error handling configuration. You can set workflows to retry automatically, trigger fallback actions, or notify you immediately. Failed workflows don't count against your execution limits.

**Q: Can I test workflows without affecting real data?**

A: Yes. Test mode uses sample data and doesn't trigger actual actions or count against execution limits. You can see exactly what would happen before activating.

**Q: How do I share workflows with my team?**

A: Workflows are shared at the workspace level. All team members can view and edit workflows based on their permissions. You can also export workflows as JSON to share with other accounts.

**Q: Can workflows call other workflows?**

A: Yes. Use the "Trigger Workflow" action to call another workflow. This is useful for creating reusable sub-workflows.

**Q: What's the execution limit?**

A: Default is 100 runs per hour per workflow. You can adjust this in workflow settings. If you need higher limits, contact support.

**Q: Can I schedule workflows to run at specific times?**

A: Yes. Use schedule-based triggers to run workflows daily, weekly, or on custom cron schedules (e.g., "Every Monday at 9am" or "First day of each month").

**Q: How do I debug a failing workflow?**

A: Go to the "Runs" tab and click on a failed run. You'll see detailed execution logs for each step, including error messages, input/output data, and timing information.

## Best Practices

1. **Use Clear Names**: Name workflows with action verbs (e.g., "Notify team of critical bugs" not "Bug workflow")

2. **Add Descriptions**: Document what the workflow does and why it exists

3. **Organize with Tags**: Use tags to group workflows by team, project, or function

4. **Test Thoroughly**: Always test with sample data before activating

5. **Configure Error Handling**: Don't skip error handling—decide what should happen when things go wrong

6. **Monitor Regularly**: Check the Runs tab weekly to catch issues early

7. **Start Simple**: Build basic workflows first, then add complexity

8. **Use Templates**: Browse pre-built templates for common use cases

9. **Document Custom Logic**: Add comments in condition descriptions

10. **Archive Unused Workflows**: Keep your workspace clean by archiving workflows you're no longer using

## Advanced Features

### Template System

Browse 50+ pre-built workflow templates:

- Employee onboarding and offboarding
- Bug triage and escalation
- Sales lead routing
- Social media monitoring
- DevOps automation
- Customer support workflows
- Data backup and sync
- Report generation

Click "Use Template" to create a copy and customize for your needs.

### Workflow Variables

Store reusable values in workflow variables:

- API endpoints
- Default values
- Configuration settings
- Shared constants

Reference variables anywhere in your workflow with `{{vars.variable_name}}`.

### Batch Processing

Process multiple items in a single workflow run:

- Loop through array data
- Apply actions to each item
- Aggregate results
- Handle errors per item

Useful for bulk operations like "Process all new orders" or "Update all matching records".

### Workflow Analytics

Track performance metrics:

- Success vs. failure rate
- Average execution time
- Most/least used workflows
- Error patterns
- Execution volume over time

Use analytics to identify optimization opportunities.

## Need Help?

If you have questions or need assistance:
- Visit our [Help Center](https://docs.flowstate.example.com)
- Contact support: support@flowstate.example.com
- Live chat: Available in-app (bottom right corner)
- Community forum: https://community.flowstate.example.com
