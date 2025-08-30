# DOBS Project - Reports App Documentation

## Overview

The **Reports App** is part of the Django Occurrence Book System (DOBS)
project.\
It provides API endpoints to generate, manage, and retrieve system-wide
reports based on occurrences.\
This enables users and administrators to analyze trends, track
incidents, and export useful summaries.

------------------------------------------------------------------------

## Features Implemented

-   **Report Model**
    -   Represents a generated report that summarizes occurrences.
    -   Fields implemented include:
        -   `title`: A short title/identifier for the report.
        -   `content`: Summary or detailed findings of the report.
        -   `created_at`: Auto-generated timestamp when the report is
            created.
        -   `created_by`: Foreign key linking to the user who generated
            the report.
-   **Serializer**
    -   Converts `Report` model instances to JSON and validates incoming
        data.
    -   Ensures required fields are included during report creation.
-   **Views**
    -   Implemented using DRF viewsets for CRUD operations.
    -   Endpoints covered:
        -   `GET /api/reports/` → List all reports.
        -   `POST /api/reports/` → Create a new report.
        -   `GET /api/reports/{id}/` → Retrieve a single report by ID.
        -   `PUT /api/reports/{id}/` → Update a report.
        -   `DELETE /api/reports/{id}/` → Delete a report.
-   **URLs**
    -   Routed under the `/api/reports/` path.
    -   Configured with Django's router for automatic RESTful endpoints.
-   **Authentication & Permissions**
    -   Token-based authentication enforced.
    -   Only authenticated users can create, update, or delete reports.
    -   Reports listing and retrieval are available to authenticated
        users.
-   **Testing**
    -   Unit tests implemented for API behavior:
        -   Report creation with authentication.
        -   Listing all reports.
        -   Retrieving a report by ID.
        -   Permission checks for unauthenticated access.

------------------------------------------------------------------------

## Example Request/Response

### Create Report (POST)

**Request**

``` http
POST /api/reports/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "title": "Weekly Security Summary",
  "content": "This report highlights the main incidents reported during the week."
}
```

**Response**

``` json
{
  "id": 1,
  "title": "Weekly Security Summary",
  "content": "This report highlights the main incidents reported during the week.",
  "created_at": "2025-08-21T16:00:00Z",
  "created_by": 2
}
```

------------------------------------------------------------------------

## Next Steps / Improvements

-   Implement **export functionality** (PDF, CSV) for reports.
-   Add **filters** to generate reports for specific dates, categories,
    or locations.
-   Extend permissions (e.g., Admin-only report deletion).
-   Add **report scheduling** for automated weekly/monthly reports.
