import streamlit as st
import re
from tools.main import run  
import os
from st_copy_to_clipboard import st_copy_to_clipboard

st.title("Code Review Assistant")


if 'analysis_output' not in st.session_state:
    st.session_state.analysis_output = None
if 'pr_url' not in st.session_state:
    st.session_state.pr_url = ""


with st.form(key='my_form'):
    
    st.text_input("Enter GitHub Pull Request URL", key="pr_url")
    submit_button = st.form_submit_button("Analyze PR")



if submit_button and st.session_state.pr_url:
    with st.spinner("Analyzing PR..."):
        try:
            
            st.session_state.analysis_output = run(st.session_state.pr_url)
        except Exception as e:
            st.session_state.analysis_output = None 
            st.error(f"Analyze failed: invalid URL or other error. Please try again. {str(e)}")
    
    st.rerun()



st.subheader("Analysis Results")
result_area = st.container(border=True)


if st.session_state.analysis_output:
    output_raw = st.session_state.analysis_output.raw
    
    with result_area:
        st.markdown(output_raw)
        st_copy_to_clipboard(output_raw, key="clipboard")
        
        
        save_button = st.button("Save Report")

    
    if save_button:
        try:
            
            os.makedirs("report", exist_ok=True)
            
            
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
    
    with result_area:
        st.info("Please enter a Pull Request URL and click 'Analyze PR'. The results will be displayed here.")

