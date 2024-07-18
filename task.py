from crewai import Task
from textwrap import dedent

class AnalysisMarketingAdData():
    
    def data_split_task(self, agent, data):
        convert_data = {'data': data}
        return Task(
            description = dedent(
                f"""
                주어진 데이터를 tool로 분석한 리포트를 작성하시오.
                {convert_data}
                """
                ),
            agent= agent,
            expected_output = dedent(
                """
                결과 보고서 예시:
                1. 데이터 기간
                2. 전체 노출, 클릭, 비용, 전환 데이터
                3. 광고 매체 별 노출, 클릭, 비용, 전환 데이터
                보고서는 모두 한국어로 작성해야 한다.
                """),
            async_execution = False,
            )
    
    def data_summary_task(self, agent, split_results):
        
        integration_task = Task(
        description=dedent(
            f"""
            분석된 데이터를 합산하여 최종 보고서를 작성하시오.
            추가로 CTR, CVR 등 비율 지표까지 계산해야 한다
            데이터 : {split_results}
            """
        ),
        agent=agent,
        expected_output=dedent(
            """
            최종 보고서 예시:
            1. 데이터 기간
            2. 전체 노출, 클릭, 비용 합계
            보고서는 모두 한국어로 작성해야 한다.
            """
            ),
        async_execution=False
        )

        return integration_task