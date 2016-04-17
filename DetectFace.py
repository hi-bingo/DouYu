import redis,requests,json,threading,logging
from setting import *

DETECT_URL='http://apicn.faceplusplus.com/detection/detect'

class Detect(object):
	def __init__(self):
		self.detect_url=DETECT_URL
		self.form={'api_key':API_KEY,'api_secret':API_SECRET,'url':''}
		self.rconn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db= REDIS_DB)  
		self.url_queue = REDIS_URL_LIST
		self.down_queue = REDIS_DOWN_LIST
		self.thread_list=[]

	def detect(self):
		while True:
			task = self.rconn.brpop(self.url_queue, 0)[1].decode('utf-8')
			detect_waited=json.loads(task)
			self.form['url']=detect_waited['url']
			reponse=json.loads(requests.post(self.detect_url,params=self.form).content.decode('utf-8'))
			try:
				if len(reponse.get("face"))<1:              								#如果人脸数为0
					continue
				else:															
					self.rconn.lpush(self.down_queue,json.dumps(detect_waited))				#将该图片加入下载队列
			except:
				self.rconn.lpush(self.url_queue,json.dumps(detect_waited))					#若失败则重新加入待检测队列


	def run(self):
		for i in range(DETECT_THREAD_NUM):
			self.thread_list.append(threading.Thread(target=self.detect,name='detect_threading'+str(i)))
		for thread in self.thread_list:
			thread.start()
		for thread in self.thread_list:
			thread.join()
		self.thread_list.clear()

def start():
	# logging.basicConfig(level=logging.INFO,
 #                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
 #                datefmt='%a, %d %b %Y %H:%M:%S',
 #                filename='detectface.log',
 #                filemode='w')
	# logging.info('DetectFace Working......')
	detect=Detect()
	detect.run()

# if __name__=="__main__":
# 	print("model 2 work")
# 	detect=Detect()
# 	detect.run()
