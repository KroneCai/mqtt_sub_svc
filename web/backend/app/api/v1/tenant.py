from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Null
from schemas.tenant import Tenant as TenantSchema
from crud.tenant import get_tenant_by_code, create_tenant,delete_tenant,update_tenant, get_tenants
from models.tenant import Tenant as TenantModel
from sqlalchemy.orm import Session
from db.db import Database
from loguru import logger

router = APIRouter()

def get_db():
    db = Database()
    engine = db.get_db_connection()
    session = db.get_db_session(engine)
    return session

sessionLocal = get_db()

@router.get("/tenants", response_model=list[TenantSchema])
async def get_tenant_list():
    db_tenants = get_tenants(db=sessionLocal)
    if db_tenants == []:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenants

@router.get("/tenant/{tenantCode}", response_model=TenantSchema)
async def get_tenant_with_code(tenantCode: str):
    db_tenant = get_tenant_by_code(db=sessionLocal, code=tenantCode)
    if db_tenant == []:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant[0]

@router.post("/tenant", response_model=TenantSchema)
async def post_tenant(tenant: TenantSchema):
    db_tenant = get_tenant_by_code(db=sessionLocal, code=tenant.code)
    if db_tenant != []:
        raise HTTPException(status_code=409, detail="Tenant already exists")
    create_tenant(sessionLocal, tenant)
    return TenantSchema.model_validate(tenant)

@router.put("/tenant", response_model=TenantSchema)
async def put_tenant(tenant: TenantSchema):
    db_tenant = get_tenant_by_code(db=sessionLocal, code=tenant.code)
    if db_tenant == []:
        raise HTTPException(status_code=404, detail="Tenant not found")
    update_tenant(db=sessionLocal, tenant=tenant)
    return TenantSchema.model_validate(tenant)

@router.delete("/tenant/{tenantCode}")
async def del_tenant(tenantCode: str):
    db_tenant = get_tenant_by_code(db=sessionLocal, code=tenantCode)
    if db_tenant is []:
        raise HTTPException(status_code=404, detail="Tenant not found")
    delete_tenant(db=sessionLocal, code=tenantCode)
    return {"message": "Tenant deleted successfully"}
