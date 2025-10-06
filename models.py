"""
Pydantic models for Repair Tracker API
"""
from datetime import date as Date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from enum import Enum

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class RepairStatus(str, Enum):
    PLANNED = "PLANNED"
    COMPLETED = "COMPLETED"

# User models
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Asset models
class AssetBase(BaseModel):
    name: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1)

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    type: Optional[str] = Field(None, min_length=1)

class AssetResponse(AssetBase):
    id: int
    owner_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AssetWithRepairs(AssetResponse):
    repairs: List['RepairResponse'] = []

# Repair models
class RepairBase(BaseModel):
    property_id: int
    date: Date
    description: str = Field(..., min_length=1)
    performed_by: str = Field(..., min_length=1)
    notes: Optional[str] = None
    cost_cents: int = Field(0, ge=0)
    status: RepairStatus = RepairStatus.COMPLETED
    
    @field_validator('date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            from datetime import datetime
            # Try different date formats
            date_formats = [
                '%Y-%m-%d',      # 2024-01-15
                '%d.%m.%Y',      # 15.01.2024
                '%d/%m/%Y',      # 15/01/2024
                '%d-%m-%Y',      # 15-01-2024
                '%m/%d/%Y',      # 01/15/2024 (US format)
                '%Y.%m.%d',      # 2024.01.15
            ]
            
            for date_format in date_formats:
                try:
                    return datetime.strptime(v, date_format).date()
                except ValueError:
                    continue
            
            raise ValueError(f"Invalid date format. Supported formats: YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY, MM/DD/YYYY, YYYY.MM.DD. Got: {v}")
        return v

class RepairCreate(RepairBase):
    pass

class RepairUpdate(BaseModel):
    property_id: Optional[int] = None
    date: Optional[str] = Field(None, description="Date in YYYY-MM-DD format")
    description: Optional[str] = Field(None, min_length=1)
    performed_by: Optional[str] = Field(None, min_length=1)
    notes: Optional[str] = None
    cost_cents: Optional[int] = Field(None, ge=0)
    status: Optional[RepairStatus] = None

class RepairResponse(RepairBase):
    id: int
    created_by_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RepairWithAsset(RepairResponse):
    asset: Optional[AssetResponse] = None

# Filter models
class RepairFilter(BaseModel):
    property_id: Optional[int] = None
    status: Optional[RepairStatus] = None
    year: Optional[int] = None
    sort_by: Optional[str] = Field(None, pattern="^(date|asset)$")
    sort_order: Optional[str] = Field(None, pattern="^(asc|desc)$")

class AssetFilter(BaseModel):
    owner_id: Optional[int] = None
    type: Optional[str] = None
    search: Optional[str] = None

# Profile models
class UserProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None

class PasswordChange(BaseModel):
    current_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)

class UserSettings(BaseModel):
    currency: str = Field("USD", pattern="^(USD|EUR|RUB|GBP|JPY)$")
    language: str = Field("en", pattern="^(en|ru|de|fr|es)$")
    date_format: str = Field("DD.MM.YYYY", pattern="^(DD.MM.YYYY|MM/DD/YYYY|YYYY-MM-DD)$")
    theme: str = Field("dark", pattern="^(dark|light)$")

class UserSettingsResponse(UserSettings):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Token models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Import models
class ImportResult(BaseModel):
    total_rows: int
    successful_imports: int
    failed_imports: int
    errors: List[str] = []

class AssetImportRow(BaseModel):
    name: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1)
    
    @field_validator('name', 'type')
    @classmethod
    def validate_not_empty(cls, v):
        if not v or v.strip() == '':
            raise ValueError('Field cannot be empty')
        return v.strip()

class RepairImportRow(BaseModel):
    asset_name: str = Field(..., min_length=1)
    date: Date = Field(..., description="Date in YYYY-MM-DD format")
    description: str = Field(..., min_length=1)
    performed_by: str = Field(..., min_length=1)
    notes: Optional[str] = None
    cost_cents: int = Field(0, ge=0)
    status: str = Field("COMPLETED", pattern="^(PLANNED|COMPLETED)$")
    
    @field_validator('asset_name', 'description', 'performed_by')
    @classmethod
    def validate_not_empty(cls, v):
        if not v or v.strip() == '':
            raise ValueError('Field cannot be empty')
        return v.strip()
    
    @field_validator('date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            from datetime import datetime
            # Try different date formats
            date_formats = [
                '%Y-%m-%d',      # 2024-01-15
                '%d.%m.%Y',      # 15.01.2024
                '%d/%m/%Y',      # 15/01/2024
                '%d-%m-%Y',      # 15-01-2024
                '%m/%d/%Y',      # 01/15/2024 (US format)
                '%Y.%m.%d',      # 2024.01.15
            ]
            
            for date_format in date_formats:
                try:
                    return datetime.strptime(v, date_format).date()
                except ValueError:
                    continue
            
            raise ValueError(f"Invalid date format. Supported formats: YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY, MM/DD/YYYY, YYYY.MM.DD. Got: {v}")
        return v
    
    @field_validator('cost_cents', mode='before')
    @classmethod
    def parse_cost(cls, v):
        if isinstance(v, str):
            # Remove currency symbols and whitespace
            v = v.strip().replace('$', '').replace('€', '').replace('₽', '').replace('£', '').replace('¥', '')
            try:
                # Try to parse as float first (for decimal amounts like 643.36)
                amount = float(v)
                # Convert to cents (multiply by 100 and round)
                return int(round(amount * 100))
            except ValueError:
                raise ValueError(f"Invalid cost format. Expected a number (e.g., 643.36 or 64336). Got: {v}")
        elif isinstance(v, (int, float)):
            # If it's already a number, convert to cents if it looks like dollars
            if v < 10000 and v > 0:  # Likely dollars if under 10000
                return int(round(float(v) * 100))
            else:  # Likely already in cents
                return int(v)
        return v

# Update forward references
AssetWithRepairs.model_rebuild()
RepairWithAsset.model_rebuild()

