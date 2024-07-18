from crewai import Crew, Process
from tkinter import filedialog, messagebox
import sys, pandas, os, time, asyncio

from agents import AnaylticsCrew
from task import AnalysisMarketingAdData
from utils import chunk_dict

from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

class MainAnalytics:
    def __init__(self, data):
        self.data = data
    
    def run(self):
        agents = AnaylticsCrew()
        tasks = AnalysisMarketingAdData()
        
        data_split_agent = agents.data_split_agent()
        
        results = []
        chunks = chunk_dict(self.data, 10)
        for idx, chunk in enumerate(chunks):
            data_split_agent = agents.data_split_agent()
            split_task = tasks.data_split_task(data_split_agent, chunk)

            crew = Crew(
                agents=[data_split_agent],
                tasks = [split_task],
                process=Process.sequential,
                verbose=True,
            )

            split_result = crew.kickoff()
            results.append(split_result)
            if idx == 1:
                break
        return results
    
    def run2(self, split_data):
        agents = AnaylticsCrew()
        tasks = AnalysisMarketingAdData()

        data_summary_agent = agents.data_summary_agent()
        summary_task = tasks.data_summary_task(data_summary_agent, split_data)

        crew_summary = Crew(
            agents=[data_summary_agent],
            tasks=[summary_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew_summary.kickoff()

        return result
    
if __name__ == "__main__":
    # try:
    file = filedialog.askopenfilenames(initialdir="/", title="파일명 선택")
    if not file:
        messagebox.showwarning("오류", "파일을 선택하세요")
        sys.exit()
    
    report = pandas.read_csv(file[0]).to_dict(orient="list")
    
    analytics_crew = MainAnalytics(report)
    result = analytics_crew.run()
    result2 = analytics_crew.run2(result)