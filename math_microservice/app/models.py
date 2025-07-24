from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PowRequest(BaseModel):
    base: float
    exponent: float

class PowResponse(BaseModel):
    result: float

class FibonacciRequest(BaseModel):
    n: int = Field(..., ge=0)

class FibonacciResponse(BaseModel):
    result: int

class FactorialRequest(BaseModel):
    n: int = Field(..., ge=0)

class FactorialResponse(BaseModel):
    result: int

class OperationRecord(BaseModel):
    id: Optional[int]
    operation: str
    input_data: str
    result: str
    timestamp: datetime

class GcdRequest(BaseModel):
    a: int
    b: int

class GcdResponse(BaseModel):
    result: int

class IsPrimeRequest(BaseModel):
    n: int = Field(..., ge=0)

class IsPrimeResponse(BaseModel):
    result: bool
