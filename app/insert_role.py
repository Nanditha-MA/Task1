from app.database import SessionLocal
from app.models import Role

db = SessionLocal()

role = Role(
    id="11111111-1111-1111-1111-111111111111",
    name="admin"
)

db.add(role)
db.commit()
db.close()

print("Role inserted successfully")
