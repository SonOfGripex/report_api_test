import asyncio
from typing import List, Optional
from datetime import datetime, timedelta, UTC
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.complaint.schemas import ComplaintResponse, ComplaintCreate, ComplaintBackendResponse
from app.complaint.models import Complaint
from app.database.connection import get_db
from app.services.sentiment_analysis import get_sentiment_analyse
from app.services.spamcheck import is_spam
from app.services.ipcheck import get_ip_info
from app.services.classify_complaint import classify
from app.services.auth import auth_bearer


complaint_router = APIRouter(prefix="/complaint", tags=["Complaints"])


@complaint_router.get('/', response_model=List[ComplaintBackendResponse])
async def get_complaints(
    db: AsyncSession = Depends(get_db),
    _auth: bool = Depends(auth_bearer),
    status_filter: Optional[str] = Query(
        None,
        description="Фильтр по статусу (open/closed)",
    ),
    hours: int = Query(
        1,
        ge=1, le=24,
        description="За сколько часов назад смотреть (1-24)",
    ),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    query = select(Complaint)

    if status_filter:
        query = query.where(Complaint.status == status_filter)

    if hours is not None:
        since_dt = datetime.now(UTC) - timedelta(hours=hours)
        query = query.where(Complaint.timestamp >= since_dt)

    query = (
        query.order_by(Complaint.timestamp.desc())
            .offset(offset)
            .limit(limit)
    )

    result = await db.execute(query)
    complaints = result.scalars().all()
    return complaints


@complaint_router.post('/', response_model=ComplaintResponse, status_code=201)
async def create_complaint(request: Request, payload: ComplaintCreate, db: AsyncSession = Depends(get_db)):
    try:
        if await is_spam(payload.text):
            raise HTTPException(status_code=422, detail='spam')

        complaint = Complaint(text=payload.text)
        db.add(complaint)
        await db.commit()
        await db.refresh(complaint)

        sentiment_task = asyncio.create_task(get_sentiment_analyse(payload.text))
        ip_check_task = asyncio.create_task(get_ip_info(request.client.host))
        classify_complaint_task = asyncio.create_task(classify(payload.text))
        sentiment, ip_country, category = await asyncio.gather(sentiment_task, ip_check_task, classify_complaint_task)

        complaint.sentiment = sentiment
        complaint.ip_country = ip_country
        complaint.category = category
        await db.commit()
        await db.refresh(complaint)

        return complaint
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@complaint_router.patch("/{id}", status_code=200)
async def close_complaint(id: int, db: AsyncSession = Depends(get_db), _auth: bool = Depends(auth_bearer)):
    try:
        comp = await db.get(Complaint, id)
        if not comp:
            raise HTTPException(404)
        comp.status = "closed"
        await db.commit()
        return {"id": id, "status": "closed"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

