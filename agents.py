from langchain_community.llms import OpenAI
from crewai import Agent
from tools.data_analytics import AnaylzeData
from crewai_tools import FileReadTool


class AnaylticsCrew():

    def data_split_agent(self):
        return Agent(
            role='데이터 통계 엔지니어',
            goal='주어진 모든 tools을 활용하여 입력된 광고 캠페인 운영 성과를 수치화하여 리포트를 작성한다.',
            backstory=("당신은 전문적인 데이터 엔지니어로,"
                    "광고 데이터 성과 수치화에 뛰어난 강점을 가지고 있습니다"),
            
            tools=[
                    AnaylzeData.sum_data,
                    AnaylzeData.check_data,
                    AnaylzeData.filter_data,
                    # AnaylzeData.eval_expr,
                    # AnaylzeData.data_expr
                   ],
                   
            memory=True,
            verbose=True
        )
        
    def data_summary_agent(self):
        return Agent(
            role='광고 성과 분석가',
            goal='개별 보고서를 종합하여 리포트를 작성한다.',
            backstory=("당신은 전문적인 마케팅 데이터 분석가로,"
                    "광고 데이터 성과 통합 및 분석에 뛰어난 강점을 가지고 있습니다"),
            
            tools=[AnaylzeData.eval_expr],
                   
            memory=True,
            verbose=True,
        )

