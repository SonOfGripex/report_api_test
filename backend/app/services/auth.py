from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.settings import settings


security = HTTPBearer(auto_error=False)

async def auth_bearer(
    creds: HTTPAuthorizationCredentials | None = Depends(security),
):
    if creds is None or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Not authenticated")

    if creds.credentials != settings.secret_token:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    return True