import requests
import numpy as np
import pandas as pd
import json

name = 's'
api_url = 'https://api.api-ninjas.com/v1/cats?name={}'.format(name)
response = requests.get(api_url, headers={'X-Api-Key': 'aveEWDcrj2oVHlcQutV9uw==AdXxxmLYwoXGtTTq'})
if response.status_code == requests.codes.ok:
    respons = response.json()
    cats=[]
    cols = ["name", "origin", "max_life_expectancy", "length", "min_weight"]
    a = np.empty(shape=[0, 5])
    for res in respons:
        a = np.append(a, [[res['name'], res['origin'], res['max_life_expectancy'], res['length'], res['min_weight']]], axis=0)
        cats.append(res['name'])
    df = pd.DataFrame(a, columns=cols, index=range(1, (a.shape[0] + 1)))
    print(df)
    with open('cats.json', 'w') as f:
        json_repo = json.dump(cats, f)

else:
    print("Error:", response.status_code, response.text)

