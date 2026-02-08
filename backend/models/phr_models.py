from sqlmodel import SQLModel, Field, create_engine
from typing import Optional
from datetime import datetime
from pydantic import validator
import uuid

class MedicalRecordBase(SQLModel):
    """Base class for Medical Records with common fields"""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    record_type: str = Field(max_length=100)  # e.g., "lab_result", "prescription", "visit_summary", "vaccination"
    date_of_record: datetime = Field(default_factory=datetime.utcnow)
    doctor_name: Optional[str] = Field(default=None, max_length=255)
    medical_institution: Optional[str] = Field(default=None, max_length=255)


class MedicalRecord(MedicalRecordBase, table=True):
    """Medical Record model representing a user's health record"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)  # Foreign key to users table
    file_url: Optional[str] = Field(default=None, max_length=500)  # URL to stored document
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Add index for record_type field to optimize queries
    __table_args__ = {'sqlite_autoincrement': True}

    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()


class VitalSignsBase(SQLModel):
    """Base class for Vital Signs with common fields"""
    heart_rate: Optional[int] = Field(default=None, ge=0, le=300)
    blood_pressure_systolic: Optional[int] = Field(default=None, ge=0, le=300)
    blood_pressure_diastolic: Optional[int] = Field(default=None, ge=0, le=200)
    temperature: Optional[float] = Field(default=None, ge=30.0, le=50.0)
    oxygen_saturation: Optional[int] = Field(default=None, ge=0, le=100)
    respiratory_rate: Optional[int] = Field(default=None, ge=0, le=100)
    weight_kg: Optional[float] = Field(default=None, ge=0.0)
    height_cm: Optional[float] = Field(default=None, ge=0.0)
    bmi: Optional[float] = Field(default=None, ge=0.0)
    notes: Optional[str] = Field(default=None, max_length=1000)


class VitalSigns(VitalSignsBase, table=True):
    """Vital Signs model for tracking patient vitals"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)  # Foreign key to users table
    recorded_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    __table_args__ = {'sqlite_autoincrement': True}

    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()

    @validator('blood_pressure_systolic', 'blood_pressure_diastolic')
    def validate_blood_pressure(cls, bp_value):
        if bp_value is not None and bp_value <= 0:
            raise ValueError('Blood pressure values must be positive')
        return bp_value


class MedicationBase(SQLModel):
    """Base class for Medications with common fields"""
    name: str = Field(min_length=1, max_length=255)
    dosage: str = Field(max_length=100)  # e.g., "10mg", "5ml"
    frequency: str = Field(max_length=100)  # e.g., "once daily", "twice weekly"
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: Optional[datetime] = Field(default=None)
    prescribed_by: Optional[str] = Field(default=None, max_length=255)
    instructions: Optional[str] = Field(default=None, max_length=1000)
    is_active: bool = Field(default=True)


class Medication(MedicationBase, table=True):
    """Medication model for tracking patient medications"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)  # Foreign key to users table
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    __table_args__ = {'sqlite_autoincrement': True}

    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()


class AllergyBase(SQLModel):
    """Base class for Allergies with common fields"""
    allergen: str = Field(min_length=1, max_length=255)  # e.g., "penicillin", "peanuts", "pollen"
    reaction: Optional[str] = Field(default=None, max_length=500)  # e.g., "rash", "difficulty breathing"
    severity: Optional[str] = Field(default=None, max_length=50)  # e.g., "mild", "moderate", "severe"
    date_identified: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = Field(default=None, max_length=1000)


class Allergy(AllergyBase, table=True):
    """Allergy model for tracking patient allergies"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)  # Foreign key to users table
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    __table_args__ = {'sqlite_autoincrement': True}

    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()