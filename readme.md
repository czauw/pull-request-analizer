# AI 驱动的 PR 代码审查助手

这是一个基于 `crewAI` 框架构建的智能 PR (Pull Request) 分析工具。它利用多个大型语言模型 (LLM) Agent 协同工作，从不同维度（例如代码逻辑、安全性）对 GitHub 上的 Pull Request 进行自动化审查，并生成一份综合性的审查报告。

## ✨ 主要功能

- **🤖 自动化代码审查**: 输入一个 GitHub PR 链接，即可自动获取代码变更并进行分析。
- **👥 多 Agent 协作**: 内置多个专门的 Agent，包括逻辑审查员、安全审计员、报告整合员和报告复核员，分工明确，保证审查的深度和广度。
- **🔌 多模型支持**: 使用你自己的api key和需要的任何模型。
- **💻 双重运行模式**:
  - **Web UI**: 提供基于 Streamlit 的图形化界面，操作直观方便。
  - **命令行**: 支持通过 `run.py` 脚本在终端中运行，便于集成和自动化。
- **📄 报告生成与保存**: 分析完成后，将最终报告展示在界面上，并可以一键保存为 Markdown 文件。

## 📂 项目结构

```
.
├── run.py              # 命令行启动脚本
├── webui.py            # Streamlit Web UI 启动脚本
├── config/
│   ├── agents.yaml     # Agent 配置文件 (角色、目标等)
│   └── tasks.yaml      # Task 配置文件 (任务描述、预期产出)
├── tools/
│   ├── crew.py         # 定义 crewAI 的 Agents, Tasks 和 Crew
│   ├── main.py         # 核心运行逻辑
│   └── utils/
│       └── pr_extract.py # 从 GitHub PR 链接提取代码内容的工具
└── report/             # 存放生成的报告文件 (自动创建)
```

## 🚀 安装与配置

**1. 克隆仓库**

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

**2. 安装依赖**
我们强烈建议在虚拟环境中安装依赖。

```bash
# 建议先创建一个 requirements.txt 文件
pip freeze > requirements.txt

# 然后通过 pip 安装
pip install -r requirements.txt
```

主要依赖包括 `crewai`, `streamlit`, `python-dotenv`, \`streamlit-copy-to-clipboard 等。

**3. 配置环境变量**
在项目根目录下创建一个 `.env` 文件。此文件用于存放 API 密钥和模型服务地址等敏感信息。

```env
# .env 文件示例
# 请根据 tools/crew.py 中的 LLM 定义进行配置
BASE_URL1="你的第一个模型服务地址"
API_KEY1="你的第一个 API Key"
GEMINI_MODEL_NAME="模型名称，例如 gemini-pro"

BASE_URL2="你的第二个模型服务地址"
API_KEY2="你的第二个 API Key"
QWEN_MODEL_NAME="模型名称，例如 qwen-max"
```

## 💡 使用说明

### 模式一：Web UI (推荐)

在终端中运行以下命令来启动 Streamlit 应用：

```bash
streamlit run webui.py
```

### 模式二：使用命令行运行

应用启动后，浏览器会自动打开一个页面。在输入框中粘贴 GitHub Pull Request 的 URL，然后点击 "Analyze PR" 按钮即可开始分析。

在终端中直接运行，可以编辑 `run.py` 文件，修改其中的 `url` 变量为你想要分析的 PR 链接。

```python
# ... existing code ...
# 在这里修改为你需要分析的 PR 链接
url="https://github.com/bytedance/trae-agent/pull/12"
output=run(url)
# ... existing code ...
```

然后在终端中执行：

```bash
python run.py
```

脚本运行结束后，审查报告将自动保存在 `report/` 目录下，文件命名格式为 `report-{owner}-{repo}-{pull\_number}.`。
