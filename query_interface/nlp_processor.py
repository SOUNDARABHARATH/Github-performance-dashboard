import re
import ollama

class NLPProcessor:
    def __init__(self):
        # Define query patterns for common metrics
        self.query_patterns = {
            'commit_frequency': re.compile(r'\bcommit frequency\b', re.IGNORECASE),
            'issue_resolution': re.compile(r'\bissue resolution time\b', re.IGNORECASE),
            'pr_merge_rate': re.compile(r'\bpull request merge rate\b', re.IGNORECASE),
            'code_review_metrics': re.compile(r'\bcode review metrics\b', re.IGNORECASE)
        }

    def process_query(self, query):
        """
        Process the user's natural language query and return the appropriate result.
        If the query matches predefined patterns, return the corresponding metric type.
        Otherwise, send the query to the Ollama LLM model for further processing.
        """
        query = query.strip().lower()

        # Check if the query matches any predefined patterns
        for key, pattern in self.query_patterns.items():
            if pattern.search(query):
                return key

        # If no predefined patterns match, use Ollama LLM for query processing
        try:
            desired_model = 'llama3.1:8b'

            # Send query to Ollama model
            response = ollama.chat(model=desired_model, messages=[
                {
                    'role': 'user',
                    'content': query,
                },
            ])

            # Extract the response message from Ollama's output
            llm_response = response['message']['content']

            return llm_response

        except Exception as e:
            # Handle exceptions related to the LLM model
            return f"Error processing query: {str(e)}"
