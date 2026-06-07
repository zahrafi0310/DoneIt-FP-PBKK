from database import SessionLocal
from models import User
from auth import hash_password

USERNAME = "admin"
EMAIL    = "admin@doneit.com"
PASSWORD = "admingacorautoA"

db = SessionLocal()

if db.query(User).filter(User.username == USERNAME).first():
    print(f"Admin '{USERNAME}' sudah ada.")
else:
    admin = User(
        username=USERNAME,
        email=EMAIL,
        hashed_password=hash_password(PASSWORD),
        is_admin=True,
        xp=None,   
        level=None, 
    )
    db.add(admin)
    db.commit()
    print(f"Admin '{USERNAME}' berhasil dibuat!")

db.close()