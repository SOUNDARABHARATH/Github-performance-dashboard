import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
from metrics.calculator import MetricsCalculator
from visualization.charts import ChartBuilder


@st.cache_data
def load_data(repo_data, commits_data, issues_data, forks_data, pull_requests_data, reviews_data):
    # Assuming `MetricsCalculator` and `ChartBuilder` are properly implemented
    raw_data = {
        "commits": commits_data,
        "issues": issues_data
    }
    metrics_calculator = MetricsCalculator(raw_data)
    commit_frequency = metrics_calculator.calculate_commit_frequency()
    issue_resolution = metrics_calculator.calculate_issue_resolution_time()
    issue_counts_by_month = metrics_calculator.calculate_issue_counts_by_month()
    issue_pie_chart_data = metrics_calculator.calculate_issue_pie_chart_data()
    pr_df = pd.DataFrame(pull_requests_data)
    issue_df = pd.DataFrame(issues_data)
    pr_merge_rate = metrics_calculator.calculate_pr_merge_rate(pr_df)
    avg_comments_per_pr = metrics_calculator.calculate_code_review_metrics(reviews_data)

    avg_stars = repo_data['stargazers_count']
    avg_star_rating = min(avg_stars / 50, 5)

    return {
        "commit_frequency": commit_frequency,
        "issue_resolution": issue_resolution,
        "issue_counts_by_month": issue_counts_by_month,
        "issue_pie_chart_data": issue_pie_chart_data,
        "pr_df": pr_df,
        "issue_df": issue_df,
        "pr_merge_rate": pr_merge_rate,
        "avg_comments_per_pr": avg_comments_per_pr,
        "avg_star_rating": avg_star_rating
    }

