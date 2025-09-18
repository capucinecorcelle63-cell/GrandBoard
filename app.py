
from app import create_app
app = create_app()

"""Application factory for the Flask project (migrated to new structure)."""
from app import create_app

app = create_app()

    # build month list (months where entries exist)
    months = (
        db.session.query(Entry.created_at)
        .order_by(Entry.created_at.desc())
        .all()
    )
    # extract unique months in format YYYY-MM
    month_set = []
    for (dt,) in months:
        key = dt.strftime("%Y-%m")
        if key not in month_set:
            month_set.append(key)

    # if no month param, take latest month or current month
    if not month:
        month = month_set[0] if month_set else datetime.utcnow().strftime("%Y-%m")

    year, mon = map(int, month.split("-"))
        month = month_set[0] if month_set else datetime.utcnow().strftime("%Y-%m")
exit()
