import streamlit as st
from data_collection.github_api import GitHubDataCollector
from data_collection.data_storage import DataStorage
from metrics.calculator import MetricsCalculator
from visualization.charts import ChartBuilder
from query_interface.nlp_processor import NLPProcessor
from visualization.dashboard import display_summary, load_data


token = st.secrets["github"]["key"]


    
st.title("Developer Performance Dashboard")
repo_url = st.text_input("Enter GitHub Repository URL")

if repo_url:
    collector = GitHubDataCollector(token)
    data_storage = DataStorage()
    nlp_processor = NLPProcessor()
    chart_builder = ChartBuilder()
    progress_bar = st.progress(0)

    try:
        repo_data = collector.get_repo_data(repo_url)
        commits_data = collector.get_commits_data(repo_url)
        issues_data = collector.get_issues_data(repo_url)
        forks_data = collector.get_forks_data(repo_url)
        pull_requests_data = collector.get_pull_requests_data(repo_url)
        reviews_data = collector.get_code_reviews_data(repo_url)

        data_storage.save_data_to_csv(repo_data, f"{repo_data['name']}_repo.csv")
        data_storage.save_data_to_csv(commits_data, f"{repo_data['name']}_commits.csv")
        data_storage.save_data_to_csv(issues_data, f"{repo_data['name']}_issues.csv")
        data_storage.save_data_to_csv(pull_requests_data, f"{repo_data['name']}_pull_requests.csv")
        data_storage.save_data_to_csv(reviews_data, f"{repo_data['name']}_reviews.csv")

        progress_bar.progress(100)

        # Cache data and metrics
        cached_data = load_data(
            repo_data, commits_data, issues_data, forks_data, pull_requests_data, reviews_data
        )

        display_summary(
            repo_data,
            collector.github.get_repo(collector._extract_repo_name(repo_url)).owner,
            cached_data["avg_star_rating"],
            forks_data,
            cached_data["commit_frequency"],
            cached_data["issue_resolution"],
            cached_data["issue_counts_by_month"],
            cached_data["issue_pie_chart_data"],
            cached_data["pr_df"],
            cached_data["issue_df"],
            cached_data["pr_merge_rate"],
            cached_data["avg_comments_per_pr"],
            chart_builder,
            nlp_processor
        )

    except Exception as e:
        st.error(f"Error fetching data: {e}")
