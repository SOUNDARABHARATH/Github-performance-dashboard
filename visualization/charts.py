import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class ChartBuilder:
    def plot_commit_frequency(self, commit_frequency_df):
        """Plot commit frequency using Plotly.""" 
        if 'count' not in commit_frequency_df.columns:
            raise ValueError("DataFrame must contain a 'count' column for commit frequency.")

        fig = px.line(commit_frequency_df, x='date', y='count', title='Commit Frequency Over Time')
        fig.update_layout(xaxis_title='Date', yaxis_title='Number of Commits')
        return fig

    def plot_issue_resolution(self, resolution_time):
        """Plot issue resolution time using Plotly.""" 
        fig = px.bar(x=["Issue Resolution Time"], y=[resolution_time], labels={"x": "Metric", "y": "Days"})
        fig.update_layout(title="Average Issue Resolution Time", yaxis_title="Days")
        return fig

    def plot_fork_count_by_month(self, forks_monthly_count_df):
        """Plot fork count by month and year with styled lines and markers using Plotly."""
        if 'count' not in forks_monthly_count_df.columns or 'month_year' not in forks_monthly_count_df.columns:
            raise ValueError("DataFrame must contain 'month_year' and 'count' columns for fork count.")
    
        # Plot line chart with markers
        fig = px.line(forks_monthly_count_df, x='month_year', y='count', 
                  title='Fork Count by Month and Year',
                  labels={'month_year': 'Month-Year', 'count': 'Fork Count'},
                  markers=True)

        # Styling the chart
        fig.update_traces(line=dict(color='royalblue', width=3),  # Line color and thickness
                      marker=dict(size=10, symbol='circle', color='darkorange'),  # Marker style
                      mode='lines+markers')  # Display both lines and markers

        # Customize layout
        fig.update_layout(
        xaxis_title='Month-Year',
        yaxis_title='Fork Count',
        xaxis=dict(showgrid=False, tickangle=45),  # Remove grid lines from X-axis and angle ticks
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),  # Customize Y-axis grid
        plot_bgcolor='white',  # Set plot background color
        title_font=dict(size=24, family='Arial', color='darkblue'),  # Title font style
        xaxis_tickfont=dict(size=12, family='Arial', color='black'),  # X-axis ticks font style
        yaxis_tickfont=dict(size=12, family='Arial', color='black')   # Y-axis ticks font style
    )

        return fig


    def plot_issue_count_by_month(self, issue_counts_df):
        """Plot stacked bar chart of issue counts and resolved issues by month and year.""" 
        try:
            if 'count' not in issue_counts_df.columns or 'resolved_issues' not in issue_counts_df.columns:
                raise ValueError("DataFrame must contain 'count' and 'resolved_issues' columns.")

            # Melt DataFrame for stacked bar plot
            melted_df = issue_counts_df.melt(id_vars='date', value_vars=['resolved_issues', 'unresolved_issues'],
                                             var_name='issue_type', value_name='issue_count')

            fig = px.bar(melted_df, x='date', y='issue_count', color='issue_type',
                         title='Issue Count and Resolution by Month and Year',
                         labels={'date': 'Month-Year', 'issue_count': 'Issue Count', 'issue_type': 'Issue Type'},
                         text='issue_count')
            fig.update_layout(xaxis_title='Month-Year', yaxis_title='Issue Count')
            return fig
        except Exception as e:
            print(f"Error plotting issue count by month: {e}")
            return None

    def plot_issue_pie_chart(self, pie_chart_data_df):
        """Plot pie chart of resolved vs. unresolved issues using Plotly.""" 
        if 'Issue Status' not in pie_chart_data_df.columns or 'Count' not in pie_chart_data_df.columns:
            raise ValueError("DataFrame must contain 'Issue Status' and 'Count' columns for pie chart.")

        fig = px.pie(pie_chart_data_df, names='Issue Status', values='Count',
                     title='Issue Status Overview')
        fig.update_layout(legend_title='Issue Status')
        return fig
    
    def plot_pr_merge_rate(self, merge_rate):
        """Plot pull request merge rate.""" 
        fig = px.bar(x=["PR Merge Rate"], y=[merge_rate], labels={"x": "Metric", "y": "Days"})
        fig.update_layout(title="Average Pull Request Merge Rate", yaxis_title="Days")
        return fig

    def plot_code_review_metrics(self, avg_comments_per_pr):
        """Plot average number of comments per pull request.""" 
        fig = px.bar(x=["Average Comments per PR"], y=[avg_comments_per_pr], labels={"x": "Metric", "y": "Comments"})
        fig.update_layout(title="Average Code Review Comments per Pull Request", yaxis_title="Comments")
        return fig

    def visualize_metrics(self, pr_df, issue_df, period='M'):
        """Visualize PR merge rates and issue resolution times on a dual-axis chart.""" 
        # Process PR data
        pr_df['created_at'] = pd.to_datetime(pr_df['created_at'])
        pr_df.set_index('created_at', inplace=True)
        
        # Calculate PR merge rate for each period
        pr_periodic = pr_df.resample(period).apply(lambda df: pd.Series({'merge_rate': calculate_merge_rate(df)}))

        # Process issue data
        issue_df['created_at'] = pd.to_datetime(issue_df['created_at'])
        issue_df.set_index('created_at', inplace=True)
        issue_periodic = issue_df.resample(period)['resolution_time'].mean()  # Average resolution time

        # Create a dual-axis plot
        fig = go.Figure()

        # PR Merge Rate (left axis)
        fig.add_trace(go.Scatter(
            x=pr_periodic.index, y=pr_periodic['merge_rate'],
            mode='lines+markers',  # Line + marker
            name='PR Merge Rate',
            line=dict(color='blue', dash='solid'),  # Solid blue line
            marker=dict(symbol='circle', color='blue'),  # Circle markers
            yaxis='y1'
        ))

        # Issue Resolution Time (right axis)
        fig.add_trace(go.Scatter(
            x=issue_periodic.index, y=issue_periodic,
            mode='lines+markers',  # Line + marker
            name='Issue Resolution Time (hrs)',
            line=dict(color='red', dash='dash'),  # Dashed red line
            marker=dict(symbol='x', color='red'),  # X markers
            yaxis='y2'
        ))

        # Update layout for dual-axis
        fig.update_layout(
            title='PR Merge Rate and Issue Resolution Time',
            xaxis=dict(title='Date'),
            yaxis=dict(title='PR Merge Rate (%)', titlefont=dict(color='blue'), tickfont=dict(color='blue')),
            yaxis2=dict(title='Issue Resolution Time (hours)', titlefont=dict(color='red'), tickfont=dict(color='red'),
                        overlaying='y', side='right'),
            legend=dict(x=0.1, y=1.1)
        )

        return fig

def calculate_merge_rate(pr_df):
    """Calculate the PR merge rate."""
    merged_count = pr_df['merged_at'].notna().sum()
    total_count = len(pr_df)
    return (merged_count / total_count) * 100 if total_count > 0 else 0
