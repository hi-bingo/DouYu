import urllib.request ,threading,os,json,redis,logging
from setting import *

class download(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.rconn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db= REDIS_DB)  
		self.down_queue = REDIS_DOWN_LIST
	def run(self):
		while True:
			task = self.rconn.brpop(self.down_queue, 0)[1].decode('utf-8')
			down_waited=json.loads(task)                            
			image_url=down_waited['url']  
			folder_name=down_waited['name']  							#所在文件夹名
			fileName=image_url.split('/').pop()							#文件名
			save_path=SAVE_PATH
			if  SAVE_PATH.strip()=='':  								#默认为当前路径
				save_path=os.path.abspath('.')
			absolute_path=os.path.join(save_path,folder_name)
			if not os.path.exists(absolute_path):  
			    os.makedirs(absolute_path)   
			urllib.request.urlretrieve(image_url,absolute_path+os.sep+fileName) 

def startDown(threadNum=DOWN_THREAD_NUM):
	# logging.basicConfig(level=logging.INFO,
 #                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
 #                datefmt='%a, %d %b %Y %H:%M:%S',
 #                filename='downimage.log',
 #                filemode='w')
	# logging.info('DownImage Working......')
	for i in range(threadNum):
		d=download()
		d.start()

# if __name__=='__main__':
# 	print("model 3 work")
# 	startDown(THREAD_NUM)
