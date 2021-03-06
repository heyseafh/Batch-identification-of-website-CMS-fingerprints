#! /usr/bin/env python
# by www.teamssix.com
import sys
import zlib
import json
import requests
import pandas as pd


def whatweb(url):
	response = requests.get(url='{}'.format(url), headers=headers, verify=False, allow_redirects=False,timeout=5)
	whatweb_dict = {"url": response.url, "text": response.text, "headers": dict(response.headers)}
	whatweb_dict = json.dumps(whatweb_dict)
	whatweb_dict = whatweb_dict.encode()
	whatweb_dict = zlib.compress(whatweb_dict)
	data = {"info": whatweb_dict}
	return requests.post("http://whatweb.bugscaner.com/api.go", headers=headers, allow_redirects=False, files=data,timeout=5)


def results(url):
	result = {}
	request = whatweb(url)
	num = request.headers["X-RateLimit-Remaining"]
	print(u"\n\033[1;33;40m[!] 今日识别剩余次数 {},正在识别{}\033[0m".format(num,url))
	req_json = request.json()
	for i in req_json:
		sub_i = req_json[i][0]
		result[i] = sub_i
	result['URL'] = url
	return result


if __name__ == '__main__':
	pools = []
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
	try:
		readDir = sys.argv[1]
		file_name = sys.argv[2]
		f = open(readDir, "r")
	except:
		print('''\033[1;31;40m
请检查你的参数是否有误

示例：python3 Batch_CMS_identification.py url.txt filename.csv
        \033[0m''')
		sys.exit()
	print('\n\033[1;33;40m示例：python3 Batch_CMS_identification.py url.txt filename.csv\033[0m')
	f = f.read().split('\n')
	if f != []:
		for url in f:
			try:
				pools.append(results(url))
			except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
				print('\033[1;31;40m\n[-] {} 连接异常，正在识别下一个URL……\033[0m'.format(url))
				pass
			except BaseException as e:
				print('\033[1;31;40m\n[-] {} 程序发生'.format(url) + str(e) + '异常，正在识别下一个URL……','\033[0m')
				pass
			finally:
				df = pd.DataFrame(pools)
				df.to_csv(r'{}'.format(file_name), encoding='GB2312')
	else:
		print('未读取到url文件，正在退出……')
