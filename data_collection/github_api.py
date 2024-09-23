from github import Github
from datetime import datetime
import pytz
import pandas as pd

class GitHubDataCollector:
    def __init__(self, token):
        self.github = Github(token)

    def _extract_repo_name(self, repo_url):
        # Extract repo name from URL (assuming format https://github.com/owner/repo)
        parts = repo_url.rstrip('/').split('/')
        return f"{parts[-2]}/{parts[-1]}"

    def _convert_to_utc(self, dt):
        """Convert a timezone-aware datetime to UTC."""
        if dt.tzinfo is not None:
            return dt.astimezone(pytz.utc)
        return dt

    def get_forks_data(self, repo_url):
        repo_name = self._extract_repo_name(repo_url)
        repo = self.github.get_repo(repo_name)
        forks = repo.get_forks()

        forks_data = []
        for fork in forks:
            forks_data.append({
                "username": fork.owner.login,
                "date": fork.created_at,
                "profile_image": fork.owner.avatar_url if fork.owner.avatar_url else None
            })
        return forks_data

    def get_repo_data(self, repo_url):
        repo_name = self._extract_repo_name(repo_url)
        repo = self.github.get_repo(repo_name)
        
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "language": repo.language,
            "created_at": self._convert_to_utc(repo.created_at).isoformat(),
            "updated_at": self._convert_to_utc(repo.updated_at).isoformat(),
            "stargazers_count": repo.stargazers_count,
            "forks_count": repo.forks_count,
            "open_issues_count": repo.open_issues_count
        }

    def get_commits_data(self, repo_url):
        repo_name = self._extract_repo_name(repo_url)
        repo = self.github.get_repo(repo_name)
        commits = repo.get_commits()
        
        commits_data = []
        for commit in commits:
            commits_data.append({
                "sha": commit.sha,
                "author": commit.commit.author.name,
                "date": self._convert_to_utc(commit.commit.author.date).isoformat(),
                "message": commit.commit.message
            })
        return commits_data

    def get_issues_data(self, repo_url):
        repo_name = self._extract_repo_name(repo_url)
        repo = self.github.get_repo(repo_name)
        issues = repo.get_issues(state='all')
        
        issues_data = []
        for issue in issues:
            issues_data.append({
                "id": issue.id,
                "title": issue.title,
                "state": issue.state,
                "created_at": self._convert_to_utc(issue.created_at).isoformat(),
                "closed_at": self._convert_to_utc(issue.closed_at).isoformat() if issue.closed_at else "Not Closed"
            })
        return issues_data

    def get_pull_requests_data(self, repo_url):
        repo_name = self._extract_repo_name(repo_url)
        repo = self.github.get_repo(repo_name)
    
        pull_requests_data = []
        for pr in repo.get_pulls(state='all'):
            pull_requests_data.append({
                "id": pr.id,
                "title": pr.title,
                "created_at": pr.created_at.isoformat(),
                "merged_at": pr.merged_at.isoformat() if pr.merged_at else "Not Merged",
                "user": pr.user.login
            })
        return pull_requests_data

    def get_code_reviews_data(self, repo_url):
        repo_name = self._extract_repo_name(repo_url)
        repo = self.github.get_repo(repo_name)
        pull_requests = repo.get_pulls(state='all')
        
        reviews_data = []
        for pr in pull_requests:
            reviews = pr.get_reviews()
            for review in reviews:
                reviews_data.append({
                    "pr_id": pr.id,
                    "reviewer": review.user.login,
                    "submitted_at": self._convert_to_utc(review.submitted_at).isoformat(),
                    "body": review.body
                })
        return reviews_data

    # Fetch PR data
    def fetch_pr_data(self, repo_url):
        repo_name = self._extract_repo_name(repo_url)
        repo = self.github.get_repo(repo_name)
        pulls = repo.get_pulls(state="all")
        
        pr_data = []
        for pr in pulls:
            pr_data.append({
                'number': pr.number,
                'state': pr.state,
                'merged': pr.merged,
                'created_at': pr.created_at,
                'closed_at': pr.closed_at if pr.closed_at else pd.NaT,  # Handle missing closed_at
                'merged_at': pr.merged_at if pr.merged_at else pd.NaT  # Handle missing merged_at
            })
        
        return pd.DataFrame(pr_data)

    # Fetch issue data
    def fetch_issue_data(self, repo_url):
        repo_name = self._extract_repo_name(repo_url)
        repo = self.github.get_repo(repo_name)
        issues = repo.get_issues(state="closed")
        
        issue_data = []
        for issue in issues:
            if not issue.pull_request:  # Exclude PRs labeled as issues
                issue_data.append({
                    'number': issue.number,
                    'created_at': issue.created_at,
                    'closed_at': issue.closed_at,
                    'resolution_time': (issue.closed_at - issue.created_at).total_seconds() / 3600 if issue.closed_at else pd.NA  # Handle missing closed_at
                })
        
        return pd.DataFrame(issue_data)
