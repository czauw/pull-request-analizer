import sys
import warnings
from tools.crew import PrAnalyst
from tools.utils.pr_extract import get_pr
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run(input:str):
    pr_content = get_pr(input)  # Assuming get_pr function returns the content of the PR
    inputs={
        "code": pr_content,  # Assuming pr_content contains the code to be analyzed
    }
    try:
        output=PrAnalyst().crew().kickoff(inputs=inputs)
        return output
    except Exception as e:
        raise Exception(f"Error during analysis: {e}")

def run_in_stream(input:str):
    pr_content = get_pr(input)  # Assuming get_pr function returns the content of the PR
    inputs={
        "code": pr_content,  # Assuming pr_content contains the code to be analyzed
    }
    try:
        output=PrAnalyst().crew().crew.stream()
        return output
    except Exception as e:
        raise Exception(f"Error during analysis: {e}")
