from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import leads
from app.models.lead import Base
from app.core.database import engine
from app.core.config import settings

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境要限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(leads.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    return {"message": "GEO Auto Leads API", "version": settings.VERSION}


@app.get("/health")
def health_check():
    return {"status": "healthy"}