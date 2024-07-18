import pandas as pd

def chunk_dict(data, chunk_size):
    """딕셔너리를 청크로 분할합니다."""
    keys = list(data.keys())
    # chunks = []
    # for i in range(0, len(keys), chunk_size):
    #     chunk = {k: data[k][i:i + chunk_size] for k in keys}
    #     chunks.append(chunk)

    chunks = []
    size = len(pd.DataFrame(data))
    for i in range(0, size, chunk_size):
        chunk = {k: data[k][i: i + chunk_size] for k in keys}
        chunks.append(chunk)

    return chunks