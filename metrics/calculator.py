import pandas as pd

class MetricsCalculator:
    def __init__(self, data):
        self.data = data
        self.commits_data = pd.DataFrame(data.get('commits', []))
        self.issues_data = pd.DataFrame(data.get('issues', []))
        self.repo_data = data.get('repo', {})
    
    def check_repo_data_validity(self):
        """Check if repository has sufficient data (stars, forks, open issues, commits)."""
        stars_count = self.repo_data.get('stargazers_count', 0)
        forks_count = self.repo_data.get('forks_count', 0)
        open_issues_count = self.repo_data.get('open_issues_count', 0)
        commit_count = len(self.commits_data)

        if stars_count == 0 and forks_count == 0 and open_issues_count == 0 and commit_count == 0:
            return "Need more information. The repository has no stars, forks, open issues, or commits."
        return None
    
    def calculate_commit_frequency(self):
        """Calculate commit frequency by month."""
        try:
            validity_message = self.check_repo_data_validity()
            if validity_message:
                return validity_message

            if self.commits_data.empty:
                return "No commit data available."

            self.commits_data['date'] = pd.to_datetime(self.commits_data['date'], utc=True)
            commit_frequency = self.commits_data.groupby(self.commits_data['date'].dt.to_period('M')).size().reset_index(name='count')
            commit_frequency['date'] = commit_frequency['date'].dt.to_timestamp()  # Convert to timestamp for Plotly
            return commit_frequency
        except Exception as e:
            print(f"Error calculating commit frequency: {e}")
            return pd.DataFrame()
    
    def calculate_issue_resolution_time(self):
        """Calculate average issue resolution time in days."""
        try:
            validity_message = self.check_repo_data_validity()
            if validity_message:
                return validity_message

            if self.issues_data.empty:
                return "No issue data available."

            self.issues_data['created_at'] = pd.to_datetime(self.issues_data['created_at'])
            self.issues_data['closed_at'] = pd.to_datetime(self.issues_data['closed_at'], errors='coerce')
            self.issues_data['resolution_time'] = (self.issues_data['closed_at'] - self.issues_data['created_at']).dt.days
            resolution_time = self.issues_data['resolution_time'].dropna().mean()
            return resolution_time
        except Exception as e:
            print(f"Error calculating issue resolution time: {e}")
            return float('nan')
    
    def calculate_issue_counts_by_month(self):
        """Calculate issue counts and resolved/unresolved issues by month."""
        try:
            validity_message = self.check_repo_data_validity()
            if validity_message:
                return validity_message

            if self.issues_data.empty:
                return "No issue data available."

            self.issues_data['created_at'] = pd.to_datetime(self.issues_data['created_at'])
            issue_counts = self.issues_data.groupby(self.issues_data['created_at'].dt.to_period('M')).size().reset_index(name='count')
            issue_counts['resolved_issues'] = self.issues_data.groupby(self.issues_data['created_at'].dt.to_period('M'))['closed_at'].count().reset_index(name='resolved_issues')['resolved_issues']
            issue_counts['unresolved_issues'] = issue_counts['count'] - issue_counts['resolved_issues']
            issue_counts['date'] = issue_counts['created_at'].dt.to_timestamp()
            return issue_counts
        except Exception as e:
            print(f"Error calculating issue counts by month: {e}")
            return pd.DataFrame()
    
    def calculate_issue_pie_chart_data(self):
        """Calculate data for pie chart showing resolved vs unresolved issues."""
        try:
            validity_message = self.check_repo_data_validity()
            if validity_message:
                return validity_message

            if self.issues_data.empty:
                return "No issue data available."

            total_issues = len(self.issues_data)
            unresolved_issues = self.issues_data['closed_at'].isna().sum()
            resolved_issues = total_issues - unresolved_issues
            return pd.DataFrame({
                'Issue Status': ['Resolved', 'Unresolved'],
                'Count': [resolved_issues, unresolved_issues]
            })
        except Exception as e:
            print(f"Error calculating pie chart data: {e}")
            return pd.DataFrame()
    
    def calculate_pr_merge_rate(self, pull_requests_data):
        """Calculate the average time to merge pull requests."""
        try:
            validity_message = self.check_repo_data_validity()
            if validity_message:
                return validity_message

            pr_df = pd.DataFrame(pull_requests_data)
            if pr_df.empty:
                return "No pull request data available."

            pr_df['created_at'] = pd.to_datetime(pr_df['created_at'], utc=True)
            pr_df['merged_at'] = pd.to_datetime(pr_df['merged_at'], errors='coerce', utc=True)
            pr_df['time_to_merge'] = (pr_df['merged_at'] - pr_df['created_at']).dt.days
            merge_rate = pr_df['time_to_merge'].dropna().mean()
            return merge_rate
        except Exception as e:
            print(f"Error calculating PR merge rate: {e}")
            return float('nan')
    
    def calculate_code_review_metrics(self, reviews_data):
        """Calculate average number of comments per pull request."""
        try:
            validity_message = self.check_repo_data_validity()
            if validity_message:
                return validity_message

            reviews_df = pd.DataFrame(reviews_data)
            if 'pr_id' not in reviews_df.columns:
                raise ValueError("Missing 'pr_id' column in reviews data")

            if reviews_df.empty:
                return "No code review data available."

            comments_per_pr = reviews_df.groupby('pr_id').size()
            avg_comments_per_pr = comments_per_pr.mean()
            return avg_comments_per_pr
        except Exception as e:
            print(f"Error calculating code review metrics: {e}")
            return float('nan')
