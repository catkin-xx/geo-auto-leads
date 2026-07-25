from celery import Celery
from app.core.config import settings

# 创建 Celery 实例
celery_app = Celery(
    "geo_auto_leads",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# 配置
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 单个任务最长30分钟
)


@celery_app.task(name="trigger_outreach")
def trigger_outreach(lead_id: int):
    """
    自动触达任务：
    根据客户来源和偏好，选择合适的渠道进行首次联系
    """
    # 这里先打印日志，实际使用时会调用企微/短信API
    print(f"[自动触达] 开始处理客户 ID: {lead_id}")
    
    # TODO: 实际项目中的步骤
    # 1. 从数据库获取客户信息
    # 2. 判断触达渠道（企微 > 短信 > 平台私信）
    # 3. 调用对应API发送消息
    # 4. 更新客户状态和触达记录
    
    print(f"[自动触达] 客户 ID: {lead_id} 触达完成")
    return f"lead_{lead_id}_outreach_done"


@celery_app.task(name="batch_collect")
def batch_collect(city: str, industry: str):
    """
    批量采集任务：触发爬虫采集指定城市和行业的数据
    """
    print(f"[批量采集] 开始采集 {city} - {industry}")
    # TODO: 调用 Scrapy 或发送指令给爬虫服务
    return f"collect_{city}_{industry}_started"


@celery_app.task(name="monitor_comments")
def monitor_comments(platform: str, keywords: list):
    """
    监控评论区任务：定时搜索相关视频/笔记的评论区
    """
    print(f"[评论监控] 开始监控 {platform}，关键词：{keywords}")
    # TODO: 触发评论监控爬虫
    return f"monitor_{platform}_started"