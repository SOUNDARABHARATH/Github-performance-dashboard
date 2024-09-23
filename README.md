GitHub Repository Metrics Dashboard
This project provides a dashboard for visualizing various GitHub repository metrics such as commit frequency, issue resolution time, pull request merge rate, and code review metrics. The dashboard uses data from the GitHub API to generate interactive charts using Plotly and integrates a Natural Language Processing (NLP) system to interpret user queries regarding these metrics.

Features
Commit Frequency Visualization: Displays the number of commits over time.
Issue Resolution Time: Shows the average time taken to resolve issues.
Fork Count by Month: Displays the number of repository forks per month and year.
Issue Count and Resolution: A stacked bar chart showing the number of issues opened and resolved each month.
Issue Status Pie Chart: Visualizes resolved vs unresolved issues.
Pull Request (PR) Merge Rate: Shows the average time taken to merge pull requests.
Code Review Metrics: Displays the average number of comments per pull request.
Natural Language Query Processing: Allows users to ask natural language questions like "What is the pull request merge rate?" and receive relevant visualizations.
Project Structure
charts.py: Contains various plotting functions to visualize metrics using Plotly.
nlp_processor.py: Handles natural language queries using predefined patterns and integrates the Ollama language model for advanced queries.
calcuden.py: Implements the logic for calculating various metrics such as commit frequency, issue resolution time, PR merge rate, and code review metrics.
Installation
Prerequisites
 1.Python 3.x
 2.Required Python packages (listed in requirements.txt):
 3.pandas
 4.plotly
 5.re
 6.ollama