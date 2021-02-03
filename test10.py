import requests
import json
headers = {
  "Origin": "http://columbus.os.adc.com",
  "Content-Length": "510",
  "Pragma": "no-cache",
  "Cache-Control": "no-cache",
  "Accept": "application/json, text/plain, */*",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
  "Content-Type": "application/json;charset=UTF-8;multipart/form-data",
  "Accept-Encoding": "gzip, deflate",
  "Accept-Language": "zh-CN,zh;q=0.9",
}
cookie = {
  "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%222972%22%2C%22%24device_id%22%3A%221752bd24638a67-002ddd53a002a9-5f4e2917-2073600-1752bd246397f2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%221752bd24638a67-002ddd53a002a9-5f4e2917-2073600-1752bd246397f2%22%7D",
  "user": "16603013472",
  "CI-SESSION": "71d57fbc-d73f-44a9-84a3-810b567ec5dd",
  "SESSION": "c22866ba-5717-47f1-b454-409c05364de6",
  "user-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOiJvcHBvLWNvbHVtYnVzIiwic3ViIjoiMTY2MDMwMTM0NzIiLCJpc3MiOiJvcHBvLWNvbHVtYnVzMTY2MDMwMTM0NzIwIiwidHlwIjoiMCIsInR5cGUiOiIwIiwiaWF0IjoxNjExODgzNzY2fQ.1J-yulZ8Z5aqZGzmIurZ9B0WdyxZD7v0F4Sm5Fzg7NE"
}
params = {"orderBy":[{"column":"createTime","order":"DESC"}],"projectId":"102099","pageInfo":{"pageSize":20,"pageNumber":2},"title":"","statusIds":[101],"priorities":[],"sprintIds":[],"causes":[],"assignUsers":[],"createUsers":[],"isArchived":0,"userDefinedAttrs":{},"createTimes":[],"updateTimes":[],"finishTimes":[],"reopenCauses":[],"sources":[],"types":[],"whetherUseCaseDiscoverys":[],"functionCharacters":[],"refuseCauses":[],"reproduceProbabilitys":[],"findStages":[],"businessEnd":"","expectedSolutionPhase":""}

r = requests.post("http://columbus.os.adc.com/bugList/list?projectId=102099", data=params, headers=headers, cookies=cookie)
print(r.text)