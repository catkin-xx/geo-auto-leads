from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class LeadBase(BaseModel):
    """客户基础字段"""
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    industry: Optional[str] = None
    source: Optional[str] = None
    source_id: str
    source_url: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    rating: Optional[float] = 0
    review_count: Optional[int] = 0
    tags: Optional[list] = []
    comment_text: Optional[str] = None


class LeadCreate(LeadBase):
    """创建客户时使用"""
    pass


class LeadUpdate(BaseModel):
    """更新客户时使用（所有字段可选）"""
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    industry: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[int] = None
    notes: Optional[str] = None
    score: Optional[int] = None


class LeadOut(LeadBase):
    """返回客户数据时使用"""
    id: int
    score: int
    status: str
    assigned_to: Optional[int] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Pydantic v2