def display_summary(
    repo_data, user, avg_star_rating, forks_data, commit_frequency,
    issue_resolution, issue_counts_by_month, issue_pie_chart_data,
    pr_df, issue_df, pr_merge_rate, avg_comments_per_pr, chart_builder, nlp_processor
):
   # Process all the data first

    # Summary Report content
    summary_report_html = f"""
    <div style="position:relative; border:1px solid #ccc; padding:16px; border-radius:8px;">
        <div style="position:absolute; top:16px; right:16px;">
            <img src="{user.avatar_url if user.avatar_url else 'https://via.placeholder.com/100'}" width="100" alt="Profile Image" style="border-radius:50%;"/>
        </div>
        <h2 style="margin:0;">User Information</h2>
        <hr style="border:1px solid #ddd;">
        <ul style="list-style-type:none; padding:0;">
            <li><strong>Name:</strong> {user.name}</li>
            <li><strong>User ID:</strong> {user.id}</li>
            <li><strong>Bio:</strong> {user.bio if user.bio else 'No Bio'}</li>
            <li><strong>Total Repositories:</strong> {user.public_repos}</li>
            <li><strong>Followers Count:</strong> {user.followers}</li>
            <li><strong>Following Count:</strong> {user.following}</li>
        </ul>
    </div>
    <div style="border:1px solid #ccc; padding:16px; border-radius:8px;">
        <h2 style="margin:0;">Repository Overview</h2>
        <hr style="border:1px solid #ddd;">
        <ul style="list-style-type:none; padding:0;">
            <li><strong>Repository Name:</strong> {repo_data['name']}</li>
            <li><strong>Description:</strong> {repo_data['description']}</li>
            <li><strong>Language:</strong> {repo_data['language']}</li>
            <li><strong>Created At:</strong> {repo_data['created_at']}</li>
            <li><strong>Updated At:</strong> {repo_data['updated_at']}</li>
            <li><strong>Stars Count:</strong> {repo_data['stargazers_count']}</li>
            <li><strong>Forks Count:</strong> {repo_data['forks_count']}</li>
            <li><strong>Open Issues Count:</strong> {repo_data['open_issues_count']}</li>
            <li><strong>Average Star Rating:</strong> {'⭐' * int(avg_star_rating)}{''.join(['☆' for _ in range(5 - int(avg_star_rating))])}</li>
        </ul>
    </div>
    """

    # Commit Frequency content
    commit_frequency_chart = None
    if (repo_data['forks_count'] != 0 or repo_data['open_issues_count'] != 0) and len(commit_frequency) > 0 and repo_data['stargazers_count'] != 0:
        commit_frequency_chart = chart_builder.plot_commit_frequency(commit_frequency)

    # Forks Details content
    forks_chart = None
    forks_table_html = None
    if (repo_data['forks_count'] != 0 or repo_data['open_issues_count'] != 0) and len(commit_frequency) > 0 and repo_data['stargazers_count'] != 0:
        forks_df = pd.DataFrame(forks_data)
        forks_df['date'] = pd.to_datetime(forks_df['date'])
        forks_df['month_year'] = forks_df['date'].dt.strftime('%Y-%m')
        forks_monthly_count = forks_df.groupby('month_year').size().reset_index(name='count')
        forks_chart = chart_builder.plot_fork_count_by_month(forks_monthly_count)

        forks_df_display = pd.DataFrame({
            'S.No': range(1, len(forks_df) + 1),
            'Profile Image': [fork['profile_image'] if fork['profile_image'] else "https://via.placeholder.com/50" for fork in forks_data],
            'Username': [fork['username'] for fork in forks_data],
            'Date': [fork['date'].strftime('%Y-%m-%d') for fork in forks_data]
        })

        def image_formatter(image_url):
            return f'<img src="{image_url}" width="50"/>'

        forks_df_display['Profile Image'] = forks_df_display['Profile Image'].apply(image_formatter)
        forks_table_html = forks_df_display.to_html(index=False, escape=False, border=1)

    # Issues Count and Status content
    issues_chart = None
    issues_pie_chart = None
    if (repo_data['forks_count'] != 0 or repo_data['open_issues_count'] != 0) and len(commit_frequency) > 0 and repo_data['stargazers_count'] != 0:
        issues_chart = chart_builder.plot_issue_count_by_month(issue_counts_by_month)
        issues_pie_chart = chart_builder.plot_issue_pie_chart(issue_pie_chart_data)

    #side bar
    st.sidebar.title("Navigation")
    nav_option = st.sidebar.radio(
        "Go to Section:",
        ("Summary Report", "Commit Frequency", "Forks Details", "Issues Count and Status")
    )
    # Display content based on nav_option
    if nav_option == "Summary Report":
        st.header("Summary Report based on GitHub URL")
        st.markdown(summary_report_html, unsafe_allow_html=True)

    elif nav_option == "Commit Frequency":
        if commit_frequency_chart:
            st.header("Commit Frequency")
            st.plotly_chart(commit_frequency_chart)
        else:
            st.write("Need more information to generate metrics.")

    elif nav_option == "Forks Details":
        if forks_chart and forks_table_html:
            st.header("Forks Count by overtime period")
            st.plotly_chart(forks_chart)

            st.header("Forking Project Other People Information")
            st.write(forks_table_html, unsafe_allow_html=True)
        else:
            st.write("Need more information to generate metrics.")

    elif nav_option == "Issues Count and Status":
        if issues_chart and issues_pie_chart:
            st.header("Issues Count by Over Time period")
            st.plotly_chart(issues_chart)

            st.header("Issue Status Overview")
            st.plotly_chart(issues_pie_chart)
        else:
            st.write("Need more information to generate metrics.")
    # Optional: Natural Language Query section
    st.header("Natural Language Query")
    query = st.text_input("Ask a question (e.g., 'show commit frequency')", key="nlp_query_1")
    if query:
        result = nlp_processor.process_query(query)
        if result == 'commit_frequency':
            st.plotly_chart(chart_builder.plot_commit_frequency(commit_frequency))
        elif result == 'issue_resolution':
            st.write(f"Average issue resolution time: {issue_resolution:.2f} days")
        elif result == 'pr_merge_rate':
            st.write(f"b: {pr_merge_rate:.2f}%")
        elif result == 'code_review_metrics':
            st.write("Code review metrics not implemented yet.")
        else:
            st.write(result)