# 📄 Occurrences App Documentation (DOBS API)

## Overview

The **Occurrences app** manages the recording and tracking of incidents
within the Django Occurrence Book System (**DOBS**).\
It provides API endpoints for creating, retrieving, updating, and
deleting occurrence records, along with related features like photos and
comments.

------------------------------------------------------------------------

## Models

### `Occurrence`

Represents a single incident recorded in the system.\
**Fields:** - `id` *(UUID / AutoField)* -- Unique identifier.\
- `title` *(CharField)* -- Short title of the occurrence.\
- `description` *(TextField)* -- Detailed explanation of the incident.\
- `location` *(CharField)* -- Where the occurrence took place.\
- `date_reported` *(DateTimeField, auto_now_add=True)* -- When the
incident was reported.\
- `reported_by` *(ForeignKey → User)* -- The user who reported the
occurrence.\
- `status` *(ChoiceField)* -- Incident status (e.g., *open,
under_investigation, resolved*).\
- `created_at` *(DateTimeField)* -- Record creation timestamp.\
- `updated_at` *(DateTimeField)* -- Last modification timestamp.

------------------------------------------------------------------------

## Serializers

### `OccurrenceSerializer`

-   Handles serialization/deserialization of `Occurrence` objects.
-   Validates input data when creating/updating occurrences.
-   Includes nested representation for `reported_by` (username or user
    id).

------------------------------------------------------------------------

## Views

### API Endpoints Implemented

1.  **List & Create Occurrences**
    -   **URL:** `/api/occurrences/`
    -   **Methods:**
        -   `GET` → Returns list of all occurrences.\
        -   `POST` → Create a new occurrence. Requires authentication.
2.  **Retrieve, Update, Delete Occurrence**
    -   **URL:** `/api/occurrences/{id}/`
    -   **Methods:**
        -   `GET` → Retrieve a specific occurrence by ID.\
        -   `PUT/PATCH` → Update an occurrence (only by reporter or
            admin).\
        -   `DELETE` → Remove an occurrence (admin only).

------------------------------------------------------------------------

## Permissions

-   **Authenticated users** → Can create and view occurrences.\
-   **Owners** (reporter of the occurrence) → Can update their own
    reports.\
-   **Admins** → Full access (create, update, delete).

------------------------------------------------------------------------

## Example Requests

### 1. Create an Occurrence (POST)

``` http
POST /api/occurrences/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "title": "Suspicious activity at main gate",
  "description": "Two unknown individuals were seen loitering near the gate.",
  "location": "North Gate",
  "status": "open"
}
```

**Response:**

``` json
{
  "id": "f2a1b4d6-1234-4567-89ab-cdef12345678",
  "title": "Suspicious activity at main gate",
  "description": "Two unknown individuals were seen loitering near the gate.",
  "location": "North Gate",
  "date_reported": "2025-08-20T14:32:10Z",
  "reported_by": "thubelihle",
  "status": "open",
  "created_at": "2025-08-20T14:32:10Z",
  "updated_at": "2025-08-20T14:32:10Z"
}
```

### 2. Get All Occurrences (GET)

``` http
GET /api/occurrences/
Authorization: Bearer <your_token>
```

**Response (sample):**

``` json
[
  {
    "id": "f2a1b4d6-1234-4567-89ab-cdef12345678",
    "title": "Suspicious activity at main gate",
    "location": "North Gate",
    "status": "open",
    "reported_by": "thubelihle",
    "date_reported": "2025-08-20T14:32:10Z"
  },
  {
    "id": "b8d4e123-5678-4a12-9ef0-abcdef987654",
    "title": "Lost property reported",
    "location": "Reception",
    "status": "resolved",
    "reported_by": "admin",
    "date_reported": "2025-08-19T10:15:05Z"
  }
]
```

------------------------------------------------------------------------

## Testing Notes

-   ✅ Successfully tested `POST` (with authentication).\
-   ✅ Successfully tested `GET` for list & detail views.\
-   ✅ Permissions checked (only owners/admin can update/delete).\
-   ⚠️ Requires valid JWT token for all write operations.

------------------------------------------------------------------------

## Next Steps (Future Enhancements)

-   Add **Occurrence Photos** model & endpoint.\
-   Add **Comments** functionality for collaborative notes.\
-   Add **filtering & search** by date, location, or status.\
-   Add **reporting/export** features (CSV, PDF).
