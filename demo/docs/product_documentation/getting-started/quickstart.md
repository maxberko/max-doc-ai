# FlowState Quickstart

## Overview

Welcome to FlowState! This guide will help you get started with workflow automation in minutes. FlowState helps teams automate repetitive tasks, connect their favorite tools, and build custom workflows without code.

Access FlowState at: `https://app.flowstate.example.com`

## What You'll Learn

In this quickstart, you'll:
- Set up your first workflow
- Connect an integration
- Test and activate your automation
- Monitor workflow runs

## Prerequisites

- A FlowState account (sign up at https://flowstate.example.com)
- At least one integration account (Slack, GitHub, Jira, etc.)
- Basic understanding of triggers and actions

## Step 1: Create Your First Workflow

![Workflow builder](https://placeholder-cloudfront-url.com/workflow-builder.png)

1. Click "Create Workflow" from your dashboard
2. Give your workflow a descriptive name (e.g., "Notify team of new issues")
3. Click "Start Building"

## Step 2: Choose a Trigger

Triggers start your workflow automatically when something happens.

![Select trigger](https://placeholder-cloudfront-url.com/select-trigger.png)

**Popular triggers:**
- New issue created (GitHub, Jira)
- Message posted (Slack)
- Email received
- Schedule (run at specific times)

**For this example:**
1. Select "GitHub" as your trigger
2. Choose "New Issue Created"
3. Connect your GitHub account if you haven't already
4. Select the repository to monitor

## Step 3: Add an Action

Actions are what your workflow does in response to the trigger.

![Add action](https://placeholder-cloudfront-url.com/add-action.png)

**For this example:**
1. Click "Add Action"
2. Select "Slack" from the integrations list
3. Choose "Send Message"
4. Select the channel (e.g., #engineering)
5. Customize the message using data from the trigger:
   ```
   New issue: {{trigger.issue.title}}
   Assigned to: {{trigger.issue.assignee}}
   Link: {{trigger.issue.url}}
   ```

## Step 4: Test Your Workflow

Before activating, test to ensure it works correctly.

![Test workflow](https://placeholder-cloudfront-url.com/test-workflow.png)

1. Click "Test Workflow"
2. FlowState will use sample data to simulate the trigger
3. Check the output to verify the Slack message looks correct
4. Make adjustments if needed

## Step 5: Activate

Once you're satisfied with the test:

1. Click "Activate Workflow"
2. Your workflow is now live!
3. FlowState will monitor for the trigger and execute actions automatically

## Step 6: Monitor Workflow Runs

![Workflow runs](https://placeholder-cloudfront-url.com/workflow-runs.png)

View your workflow's activity:

1. Go to "Workflows" in the main menu
2. Click on your workflow
3. Select the "Runs" tab

**You'll see:**
- When the workflow ran
- Whether it succeeded or failed
- Execution details and logs
- Performance metrics

## Next Steps

Now that you've created your first workflow, explore these capabilities:

- **Add multiple actions**: Chain actions together for complex workflows
- **Use conditionals**: Add logic to control when actions run
- **Try advanced triggers**: Webhooks, custom schedules, and more
- **Explore integrations**: Connect to 100+ tools
- **Check out templates**: Pre-built workflows for common use cases

## Common Use Cases

**DevOps Automation:**
- Auto-deploy on successful builds
- Notify team of failed tests
- Create tickets for production errors

**Sales & Marketing:**
- Auto-add leads to CRM
- Send welcome emails to new signups
- Update spreadsheets with form responses

**Project Management:**
- Auto-assign tasks based on workload
- Send daily standup reminders
- Create reports from project data

## Tips for Success

1. **Start simple**: Begin with one trigger and one action, then expand
2. **Test thoroughly**: Always test before activating production workflows
3. **Monitor regularly**: Check workflow runs to catch issues early
4. **Use clear naming**: Descriptive names make workflows easier to manage
5. **Document your workflows**: Add descriptions and notes for your team

## Need Help?

- **Documentation**: https://docs.flowstate.example.com
- **Community**: Join our Slack community
- **Support**: support@flowstate.example.com
- **Live chat**: Available in the app (bottom right)

---

**Congratulations!** You've created your first automated workflow. Continue exploring FlowState to discover how automation can save your team hours every week.
