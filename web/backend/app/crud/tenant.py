from sqlalchemy.orm import Session
from loguru import logger
from models.tenant import Tenant
from datetime import datetime

def get_tenant_by_code(db: Session, code: str):
    # logger.info(f"get_tenant_by_code code: {code}")
    result = db.query(Tenant).filter(Tenant.code == code).order_by(Tenant.create_time.desc()).all()
    return result

def get_tenants(db: Session):
    # logger.info(f"get_tenants")
    return db.query(Tenant).order_by(Tenant.create_time.desc()).all()

def create_tenant(db: Session, tenant: Tenant):
    # logger.info(f"create_tenant tenant: {tenant}")
    tenant_orm = Tenant(**tenant.model_dump())
    db.add(tenant_orm)
    db.commit()
    db.refresh(tenant_orm)
    return tenant_orm

def update_tenant(db: Session, tenant: Tenant):
    tenant_orm = db.query(Tenant).filter(Tenant.code == tenant.code).first()
    if tenant_orm == []:
        return []
    tenant_orm.name = tenant.name
    tenant_orm.description = tenant.description
    tenant_orm.account = tenant.account
    tenant_orm.update_time = datetime.now()

    db.commit()
    db.refresh(tenant_orm)
    return tenant_orm

def delete_tenant(db: Session, code: str):
    # logger.info(f"delete_tenant tenant: {tenant}")
    result = db.query(Tenant).filter(Tenant.code == code).delete()
    if result == 0:
        return 0
    db.commit()
