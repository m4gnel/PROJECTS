import asyncio
import sys
import uuid
from datetime import date
from sqlalchemy import select

sys.path.insert(0, ".")

from backend.database import AsyncSessionLocal
from backend.models.db import Base
from sqlalchemy import Column, String, Date, JSONB
from sqlalchemy.dialects.postgresql import UUID


class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(300), nullable=False)
    short_name = Column(String(50), nullable=True)
    authority = Column(String(200), nullable=True)
    authority_level = Column(String(20), nullable=True)
    state = Column(String(100), nullable=True)
    crops_applicable = Column(JSONB, nullable=True)
    eligibility_rules = Column(JSONB, nullable=False)
    benefits_json = Column(JSONB, nullable=True)
    enrollment_url = Column(String(500), nullable=True)
    helpline = Column(String(50), nullable=True)
    valid_from = Column(Date, nullable=True)
    valid_until = Column(Date, nullable=False)
    status = Column(String(20), default="active")


async def seed():
    async with AsyncSessionLocal() as session:
        schemes_data = [
            {
                "name": "Pradhan Mantri Fasal Bima Yojana",
                "short_name": "PMFBY",
                "authority": "Ministry of Agriculture",
                "authority_level": "central",
                "state": None,
                "crops_applicable": ["rice", "maize", "tomato", "banana"],
                "eligibility_rules": {
                    "land_ownership": ["owner", "tenant"],
                    "aadhaar_required": True,
                    "enrollment_window_days_after_sowing": 30
                },
                "benefits_json": {"premium_kharif_pct": 2.0, "premium_rabi_pct": 1.5, "coverage": "yield loss"},
                "enrollment_url": "https://pmfby.gov.in",
                "valid_until": date(2027, 3, 31),
                "status": "active"
            },
            {
                "name": "Pradhan Mantri Kisan Samman Nidhi",
                "short_name": "PM-KISAN",
                "authority": "Ministry of Agriculture",
                "authority_level": "central",
                "state": None,
                "crops_applicable": None,
                "eligibility_rules": {
                    "land_ha_max": 2,
                    "not_income_taxpayer": True,
                    "not_government_employee": True
                },
                "benefits_json": {"annual_amount_inr": 6000, "installments": 3},
                "enrollment_url": "https://pmkisan.gov.in",
                "valid_until": date(2028, 3, 31),
                "status": "active"
            },
            {
                "name": "Kerala Karshaka Kshemanidhi",
                "short_name": "KSHEMANIDHI",
                "authority": "Kerala Agriculture Department",
                "authority_level": "state",
                "state": "Kerala",
                "crops_applicable": ["rice", "banana", "coconut", "tomato", "maize"],
                "eligibility_rules": {
                    "state": "Kerala",
                    "registered_farmer": True
                },
                "benefits_json": {"pension_monthly_inr": 1000},
                "enrollment_url": "https://karshakakshemanidhi.kerala.gov.in",
                "valid_until": date(2027, 3, 31),
                "status": "active"
            }
        ]

        for sdata in schemes_data:
            stmt = select(Scheme).where(Scheme.name == sdata["name"])
            res = await session.execute(stmt)
            existing = res.scalars().first()
            if not existing:
                s = Scheme(**sdata)
                session.add(s)
                print(f"Seeded scheme: {sdata['short_name']}")

        await session.commit()
        print("Seeding completed successfully.")

if __name__ == "__main__":
    asyncio.run(seed())
