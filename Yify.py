import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from scrapy.crawler import CrawlerProcess
dict = {
	# 'BOT_NAME' : 'hyper_scraping',
	# 'SPIDER_MODULES' : ['hyper_scraping.spiders'],
	# 'NEWSPIDER_MODULE' : 'hyper_scraping.spiders',
	'ROBOTSTXT_OBEY' : False,
	'DOWNLOADER_MIDDLEWARES' : {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,},

	}
class Yify(scrapy.Spider):
	name = 'Hollywood'
	t=''
	x = 'Avengers'
	p=x.split(' ')
	list=[]
	for i in range(len(p)):
		if i != (len(p)-1) :
			temp=p[i]+'%20'
			list.append(temp)
		else:
 			list.append(p[i])
# print(p,list)
	x=''.join(list)
	naam = []	
	url  = 'https://yts.mx/browse-movies/'+x+'/all/all/0/latest/0/all'
	start_urls = [url,
				 ]
	def parse(self,response):
		# open_in_browser(response)
		name = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "browse-movie-title", " " ))]/text()').extract()	
		links = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "browse-movie-title", " " ))]/@href').extract()	
		yield {'name':name,'links':links}
		# x=int(input('Please select the total movies are '+str(len(links))+' :  '))
		x=1
		yield response.follow(links[x],callback=self.endgame)
	def endgame(self,response):
			# open_in_browser(response)
			torrent_links = response.xpath('//*[(@id = "movie-info")]//*[contains(concat( " ", @class, " " ), concat( " ", "hidden-sm", " " ))]//a/@href').extract()
			Quality = response.xpath('//*[(@id = "movie-info")]//*[contains(concat( " ", @class, " " ), concat( " ", "hidden-sm", " " ))]//a/text()').extract()
			# subtitle = 	response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "hidden-sm", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "button", " " ))]/@href').extract_first()
			yield {'Quality':Quality}
			yield {'torrent_links':torrent_links}
			# yield {'subtitle':subtitle}
process = CrawlerProcess(settings=dict)	
process.crawl(Yify)
process.start()	