import os
import pandas as pd
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Define tools
file_read_tool = FileReadTool()

# Function to preprocess CSV data
def preprocess_csv(df):
    # Preprocess data (example: dropping missing values)
    df = df.dropna()
    return df

# Function to analyze data and generate statistical summaries
def analyze_data(df):
    summary = df.describe().to_markdown()  # Generate statistical summary in markdown format
    with open('output/statistical_summary.md', 'w') as f:
        f.write(summary)
    return summary

# DataAnalyzer Agent: Reads and preprocesses CSV data
data_analyzer_agent = Agent(
    role='DataAnalyzer',
    goal='Read and preprocess CSV data',
    backstory="An expert in data preprocessing and cleaning.",
    tools=[file_read_tool],
    verbose=True
)

# Statistician Agent: Analyzes data and generates statistical summaries
statistician_agent = Agent(
    role='Statistician',
    goal='Analyze data and generate statistical summaries',
    backstory="A data scientist specializing in statistical analysis.",
    verbose=True
)

# Task to read and preprocess CSV data
read_preprocess_task = Task(
    description='Read and preprocess CSV data',
    expected_output='A cleaned DataFrame',
    agent=data_analyzer_agent,
    tools=[file_read_tool],
    function=lambda: preprocess_csv(pd.read_csv('C:/Users/blueorange/Desktop/240626_PA_일일리포트 RAW.csv')),
)

# Task to analyze data and generate statistical summaries
analyze_data_task = Task(
    description='Analyze data and generate statistical summaries',
    expected_output='A statistical summary in markdown format',
    agent=statistician_agent,
    function=lambda: analyze_data(preprocess_csv(pd.read_csv('C:/Users/blueorange/Desktop/240626_PA_일일리포트 RAW.csv'))),  # Pass the output of the first task to the second
)

# Crew setup
crew = Crew(
    agents=[data_analyzer_agent, statistician_agent],
    tasks=[read_preprocess_task, analyze_data_task],
    process=Process.sequential,
    manager_llm=ChatOpenAI(model="gpt-4"),
    verbose=True,
    cache=True,
    full_output=True,
    output_log_file='crew_output.log'
)

# Kickoff the process
result = crew.kickoff()

# Check the results
print(result)