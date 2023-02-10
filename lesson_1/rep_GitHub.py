import requests as rq
import json

respons = rq.get('https://api.github.com/users/RinaKoner128/repos').json()
repos=[]

for res in respons:
    repos.append(res['name'])
print(repos)

with open('repos.json', 'w') as f:
    json_repo = json.dump(repos, f)

