import os
import re
from dotenv import load_dotenv
from github import Github

def get_pr(pr_url:str) -> str:
    load_dotenv()
    GITHUB_PAT=os.getenv("GITHUB_PAT")
    if not GITHUB_PAT:
        raise ValueError("GITHUB_PAT is not set in the environment variables.")
    g = Github(GITHUB_PAT)
    match=re.search(r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)",pr_url)
    if not match:
        raise ValueError("Invalid PR URL format.")  # Raise an error if the URL format is incorrect.
    owner,repo,pull_number=match.groups()
    pull_number=int(pull_number)
    repo = g.get_repo(f"{owner}/{repo}")
    pr = repo.get_pull(pull_number)
    pr_title=pr.title
    pr_body=pr.body if pr.body else ""
    report_comment=[]
    report_comment.append(f"# PR 审查任务\n")
    report_comment.append(f"## PR 标题{pr_title}\n")
    report_comment.append(f"## PR 内容:\n{pr_body}")
    report_comment.append("\n----")
    report_comment.append(f"## 代码变更详情：\n")
    changed_files=pr.get_files()
    if not changed_files:
        report_comment.append("没有检测到代码变更。\n")
    for file in changed_files:
        file_name=file.filename
        status=file.status
        report_comment.append(f"- **文件名:** {file_name}\n")
        report_comment.append(f"  - **状态:** {status}\n")
        report_comment.append(f"Additions: {file.additions}, Deletions: {file.deletions}\n")
        report_comment.append(f"  - **内容:**\n")
        patch=file.patch
        if not patch:
            report_comment.append("  - 没有提供补丁信息。\n")
        else:
            report_comment.append(f"{file.patch}\n")
    changes="".join(report_comment)
    return changes
