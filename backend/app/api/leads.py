from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.models.lead import Lead
from app.schemas.lead import LeadOut, LeadUpdate, LeadCreate
from app.core.database import get_db
from app.services.lead_scoring import score_lead
from app.tasks.celery_app import trigger_outreach

router = APIRouter(prefix="/leads", tags=["leads"])

# ==================== 获取客户列表 ====================
@router.get("/", response_model=List[LeadOut])
def list_leads(
    city: str = Query(None, description="城市"),
    industry: str = Query(None, description="行业"),
    status: str = Query(None, description="状态"),
    min_score: int = Query(0, description="最低评分"),
    skip: int = Query(0, description="跳过条数"),
    limit: int = Query(20, description="返回条数"),
    db: Session = Depends(get_db)
):
    """
    查询潜在客户列表，支持按城市、行业、状态、评分筛选
    """
    query = db.query(Lead)
    if city:
        query = query.filter(Lead.city == city)
    if industry:
        query = query.filter(Lead.industry == industry)
    if status:
        query = query.filter(Lead.status == status)
    if min_score:
        query = query.filter(Lead.score >= min_score)
    return query.offset(skip).limit(limit).all()


# ==================== 新增客户（采集器推送） ====================
@router.post("/ingest", response_model=LeadOut)
def ingest_lead(lead_data: LeadCreate, db: Session = Depends(get_db)):
    """
    接收爬虫推送的新客户，自动去重并评分
    """
    # 检查是否已存在（按 source_id 去重）
    existing = db.query(Lead).filter(Lead.source_id == lead_data.source_id).first()
    if existing:
        # 已存在就更新信息
        for key, value in lead_data.dict(exclude_unset=True).items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing
    
    # 新建客户
    lead = Lead(**lead_data.dict())
    lead.score = score_lead(lead)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


# ==================== 更新客户信息 ====================
@router.patch("/{lead_id}", response_model=LeadOut)
def update_lead(lead_id: int, lead_data: LeadUpdate, db: Session = Depends(get_db)):
    """
    更新客户信息（状态、分配销售等）
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="客户不存在")
    for key, value in lead_data.dict(exclude_unset=True).items():
        setattr(lead, key, value)
    db.commit()
    db.refresh(lead)
    return lead


# ==================== 分配客户给销售 ====================
@router.patch("/{lead_id}/assign")
def assign_lead(lead_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    将客户分配给指定的销售人员
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="客户不存在")
    lead.assigned_to = user_id
    lead.status = "assigned"
    db.commit()
    return {"ok": True, "message": f"客户 {lead.name} 已分配给用户 {user_id}"}


# ==================== 批量评分 ====================
@router.post("/batch-score")
def batch_score(db: Session = Depends(get_db)):
    """
    对所有新客户重新计算评分
    """
    leads = db.query(Lead).filter(Lead.status == "new").all()
    count = 0
    for lead in leads:
        lead.score = score_lead(lead)
        count += 1
    db.commit()
    return {"scored": count, "message": f"已为 {count} 个客户重新评分"}


# ==================== 批量触达 ====================
@router.post("/batch-outreach")
def batch_outreach(lead_ids: List[int], db: Session = Depends(get_db)):
    """
    对指定客户执行自动触达（异步任务）
    """
    leads = db.query(Lead).filter(Lead.id.in_(lead_ids)).all()
    queued = 0
    for lead in leads:
        trigger_outreach.delay(lead.id)
        lead.status = "contacting"
        queued += 1
    db.commit()
    return {"queued": queued, "message": f"已提交 {queued} 个触达任务到队列"}


# ==================== 获取单个客户详情 ====================
@router.get("/{lead_id}", response_model=LeadOut)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    """
    获取单个客户的详细信息
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="客户不存在")
    return lead


# ==================== 删除客户 ====================
@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    """
    删除客户记录
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="客户不存在")
    db.delete(lead)
    db.commit()
    return {"ok": True, "message": f"客户已删除"}