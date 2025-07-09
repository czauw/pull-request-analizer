import streamlit as st
import re
from tools.main import run  # 假设这个函数能正常工作
import os
from st_copy_to_clipboard import st_copy_to_clipboard

st.title("Code Review Assistant")

# --- 1. (关键改动) 在 Session State 中初始化结果变量 ---
if 'analysis_output' not in st.session_state:
    st.session_state.analysis_output = None
if 'pr_url' not in st.session_state:
    st.session_state.pr_url = ""

# --- 输入表单部分 (保持不变) ---
with st.form(key='my_form'):
    # 使用 key 将输入框绑定到 session_state，这样它的值在 rerun 后会保留
    st.text_input("Enter GitHub Pull Request URL", key="pr_url")
    submit_button = st.form_submit_button("Analyze PR")

# --- 2. (关键改动) 将分析逻辑和状态更新分离出来 ---
# 这个 block 只负责处理“分析”这个动作
if submit_button and st.session_state.pr_url:
    with st.spinner("Analyzing PR..."):
        try:
            # 运行分析并将结果对象存入 session_state
            st.session_state.analysis_output = run(st.session_state.pr_url)
        except Exception as e:
            st.session_state.analysis_output = None # 分析失败则清空结果
            st.error(f"Analyze failed: invalid URL or other error. Please try again. {str(e)}")
    # 分析完成后，建议使用 st.rerun() 保证一个干净的重绘
    st.rerun()

# --- 3. (关键改动) 无条件地渲染结果展示区 ---
# 这个 block 只负责根据当前的状态来“画”出界面
st.subheader("Analysis Results")
result_area = st.container(border=True)

# 只要 session_state 中有结果，就显示它和相关按钮
if st.session_state.analysis_output:
    output_raw = st.session_state.analysis_output.raw
    
    with result_area:
        st.markdown(output_raw)
        st_copy_to_clipboard(output_raw, key="clipboard")
        
        # 将保存按钮也放在这里
        save_button = st.button("Save Report")

    # 保存按钮的逻辑紧跟其后
    if save_button:
        try:
            # 确保 report 文件夹存在
            os.makedirs("report", exist_ok=True)
            
            # 使用 session_state 中的 URL 进行正则匹配
            match = re.search(r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)", st.session_state.pr_url)
            if match:
                owner, repo, pull_number = match.groups()
                file_path = os.path.join("report", f"report-{owner}-{repo}-{pull_number}.md")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output_raw)
                st.success(f"Report saved successfully to: {file_path}")
            else:
                st.error("Could not extract information from the URL to create a filename.")
        except Exception as e:
            st.error(f"Failed to save the report: {str(e)}")
else:
    # 如果没有结果，显示提示信息
    with result_area:
        st.info("Please enter a Pull Request URL and click 'Analyze PR'. The results will be displayed here.")

