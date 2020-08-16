import requests
import json


def yuhun(url):
  reqst = 'https://yys.cbg.163.com/cgi/api/get_equip_detail'

  url = url.split('?')[0]
  url = url.split('/')[-2:]

  assert len(url) == 2, len(url)

  data = {
    'serverid': url[0],
    'ordersn': url[1],
  }

  res = requests.post(reqst, data=data)
  res = _parse(res)
  return res


def _parse(reqst):
  reqst = json.loads(reqst.text)
  reqst = json.loads(reqst['equip']['equip_desc'].encode().decode('unicode_escape'))
  reqst = reqst['inventory']
  print('御魂数:', len(reqst))
  return reqst


if __name__ == '__main__':
  res = yuhun('https://yys.cbg.163.com/cgi/mweb/equip/7/202007292101616-7-AVS8BKAONKILEO')
  with open('temp.txt', 'w') as fb:
    fb.write(str(res))
  for key, value in res.items():
    if value['name'] == '荒骷髅':
      print(value)
      print(key)
      break
  # print(list(res.values())[2])
