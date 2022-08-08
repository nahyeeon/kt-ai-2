import scrapy
import pandas as pd
from naverexchange.items import NaverexchangeItem

class naverSpider(scrapy.Spider):
    
    name= 'naverSpider'
    
    def start_requests(self):
        page, pagesize = 1, 60
        url = f'https://api.stock.naver.com/marketindex/exchange/FX_USDKRW/prices?page={page}&pageSize={pagesize}'
        
    
        yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        data = response.json()
        df = pd.DataFrame(data)[['localTradedAt','closePrice']]
        #print(df)
        
        for i in range(len(df)):
            item = NaverexchangeItem()
            #print(df.loc[i]['localTradedAt'])
            #print(df.loc[i]['closePrice'])
            item['localTradedAt'] = df.loc[i]['localTradedAt']
            item['closePrice'] = df.loc[i]['closePrice']
            yield item