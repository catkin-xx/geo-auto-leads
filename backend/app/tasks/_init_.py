from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Lead(Base):
    """
    潜在客户数据模型
    """
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # 基本信息
    name = Column(String(255), index=True, comment="店铺/公司名称")
    phone = Column(String(20), index=True, nullable=True, comment="联系电话")
    address = Column(String(500), comment="详细地址")
    city = Column(String(50), index=True, comment="城市")
    district = Column(String(50), nullable=True, comment="区县")
    
    # 行业分类
    industry = Column(String(50), index=True, comment="行业（家电维修/开锁/家政等）")
    
    # 来源信息
    source = Column(String(50), comment="来源平台（amap/meituan/douyin/douyin_comment等）")
    source_id = Column(String(100), unique=True, comment="来源平台唯一ID，用于去重")
    source_url = Column(String(500), nullable=True, comment="来源链接")
    
    # 地理位置
    lat = Column(Float, nullable=True, comment="纬度")
    lng = Column(Float, nullable=True, comment="经度")
    
    # 平台评分
    rating = Column(Float, default=0, comment="平台评分")
    review_count = Column(Integer, default=0, comment="评价数量")
    
    # 标签（JSON数组）
    tags = Column(JSON, default=[], comment="特征标签（new_shop/no_website/poor_rating等）")
    
    # 系统评分（GEO需求度）
    score = Column(Integer, default=0, comment="GEO需求评分（0-100）")
    
    # 客户状态
    status = Column(String(20), default="new", comment="状态：new/contacting/interested/negotiating/deal/invalid")
    
    # 分配信息
    assigned_to = Column(Integer, nullable=True, comment="分配的销售/运营人员ID")
    
    # 备注
    notes = Column(Text, nullable=True, comment="备注信息")
    comment_text = Column(Text, nullable=True, comment="如果是评论区抓取，保存原文")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, comment="更新时间")
    
    # 是否删除（软删除）
    is_deleted = Column(Boolean, default=False, comment="是否已删除")


class User(Base):
    """
    系统用户（销售人员/管理员）
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(255))
    role = Column(String(20), default="sales")  # admin / sales
    city = Column(String(50), nullable=True)  # 负责的城市
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)