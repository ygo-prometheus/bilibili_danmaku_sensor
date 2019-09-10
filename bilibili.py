from lxml import etree
import requests
import time
import jieba
import numpy as np
from PIL import Image
from wordcloud import WordCloud as wc
class Bilibili():
	"""docstring for Bilibili"""
	def __init__(self,oid):
		self.headers={
		'Host': 'api.bilibili.com',
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Cookie': 'finger=edc6ecda; LIVE_BUVID=AUTO1415378023816310; stardustvideo=1; CURRENT_FNVAL=8; buvid3=0D8F3D74-987D-442D-99CF-42BC9A967709149017infoc; rpdid=olwimklsiidoskmqwipww; fts=1537803390'

		}
		self.url='https://api.bilibili.com/x/v1/dm/list.so?oid='+str(oid)
		self.barrage_reault=self.get_page()

	# 获取信息
	def get_page(self):
		try:
			# 延时操作，防止太快爬取
			time.sleep(0.5)
			response=requests.get(self.url,headers=self.headers)
		except Exception as e:
			print('获取xml内容失败,%s' % e)
			return False
		else:
			if response.status_code == 200:
				# 下载xml文件
				with open('bilibili.xml','wb') as f:
					f.write(response.content)
				return True
			else:
				return False

	# 解析网页
	def param_page(self):
		time.sleep(1)
		if  self.barrage_reault:
			# 文件路径，html解析器
			html=etree.parse('bilibili.xml',etree.HTMLParser())
			# xpath解析，获取当前所有的d标签下的所有文本内容
			results=html.xpath('//d//text()')
			return results

	# 弹幕去重
	def remove_double_barrage(self):
		'''
		double_arrage:所有重复弹幕的集合
		results:去重后的弹幕
		barrage:每种弹幕内容都存储一遍
		'''
		double_barrage=[]
		results=[]
		barrage=set()
		for result in self.param_page():
			if result not in results:
				results.append(result)
			else:
				double_barrage.append(result)
				barrage.add(result)
		return double_barrage,results,barrage

	# 弹幕重复计算和词云的制作
	def make_wordCould(self):
		double_barrages,results,barrages=self.remove_double_barrage()
		# 重词计数
		with open('barrages.txt','w') as f:
			for barrage in barrages:
				amount=double_barrages.count(barrage)
				f.write(barrage+':'+str(amount+1)+'\n')
				
		# 设置停用词
		stop_words=['【','】',',','.','?','!','。']
		words=[]
		if results:
			for result in results:
				for stop in stop_words:
					result=''.join(result.split(stop))
				words.append(result)
			# 列表拼接成字符串
			words=''.join(words)
			words=jieba.cut(words)
			words=''.join(words)
			luo=np.array(Image.open('洛天依.jpg'))
			w=wc(font_path='‪C:/Windows/Fonts/SIMYOU.TTF',background_color='white',width=1600,height=1600,max_words=2000,mask=luo)
			w.generate(words)
			w.to_file('luo.jpg')
			



b=Bilibili(2238927)
b.make_wordCould()