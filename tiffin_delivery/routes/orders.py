from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import date, datetime, time, timezone
from database import get_session
from models import Order, OrderCreate, OrderUpdate, OrderStatus, StatusLog

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=Order)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    db_order = Order.model_validate(order)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.get("/", response_model=list[Order])
def list_orders(
    status: OrderStatus | None = Query(None, description="Filter by status"),
    created_date: date | None = Query(None, description="Filter by YYYY-MM-DD"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session)
):
    query = select(Order)

    # Filter 1: Status
    if status:
        query = query.where(Order.status == status)

    # Filter 2: Date Range (Full Day 00:00 to 23:59)
    if created_date:
        start_datetime = datetime.combine(created_date, time.min)
        end_datetime = datetime.combine(created_date, time.max)
        query = query.where(
            Order.created_at >= start_datetime,
            Order.created_at <= end_datetime
        )

    # Pagination: Offset & Limit
    query = query.offset(skip).limit(limit)
    return session.exec(query).all()


@router.patch("/{order_id}", response_model=StatusLog)
def update_order_status(
    order_id: int,
    order_update: OrderUpdate,
    session: Session = Depends(get_session)
):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    old_status = db_order.status
    update_data = order_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_order, key, value)

    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    return StatusLog(
        order_id=db_order.id,
        old_status=old_status,
        new_status=db_order.status,
        changed_at=datetime.now(timezone.utc)
    )