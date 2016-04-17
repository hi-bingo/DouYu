import requests,re,threading,time,redis,json,logging
from lxml import etree
from setting import *

DOUYU_BASE_URL='http://www.douyu.com/directory/'
DETECT_BASE_URL='http://apicn.faceplusplus.com/detection/detect'
BASE_URL='http://www.douyu.com'

Types_Xpath='//*[@id="left-big-scroll"]/div[2]/div/div[2]/div[2]/dl/dt'
Type_URL_Xpath='a/@href'
PageNum_Xpath='/html/head/script[5]/text()'
Image_Point_Xpath='//*[@id="live-list-contentbox"]/li'
Image_Xpath='a/span/img/@data-original'

class DouyuSpider(object):
	def __init__(self):
		self.time_limit=TIME_LIMIT
		self.url=DOUYU_BASE_URL
		self.base_url=BASE_URL
		self.types_xpath=Types_Xpath
		self.type_utl_xpath=Type_URL_Xpath
		self.pagenum_xpath=PageNum_Xpath
		self.image_point_xpath=Image_Point_Xpath
		self.image_xpath=Image_Xpath
		self.type_url_list=[]
		self.url_list=[]
		self.thread_list=[]
		self.rconn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db= REDIS_DB)  
		self.queue = REDIS_URL_LIST

	def getAllUrl(self):
		response=requests.get(self.url)
		selector=etree.HTML(response.content)
		allTypes=selector.xpath(self.types_xpath)
		for types in allTypes:
			self.type_url_list.append(self.base_url+types.xpath(self.type_utl_xpath)[0])

	def getAllRoom(self):
		for type_url in self.type_url_list:
			response=requests.get(type_url)
			selector=etree.HTML(response.content)
			pagenum=selector.xpath(self.pagenum_xpath)[0]
			pagenum=re.match(r'.*?count: "(\d+)".*?',pagenum[98:125]).group(1)
			for i in range(1,int(pagenum)+1):
				self.url_list.append(type_url+'?page='+str(i))
		for i in range(int(len(self.url_list)/10)+1):
			self.thread_list.append(threading.Thread(target=self.getImageUrl,args=(self.url_list[i*10:10*i+9])))
		for thread in self.thread_list:
			thread.start()
		for thread in self.thread_list:
			thread.join()	

	def getImageUrl(self,*page_url):
		print(page_url)
		for page in page_url:
			response=requests.get(page)
			selector=etree.HTML(response.content)
			allImages=selector.xpath(self.image_point_xpath)
			#处理所有Image
			for image in allImages:
				task_name=image.xpath("@data-rid")[0]
				task_url=image.xpath(self.image_xpath)[0]
				task=dict(name=task_name,url=task_url)
				self.rconn.lpush(self.queue,json.dumps(task))

	def run(self):
		while True:
			self.getAllUrl()
			self.getAllRoom()
			self.type_url_list.clear()
			self.url_list.clear()
			self.thread_list.clear()
			time.sleep(self.time_limit)

def start():
	# logging.basicConfig(level=logging.INFO,
 #                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
 #                datefmt='%a, %d %b %Y %H:%M:%S',
 #                filename='DouyuCrawler.log',
 #                filemode='w')
	# logging.info("DouyuSpider Working......")
	spider=DouyuSpider()
	spider.run()

if __name__=="__main__":
	print("model 1 work")
	spider=DouyuSpider()
	spider.run()
	

