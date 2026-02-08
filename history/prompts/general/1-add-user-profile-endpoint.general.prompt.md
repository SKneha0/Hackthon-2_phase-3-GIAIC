---
id: 1
title: Add User Profile Endpoint
stage: general
date_iso: 2026-02-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: Add a protected endpoint to fetch the current authenticated user's profile information
labels:
  - auth
  - endpoint
  - user-profile
spec_url: null
ticket_url: null
adr_url: null
pr_url: null
---

# Add User Profile Endpoint

## Files Modified
 - C:\Users\alish\Desktop\Ali\neha\hackathon-2-phasee-2\hackathon-2-phasee-2\backend\schemas\auth_schemas.py
 - C:\Users\alish\Desktop\Ali\neha\hackathon-2-phasee-2\hackathon-2-phasee-2\backend\routes\auth.py

## Summary
Added a new protected endpoint GET /api/auth/me that returns the logged-in user's basic profile data. The endpoint requires a valid JWT token via the existing get_current_user dependency and returns user profile information in the specified JSON format.

## Changes Made

### 1. Added UserProfileResponse Pydantic Model
- Created a new response model in auth_schemas.py for user profile data
- Includes id, email, name (optional), and createdAt fields
- Ensures clean, typed output for the endpoint

### 2. Implemented GET /api/auth/me Endpoint
- Added the protected endpoint to routes/auth.py
- Uses existing get_current_user dependency for authentication
- Queries the database to get full user information
- Returns user profile in the required JSON format
- Converts createdAt field to ISO string format
- Handles 404 case when user is not found in the database

## Technical Details
- Endpoint: GET /api/auth/me
- Authentication: Requires valid JWT token via existing get_current_user dependency
- Response: JSON with id, email, name, and createdAt fields
- Error handling: Returns 401 for invalid/missing token, 404 for user not found

## Prompt Text
Current Requirement: Add a protected endpoint to fetch the current authenticated user's profile information.

Implement a new GET /api/auth/me route in the FastAPI backend that returns the logged-in user's basic profile data.

Requirements:
- Endpoint: GET /api/auth/me
- Must be protected: Require valid JWT token via existing get_current_user dependency
- If no valid token → return 401 Unauthorized
- Response body (JSON):
  {
    "id": string,        // user.id from database
    "email": string,     // user.email
    "name": string,      // user.name (or null if not provided)
    "createdAt": string   // ISO format timestamp of user creation (user.created_at)
  }

- Use the existing User model from SQLModel
- Ensure the createdAt field is properly converted to ISO string (e.g., user.created_at.isoformat())
- Use a Pydantic response model for clean, typed output (e.g., UserProfileResponse)
- Route should be placed in the auth routes file (routes/auth.py or similar)
- Return only the current user's data – n

## Response Text
Successfully implemented the protected endpoint to fetch the current authenticated user's profile information. The changes include:

1. Added a new Pydantic response model `UserProfileResponse` in the auth_schemas.py file with the required fields (id, email, name, createdAt).

2. Implemented the GET /api/auth/me endpoint in the routes/auth.py file that:
   - Uses the existing `get_current_user` dependency for authentication
   - Queries the database to retrieve the full user information
   - Returns the user profile data in the specified JSON format
   - Properly converts the createdAt field to ISO string format
   - Handles error cases (401 for invalid token, 404 for user not found)

The endpoint is now available and follows all the specified requirements.

## Outcome
The endpoint has been successfully implemented and follows all the specified requirements. The authentication dependency correctly protects the endpoint, and the response format matches the requirements.