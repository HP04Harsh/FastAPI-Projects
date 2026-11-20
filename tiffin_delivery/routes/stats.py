from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func
from datetime import date, datetime, time
from database import get_session
from models import Order, OrderStatus

router = APIRouter(prefix="/stats", tags=["Analytics"])

@router.get("/daily")
def get_daily_summary(
    summary_date: date | None = Query(None, description="Date for summary (defaults to today)"),
    session: Session = Depends(get_session)
):
    # 1. Default to today's date if not provided
    target_date = summary_date or date.today()

    # 2. Calculate Start (00:00:00) and End (23:59:59) boundaries
    start_time = datetime.combine(target_date, time.min)
    end_time = datetime.combine(target_date, time.max)

    by_status = {}
    total_orders = 0

    # 3. Loop through Enum values to count occurrences per status
    for status in OrderStatus:
        statement = select(func.count(Order.id)).where(
            Order.created_at >= start_time,
            Order.created_at <= end_time,
            Order.status == status
        )
        count = session.exec(statement).one()
        by_status[status.value] = count
        total_orders += count

    # 4. Return formatted summary payload
    return {
        "date": target_date.isoformat(),
        "total_orders": total_orders,
        "by_status": by_status
    }