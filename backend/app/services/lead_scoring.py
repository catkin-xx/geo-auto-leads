def score_lead(lead):
    """
    根据客户特征计算GEO需求评分（0-100）
    分数越高，越需要地图优化服务
    """
    score = 0
    tags = lead.tags or []
    
    # 新店铺（注册时间短）
    if "new_shop" in tags:
        score += 30
    
    # 没有小程序/官网
    if "no_miniapp" in tags:
        score += 20
    
    # 没有企业微信
    if "no_wecom" in tags:
        score += 15
    
    # 平台评分低
    if lead.rating and lead.rating < 3.5:
        score += 20
    
    # 评价数量少（说明线上经营弱）
    if lead.review_count is not None and lead.review_count < 10:
        score += 10
    
    # 评论区主动询问GEO（极高意向）
    if lead.source and "comment" in lead.source:
        score += 40
    
    # 竞争对手多（同区域同行业商家多）
    if "high_competition" in tags:
        score += 15
    
    # 没有在美团/点评上运营
    if "no_meituan" in tags:
        score += 20
    
    # 确保不超过100
    return min(score, 100)