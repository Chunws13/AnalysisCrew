from langchain.tools import tool
import pandas as pd

class AnaylzeData():
    @tool("데이터 선별")
    def check_data(data: dict):
        """
        데이터 합산 전, 어떤 데이터를 합산할 수 있는지 확인한다.
        return 된 데이터는 함수명 : sum_data 필드의 fields Args에 사용 가능하다.

        이미 해당 함수를 사용하여 결과를 구한 경우, True가 반환된다.

        Args:
            data(dict): 필드 타입을 검사하고자 하는 데이터의 딕셔너리

        Returns:
            함수를 사용한 적이 없는 경우, 
                dict : sum_data의 fields Args에 적용 가능한 필드 목록

            함수를 사용한 적이 있는 경우,
                Bool : True
        """
        if hasattr(data, 'check_data') and data['check_data']:
            return data['check_data']
        
        keys = data.keys()
        result = []
        for key in keys:
            if all(isinstance(x, (int, float)) for x in data[key]):
                result.append(key)
        
        data['check_data'] = True
        return result

    @tool("데이터 합계")
    def sum_data(data: dict, fields: list):
        """
        노출, 클릭, 비용, 전환 등 수치로 입력된 데이터의 합계를 구할 수 있음
        
        Args:
            data (dict): 합계를 구할 데이터가 포함된 딕셔너리
            fields (list): 그룹화 할 필드 이름들의 리스트
        
        Returns:
            함수를 사용한 적이 없는 경우
                dict: 각 필드 이름을 키로 하고, 그 값의 합계를 값으로 하는 딕셔너리
        
        Raises:
            KeyError: 지정된 필드가 데이터에 존재하지 않을 때
            TypeError: 필드의 값들이 수치가 아닐 때
        """
        # if hasattr(data, 'sum_data') and data.sum_data:
        #     return
        
        result = {}
        
        for field in fields:
            try:
                # 필드가 존재하지 않는 경우 예외 발생
                if field not in data:
                    raise KeyError(f"Field '{field}' not found in the data")
                
                # 필드의 값이 리스트가 아니거나 값들이 수치가 아닌 경우 예외 발생
                if not all(isinstance(x, (int, float)) for x in data[field]):
                    raise TypeError(f"All values in the field '{field}' must be numeric")
                
                # 합계를 계산하여 딕셔너리에 저장
                result[field] = sum(data[field])
            
            except KeyError as ke:
                raise ke
            
            except TypeError as te:
                raise te
            
            except Exception as e:
                raise e
            
        # data['sum_data'] = True
        return result
    
    @tool("데이터 필터")
    def filter_data(data: dict, field: str, condition: str):
        """
        data 중 특정 field 의 condition의 데이터를 반환한다.

        Args:
            data (dict): 필터링 되기 전 데이터
            field (str): 필터링 기준이 되는 행
            condition (str): 필터 조건
        
        Return:
            dict: 입력한 조건에 맞게 필터링 된 데이터

        Raises:
            KeyError: data에 입력한 field가 없는 경우
            TypeError: field 내 데이터가 object Type이 아닌 경우
            Exception: filed 내 condition 이 없는 경우
        """

        data_frame = pd.DataFrame(data)

        if data_frame[field].dtype != object:
            raise TypeError("object type의 필드만 입력 가능합니다.")
        
        if field not in data_frame.columns:
            raise KeyError("해당 필드는 데이터에 없습니다.")
        
        if condition not in data_frame[field].unique():
            raise Exception("해당 condition은  field 내 없습니다")
        
        filter_data = data_frame[data_frame[field] == condition]

        return filter_data.to_dict(orient="list")
    
    @tool("수식 계산기")
    def eval_expr(expr):
        """
        수식을 평가하여 결과를 반환합니다.
        
        Args:
            expr (str): 평가할 수식
        
        Returns:
            float: 수식의 평가 결과
        
        Raises:
            ValueError: 수식이 잘못되었거나 허용되지 않은 연산이 포함된 경우
        """
        try:
            return eval(expr)
        
        except Exception as e:
            raise ValueError(f"Invalid expression: {expr}") from e
        
    @tool("데이터 프레임 수식 계산기")
    def data_expr(expr, data):
        """
        데이터프레임의 수식을 계산할 수 있음
        """
        try:
            data = pd.DataFrame(data)
            return eval(expr)

        except:
            return data

if __name__ == "__main__":
    report = {
        "기간" : ["2024-06-26", "2024-06-27"],
        "매체" : ["네이버", "카카오"],
        '광고비' : [10000, 20000],
        '클릭수': [200, 160],
        '노출수' : [154523, 52146],
        "PA 청약": [3, 8]
    }

    data = AnaylzeData.filter_data(report, "기간", "2024-06-26")
    print(data)