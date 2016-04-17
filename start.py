from multiprocessing import Pool
import os
import DouYuCrawler
import DetectFace
import DownImage


if __name__=="__main__":
	p = Pool(4)
	p.apply_async(DouYuCrawler.start)
	p.apply_async(DetectFace.start)
	p.apply_async(DownImage.startDown)
	
	p.close()
	p.join()
	print('All subprocesses done.')
