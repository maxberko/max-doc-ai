# Dashboards

## Overview

Dashboards give you instant visibility into your team's workflows with customizable views that surface the metrics that matter most. Track performance in real-time, spot trends before they become issues, and make data-driven decisions quickly.

Access Dashboards at: `https://app.flowstate.example.com/dashboards`

## Key Capabilities

- **Real-Time Metrics**: Track workflow performance as it happens with automatic updates
- **Drag-and-Drop Customization**: Build your perfect dashboard in seconds with intuitive widgets
- **Smart Insights**: Get actionable recommendations based on your workflow data
- **Team Collaboration**: Share dashboards and create role-specific views
- **Export & Reporting**: Generate reports for stakeholders, retrospectives, or compliance

## How It Works

### Accessing Dashboards

![Dashboard overview](https://placeholder-cloudfront-url.com/dashboards-overview.png)

Navigate to Dashboards from the main menu. Your default dashboard loads automatically with recommended widgets based on your workflows.

### Creating Custom Dashboards

![Dashboard customization](https://placeholder-cloudfront-url.com/dashboards-customization.png)

Create dashboards for different purposes:

1. Click "New Dashboard" in the top right
2. Choose a template or start from scratch
3. Add a descriptive name (e.g., "Engineering Weekly", "Sales Pipeline")
4. Click "Create"

### Adding Widgets

![Available widgets](https://placeholder-cloudfront-url.com/dashboards-widgets.png)

Widgets display different types of data:

**Available widget types:**
- **Success Rate**: Percentage of successful workflow runs
- **Run Count**: Total executions over time
- **Average Duration**: How long workflows take to complete
- **Error Rate**: Failed runs and error patterns
- **Top Performers**: Most active or successful workflows
- **Recent Activity**: Latest workflow runs with status
- **Custom Metrics**: Build your own visualizations

**To add a widget:**
1. Click "Add Widget" on any dashboard
2. Select the widget type
3. Configure the data source and filters
4. Customize appearance (size, colors, time range)
5. Click "Add to Dashboard"

### Arranging Your Dashboard

![Dashboard layout](https://placeholder-cloudfront-url.com/dashboards-layout.png)

Customize the layout:
- **Drag widgets** to reposition them
- **Resize** by dragging corners
- **Delete** by clicking the X icon
- **Duplicate** to quickly create similar widgets
- **Configure** by clicking the settings icon

Changes save automatically.

### Filtering Data

Narrow down what you see:

- **Time Range**: Last hour, day, week, month, or custom
- **Workflows**: Specific workflows or all
- **Status**: Successful, failed, or both
- **Tags**: If you've tagged your workflows

Filters apply to the entire dashboard.

### Sharing Dashboards

![Share dashboard](https://placeholder-cloudfront-url.com/dashboards-share.png)

Collaborate with your team:

1. Click "Share" on any dashboard
2. Choose sharing option:
   - **View Only**: Read-only access
   - **Can Edit**: Full editing permissions
   - **Public Link**: Anyone with link can view
3. Add team members by email or share the link

**Team dashboard management:**
- Set default dashboards for your team
- Create role-specific views (manager, developer, analyst)
- Control who can edit vs. view

## Configuration

### Dashboard Settings

Access settings via the gear icon:

| Setting | Description | Options |
|---------|-------------|---------|
| Auto-refresh | Update frequency | Off, 30s, 1m, 5m, 15m |
| Theme | Visual appearance | Light, dark, auto |
| Default view | What loads first | Any of your dashboards |
| Timezone | Time display | Your timezone or UTC |

### Widget Configuration

Each widget has its own settings:

**Common options:**
- Data source (which workflows)
- Time range (custom or preset)
- Visualization type (chart, table, number)
- Refresh rate (independent of dashboard)
- Alert thresholds (highlight issues)

### Notifications

Get alerted when metrics cross thresholds:

1. Open widget settings
2. Enable "Notifications"
3. Set threshold (e.g., error rate > 5%)
4. Choose notification method (email, Slack)
5. Save

## Use Cases

### Use Case 1: Daily Standup Dashboard

**Situation**: Engineering team wants a quick overview for daily standups

**Solution**: Create a dashboard with:
- Recent deployments (last 24 hours)
- Build success rate
- Open pull requests
- Failed workflows needing attention

**Example**: Team spends 2 minutes reviewing the dashboard at standup instead of 15 minutes gathering status from multiple tools.

### Use Case 2: Executive Summary

**Situation**: Leadership needs monthly workflow efficiency reports

**Solution**: Create a dashboard with:
- Total workflow runs (trend over time)
- Time saved through automation
- Most active workflows
- ROI metrics

Set auto-export to generate monthly reports automatically.

### Use Case 3: On-Call Monitoring

**Situation**: Ops team needs to monitor critical workflows 24/7

**Solution**: Create a dedicated on-call dashboard with:
- Real-time status of production workflows
- Error alerts with severity
- Recent failures with logs
- Escalation status

Share with on-call rotation and enable push notifications.

### Use Case 4: Department Performance

**Situation**: Multiple teams using FlowState want to compare adoption

**Solution**: Create department dashboards showing:
- Workflow usage by team
- Automation coverage (what's automated vs. manual)
- Time savings per department
- Active users and engagement

## FAQ

**Q: How many dashboards can I create?**

A: Unlimited dashboards on all plans.

**Q: Can I export dashboard data?**

A: Yes, click "Export" to download as CSV, PDF, or PNG image.

**Q: Do dashboards update in real-time?**

A: Yes, dashboards refresh automatically based on your auto-refresh setting (default: 1 minute).

**Q: Can I see historical data beyond the current view?**

A: Yes, change the time range filter to view any historical period. Data retention depends on your plan.

**Q: What happens if I delete a dashboard?**

A: The dashboard and its configuration are deleted, but your underlying workflow data is preserved. You can recreate the dashboard anytime.

**Q: Can external stakeholders view dashboards?**

A: Yes, use the "Public Link" sharing option to create a view-only link that works without a FlowState account.

## Best Practices

1. **Start with templates**: Use pre-built dashboards as starting points
2. **One purpose per dashboard**: Keep dashboards focused on specific goals
3. **Use descriptive names**: Make it easy to find the right dashboard
4. **Set appropriate refresh rates**: Balance real-time needs with performance
5. **Review regularly**: Update dashboards as your workflows evolve
6. **Share strategically**: Give team members relevant dashboards, not everything
7. **Set up alerts**: Proactively catch issues before they escalate
8. **Document your metrics**: Add notes explaining what each widget measures

## Need Help?

If you have questions or need assistance:
- Visit our [Help Center](https://docs.flowstate.example.com)
- Contact support: support@flowstate.example.com
- Live chat: Available in-app (bottom right corner)
