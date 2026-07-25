import scrapy
import json
from urllib.parse import quote


class AmapSpider(scrapy.Spider):
    """
    高德地图 POI 采集爬虫
    """
    name = "amap"
    allowed_domains = ["restapi.amap.com"]
    
    def __init__(self, keyword="家电维修", city="南京", api_key=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.city = city
        self.api_key = api_key or "YOUR_AMAP_KEY"
        self.base_url = "https://restapi.amap.com/v3/place/text"
        self.current_page = 1
    
    def start_requests(self):
        params = {
            "key": self.api_key,
            "keywords": self.keyword,
            "city": self.city,
            "offset": 20,
            "page": self.current_page,
            "extensions": "all"
        }
        url = f"{self.base_url}?{'&'.join([f'{k}={quote(str(v))}' for k, v in params.items()])}"
        yield scrapy.Request(url, callback=self.parse, meta={"page": 1})
    
    def parse(self, response):
        data = json.loads(response.text)
        
        if data.get("status") != "1":
            self.logger.error(f"API请求失败: {data}")
            return
        
        pois = data.get("pois", [])
        for poi in pois:
            location = poi.get("location", "0,0").split(",")
            yield {
                "name": poi.get("name", ""),
                "phone": poi.get("tel", "") or poi.get("biz_ext", {}).get("tel", ""),
                "address": poi.get("address", ""),
                "city": poi.get("cityname", self.city),
                "district": poi.get("adname", ""),
                "industry": poi.get("type", self.keyword).split(";")[0] if poi.get("type") else self.keyword,
                "source": "amap",
                "source_id": poi.get("id", ""),
                "lat": float(location[0]) if len(location) > 1 else None,
                "lng": float(location[1]) if len(location) > 1 else None,
                "rating": float(poi.get("biz_ext", {}).get("rating", 0) or 0),
                "tags": self._extract_tags(poi),
            }
        
        # 翻页
        total_count = int(data.get("count", 0))
        if total_count > self.current_page * 20:
            self.current_page += 1
            params = {
                "key": self.api_key,
                "keywords": self.keyword,
                "city": self.city,
                "offset": 20,
                "page": self.current_page,
                "extensions": "all"
            }
            url = f"{self.base_url}?{'&'.join([f'{k}={quote(str(v))}' for k, v in params.items()])}"
            yield scrapy.Request(url, callback=self.parse, meta={"page": self.current_page})
    
    def _extract_tags(self, poi):
        """根据POI信息自动打标签"""
        tags = []
        biz_ext = poi.get("biz_ext", {})
        
        # 判断是否新店（根据照片数量推测）
        photos = poi.get("photos", [])
        if len(photos) < 3:
            tags.append("new_shop")
        
        # 判断评分
        rating = float(biz_ext.get("rating", 0) or 0)
        if 0 < rating < 3.5:
            tags.append("poor_rating")
        
        # 判断是否有联系方式
        if not poi.get("tel") and not biz_ext.get("tel"):
            tags.append("no_phone")
        
        return tags