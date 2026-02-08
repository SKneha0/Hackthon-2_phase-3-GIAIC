from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MedicalRecordCreate(BaseModel):
    """Schema for creating a new medical record"""
    title: str = Field(..., min_length=1, max_length=255, description="Title of the medical record")
    description: Optional[str] = Field(default=None, max_length=2000, description="Detailed description of the record")
    record_type: str = Field(..., max_length=100, description="Type of medical record (e.g., lab_result, prescription)")
    date_of_record: datetime = Field(default_factory=datetime.utcnow, description="Date when the record was created")
    doctor_name: Optional[str] = Field(default=None, max_length=255, description="Name of the doctor who created the record")
    medical_institution: Optional[str] = Field(default=None, max_length=255, description="Medical institution where record was created")
    file_url: Optional[str] = Field(default=None, max_length=500, description="URL to stored document")


class MedicalRecordUpdate(BaseModel):
    """Schema for updating an existing medical record"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255, description="Updated title")
    description: Optional[str] = Field(default=None, max_length=2000, description="Updated description")
    record_type: Optional[str] = Field(default=None, max_length=100, description="Updated record type")
    date_of_record: Optional[datetime] = Field(default=None, description="Updated date of record")
    doctor_name: Optional[str] = Field(default=None, max_length=255, description="Updated doctor name")
    medical_institution: Optional[str] = Field(default=None, max_length=255, description="Updated medical institution")
    file_url: Optional[str] = Field(default=None, max_length=500, description="Updated file URL")


class MedicalRecordResponse(BaseModel):
    """Schema for returning medical record data"""
    id: int
    title: str
    description: Optional[str]
    record_type: str
    date_of_record: datetime
    doctor_name: Optional[str]
    medical_institution: Optional[str]
    file_url: Optional[str]
    user_id: int
    created_at: datetime
    updated_at: datetime


class VitalSignsCreate(BaseModel):
    """Schema for creating vital signs record"""
    heart_rate: Optional[int] = Field(default=None, ge=0, le=300, description="Heart rate in beats per minute")
    blood_pressure_systolic: Optional[int] = Field(default=None, ge=0, le=300, description="Systolic blood pressure")
    blood_pressure_diastolic: Optional[int] = Field(default=None, ge=0, le=200, description="Diastolic blood pressure")
    temperature: Optional[float] = Field(default=None, ge=30.0, le=50.0, description="Body temperature in Celsius")
    oxygen_saturation: Optional[int] = Field(default=None, ge=0, le=100, description="Oxygen saturation percentage")
    respiratory_rate: Optional[int] = Field(default=None, ge=0, le=100, description="Respiratory rate per minute")
    weight_kg: Optional[float] = Field(default=None, ge=0.0, description="Weight in kilograms")
    height_cm: Optional[float] = Field(default=None, ge=0.0, description="Height in centimeters")
    bmi: Optional[float] = Field(default=None, ge=0.0, description="Body Mass Index")
    notes: Optional[str] = Field(default=None, max_length=1000, description="Additional notes")


class VitalSignsUpdate(BaseModel):
    """Schema for updating vital signs record"""
    heart_rate: Optional[int] = Field(default=None, ge=0, le=300, description="Updated heart rate")
    blood_pressure_systolic: Optional[int] = Field(default=None, ge=0, le=300, description="Updated systolic blood pressure")
    blood_pressure_diastolic: Optional[int] = Field(default=None, ge=0, le=200, description="Updated diastolic blood pressure")
    temperature: Optional[float] = Field(default=None, ge=30.0, le=50.0, description="Updated temperature")
    oxygen_saturation: Optional[int] = Field(default=None, ge=0, le=100, description="Updated oxygen saturation")
    respiratory_rate: Optional[int] = Field(default=None, ge=0, le=100, description="Updated respiratory rate")
    weight_kg: Optional[float] = Field(default=None, ge=0.0, description="Updated weight")
    height_cm: Optional[float] = Field(default=None, ge=0.0, description="Updated height")
    bmi: Optional[float] = Field(default=None, ge=0.0, description="Updated BMI")
    notes: Optional[str] = Field(default=None, max_length=1000, description="Updated notes")


class VitalSignsResponse(BaseModel):
    """Schema for returning vital signs data"""
    id: int
    user_id: int
    heart_rate: Optional[int]
    blood_pressure_systolic: Optional[int]
    blood_pressure_diastolic: Optional[int]
    temperature: Optional[float]
    oxygen_saturation: Optional[int]
    respiratory_rate: Optional[int]
    weight_kg: Optional[float]
    height_cm: Optional[float]
    bmi: Optional[float]
    notes: Optional[str]
    recorded_at: datetime
    created_at: datetime
    updated_at: datetime


class MedicationCreate(BaseModel):
    """Schema for creating a medication record"""
    name: str = Field(..., min_length=1, max_length=255, description="Name of the medication")
    dosage: str = Field(..., max_length=100, description="Dosage amount and unit (e.g., 10mg, 5ml)")
    frequency: str = Field(..., max_length=100, description="How often to take the medication")
    start_date: datetime = Field(default_factory=datetime.utcnow, description="When to start taking the medication")
    end_date: Optional[datetime] = Field(default=None, description="When to stop taking the medication")
    prescribed_by: Optional[str] = Field(default=None, max_length=255, description="Doctor who prescribed the medication")
    instructions: Optional[str] = Field(default=None, max_length=1000, description="Special instructions for taking medication")
    is_active: bool = Field(default=True, description="Whether the medication is currently active")


class MedicationUpdate(BaseModel):
    """Schema for updating a medication record"""
    name: Optional[str] = Field(default=None, min_length=1, max_length=255, description="Updated medication name")
    dosage: Optional[str] = Field(default=None, max_length=100, description="Updated dosage")
    frequency: Optional[str] = Field(default=None, max_length=100, description="Updated frequency")
    start_date: Optional[datetime] = Field(default=None, description="Updated start date")
    end_date: Optional[datetime] = Field(default=None, description="Updated end date")
    prescribed_by: Optional[str] = Field(default=None, max_length=255, description="Updated prescribing doctor")
    instructions: Optional[str] = Field(default=None, max_length=1000, description="Updated instructions")
    is_active: Optional[bool] = Field(default=None, description="Updated active status")


class MedicationResponse(BaseModel):
    """Schema for returning medication data"""
    id: int
    name: str
    dosage: str
    frequency: str
    start_date: datetime
    end_date: Optional[datetime]
    prescribed_by: Optional[str]
    instructions: Optional[str]
    is_active: bool
    user_id: int
    created_at: datetime
    updated_at: datetime


class AllergyCreate(BaseModel):
    """Schema for creating an allergy record"""
    allergen: str = Field(..., min_length=1, max_length=255, description="Substance causing the allergy")
    reaction: Optional[str] = Field(default=None, max_length=500, description="Reaction experienced")
    severity: Optional[str] = Field(default=None, max_length=50, description="Severity level (mild, moderate, severe)")
    date_identified: datetime = Field(default_factory=datetime.utcnow, description="When the allergy was identified")
    notes: Optional[str] = Field(default=None, max_length=1000, description="Additional notes")
    is_active: bool = Field(default=True, description="Whether the allergy is currently active")


class AllergyUpdate(BaseModel):
    """Schema for updating an allergy record"""
    allergen: Optional[str] = Field(default=None, min_length=1, max_length=255, description="Updated allergen")
    reaction: Optional[str] = Field(default=None, max_length=500, description="Updated reaction")
    severity: Optional[str] = Field(default=None, max_length=50, description="Updated severity")
    date_identified: Optional[datetime] = Field(default=None, description="Updated identification date")
    notes: Optional[str] = Field(default=None, max_length=1000, description="Updated notes")
    is_active: Optional[bool] = Field(default=None, description="Updated active status")


class AllergyResponse(BaseModel):
    """Schema for returning allergy data"""
    id: int
    allergen: str
    reaction: Optional[str]
    severity: Optional[str]
    date_identified: datetime
    notes: Optional[str]
    is_active: bool
    user_id: int
    created_at: datetime
    updated_at: datetime