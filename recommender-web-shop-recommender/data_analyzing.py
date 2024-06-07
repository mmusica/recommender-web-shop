import pandas as pd
import json
from io import StringIO

#file = 'meta_Electronics.jsonl'
file = "ME_small.jsonl"
if __name__ == "__main__":
    
    df = pd.read_json(path_or_buf=file, lines=True)
    print(df.head(2))
    #df = pd.read_json(StringIO(str(data)))
