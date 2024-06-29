from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer
import config

security = HTTPBearer()

def verify_token(credentials=Security(security)):
    if credentials.credentials != config.TOKEN: return None
