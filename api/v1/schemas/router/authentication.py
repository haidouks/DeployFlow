from pydantic import BaseModel, Field

class Authencation_Failed_Response(BaseModel):
    detail: str = Field(..., description="Detail about authentication or authorization failure", example="LDAP Connection Error: invalidCredentials")