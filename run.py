from tools.main import run
import re
import os

if not os.path.isdir("report"):
    os.makedirs("report",exist_ok=True)

url="https://github.com/bytedance/trae-agent/pull/12"
output=run(url)


match=re.search(r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)",url)
owner,repo,pull_number=match.groups()

with open(os.path.join("report",f"report-{owner}-{repo}-{pull_number}.md"),"w",encoding="utf-8") as f:
    f.write(output.raw)
