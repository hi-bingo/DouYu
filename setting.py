REDIS_HOST='localhost'		 #redis相关配置
REDIS_PORT='6379'
REDIS_DB='1'
REDIS_URL_LIST='url_list'	 #待检测队列
REDIS_DOWN_LIST='down_list'  #待下载队列
TIME_LIMIT=600               #1爬取频率：10分钟
SAVE_PATH='' 				 #存储的总目录

DOWN_THREAD_NUM=10 				#下载的线程数
DETECT_THREAD_NUM=3				#检测线程数
