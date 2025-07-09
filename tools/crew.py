from crewai import Agent,LLM,Task,Process,Crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase,agent,crew,task
from dotenv import load_dotenv
import os
from typing import List
load_dotenv()
BASE_URL1=os.getenv("BASE_URL1")
BASE_URL2=os.getenv("BASE_URL2")
GEMINI_MODEL_NAME=os.getenv("GEMINI_MODEL_NAME")
API_KEY1=os.getenv("API_KEY1")
QWEN_MODEL_NAME=os.getenv("QWEN_MODEL_NAME")
API_KEY2=os.getenv("API_KEY2")
gemini=LLM(model="openai/"+GEMINI_MODEL_NAME,api_key=API_KEY1,base_url=BASE_URL1,timeout=600)
qwen=LLM(model="openai/"+QWEN_MODEL_NAME,api_key=API_KEY2,base_url=BASE_URL2,timeout=600)
gpt4d1=LLM(model="openai/gpt-4.1-2025-04-14",api_key=API_KEY1,base_url=BASE_URL1,timeout=600)
gpt4o=LLM(model="openai/gpt-4o",api_key=API_KEY1,base_url=BASE_URL2,timeout=600)
@CrewBase
class PrAnalyst():
    agents_config="../config/agents.yaml"
    tasks_config="../config/tasks.yaml"
    agents=List[BaseAgent]
    tasks=List[Task]
    model=gemini
    @agent
    def logic_reviewer(self):
        """审查代码逻辑的审查员"""
        return Agent(
            config=self.agents_config["logic_reviewer"],
            llm=self.model,
            verbose=True
        )
    @agent
    def security_auditor(self):
        """审查代码安全的审查员"""
        return Agent(
            config=self.agents_config["security_auditor"],
            llm=self.model,
            verbose=True
        )
    @agent
    def report_synthesizer(self):
        """将多维度的报告综合的报告合成器"""
        return Agent(
            config=self.agents_config["report_synthesizer"],
            llm=self.model,
            verbose=True
       )
    @agent
    def report_reviewer(self):
        """审查报告的审查员"""
        return Agent(
            config=self.agents_config["report_reviewer"],
            llm=qwen,
            verbose=True
        )
    @task
    def analyze_logic(self):
        return Task(
            config=self.tasks_config["analyze_logic"],
        )
    @task
    def analyze_security(self):
        return Task(
            config=self.tasks_config["analyze_security"],
       )
    @task
    def synthesize_report(self):
        return Task(
            config=self.tasks_config["synthesize_report"],
        )
    @task
    def finalize_report(self):
        return Task(
            config=self.tasks_config["finalize_report"],
        )
    @crew
    def crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
    
    def create_crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,   
            process=Process.sequential,
            verbose=False
        )