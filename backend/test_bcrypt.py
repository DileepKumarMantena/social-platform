from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed = "$2b$12$i2/jGHEcj/JiGt.YTvWFNuz/jAUFlKEj4QiaU9xyplMwbBMapSXGC"

print("Password match result:", pwd_context.verify("password", hashed))