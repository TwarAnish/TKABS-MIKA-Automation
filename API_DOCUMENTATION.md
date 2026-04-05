# Capacity Planning API Documentation

## Overview
This document provides comprehensive documentation for all Capacity Planning API endpoints, including request/response formats and validation error handling.

## API Categories

### 1. Core CRUD APIs (Model-based)
### 2. Dashboard & Analytics APIs
### 3. Bulk Operations APIs
### 4. Legacy Function-based APIs

---

## 1. Core CRUD APIs (Model-based)

### Departments

#### `GET /api/departments/`
**List all departments**
- **Query Parameters**:
  - `search` (string): Search in department names
  - `ordering` (string): Order by 'order' or 'name'
- **Response**: Array of department objects
- **Success Response**:
```json
[
  {
    "id": 1,
    "name": "Engineering",
    "icon_text": "ENG",
    "parent": null,
    "order": 1,
    "level": 0,
    "full_path": "Engineering",
    "children_count": 2
  }
]
```

#### `GET /api/departments/tree/`
**Get department hierarchy tree**
- **Response**: Nested department tree structure

#### `POST /api/departments/`
**Create new department**
- **Request Body**:
```json
{
  "name": "Design Engineering",
  "icon_text": "DES",
  "parent": 1,
  "order": 2
}
```
- **Validation Errors**:
  - `name`: ["This field is required."]
  - `non_field_errors`: ["Department with this Parent and Name already exists."]

### Resources

#### `GET /api/resources/`
**List all resources**
- **Query Parameters**:
  - `is_internal` (boolean): Filter by internal/external
  - `department` (int): Department ID
  - `role` (string): Role code (DES, SIM, etc.)
  - `is_active` (boolean): Active status
  - `search` (string): Search in names
- **Response**: Array of resource objects with department and supplier info

#### `GET /api/resources/{id}/weekly-load/`
**Get resource weekly allocation load**
- **Query Parameters**:
  - `start` (YYYY-MM-DD): Start date (defaults to this Monday)
  - `weeks` (int): Number of weeks (default 26, max 104)
- **Response**:
```json
{
  "resource": "John Doe",
  "availability_per_week": 45,
  "data": [
    {
      "week_monday": "2025-01-13",
      "hours": 40
    }
  ]
}
```
- **Validation Errors**:
  - `{"error": "weeks must be a positive integer between 1 and 104"}`
  - `{"error": "Invalid start date format. Use YYYY-MM-DD"}`

#### `POST /api/resources/`
**Create new resource**
- **Request Body**:
```json
{
  "name": "Jane Smith",
  "role": "DES",
  "is_internal": true,
  "department": 1,
  "availability_per_week": 40,
  "department_name_input": "Design Engineering"
}
```
- **Validation Errors**:
  - `department_name_input`: ["Department 'Invalid Dept' not found"]
  - `non_field_errors`: ["External resource must have a supplier."]

### Projects

#### `GET /api/projects/`
**List all projects**
- **Query Parameters**:
  - `status` (string): QUOTED, PLANNED, ORDERED
  - `department` (int/string): Department ID or name
  - `search` (string): Search in name/project_code
- **Response**: Array of project objects with department and allocation summaries

#### `POST /api/projects/`
**Create new project**
- **Request Body**:
```json
{
  "project_code": "PRJ-2025-001",
  "name": "New Project",
  "status": "PLANNED",
  "total_manhours": 1000,
  "allotted_weeks": 10,
  "start_monday": "2025-01-06",
  "department": 1,
  "department_name_input": "Engineering"
}
```
- **Validation Errors**:
  - `project_code`: ["Project with this Project code already exists."]
  - `department_name_input`: ["Department 'Invalid' not found"]
  - `non_field_errors`: ["End date cannot be before start date."]

### Project Assignments

#### `GET /api/assignments/`
**List all project assignments**
- **Query Parameters**:
  - `project` (int): Project ID
  - `resource` (int): Resource ID
  - `is_lead` (boolean): Lead assignments only
- **Response**: Array of assignment objects with nested resource/project data

#### `POST /api/assignments/`
**Create project assignment**
- **Request Body**:
```json
{
  "resource": 1,
  "project": 1,
  "is_lead": false,
  "week_monday": "2025-01-13",
  "notes": "Assignment notes"
}
```
- **Validation Errors**:
  - `non_field_errors`: ["Assignment already exists for John Doe on PRJ-001 in week 2025-01-13"]

### Resource Allocations

#### `GET /api/allocations/`
**List all resource allocations**
- **Query Parameters**:
  - `project` (int): Project ID
  - `resource` (int): Resource ID
  - `week_monday` (YYYY-MM-DD): Specific week
- **Response**: Array of allocation objects with nested resource/project data

#### `POST /api/allocations/`
**Create resource allocation**
- **Request Body**:
```json
{
  "resource": 1,
  "project": 1,
  "week_monday": "2025-01-13",
  "hours": 40
}
```
- **Validation Errors**:
  - `hours`: ["Ensure this value is less than or equal to 45."]
  - `non_field_errors`: ["Resource John Doe already has an allocation in week 2025-01-13."]

### Project Week Allocations

#### `GET /api/planned-demand/`
**List all planned demand allocations**
- **Query Parameters**:
  - `project` (int): Project ID
  - `week_monday` (YYYY-MM-DD): Specific week
- **Response**: Array of planned allocation objects

#### `POST /api/planned-demand/`
**Create planned demand allocation**
- **Request Body**:
```json
{
  "project": 1,
  "week_monday": "2025-01-13",
  "manhours": 160,
  "notes": "Design freeze week"
}
```
- **Validation Errors**:
  - `non_field_errors`: ["Allocation already exists for project 'PRJ-001' on 2025-01-13"]

### External Capacities

#### `GET /api/external-capacity/`
**List all external capacities**
- **Query Parameters**:
  - `supplier` (int): Supplier ID
  - `project` (int): Project ID
  - `week_monday` (YYYY-MM-DD): Specific week
- **Response**: Array of external capacity objects with nested supplier/project data

#### `POST /api/external-capacity/`
**Create external capacity allocation**
- **Request Body**:
```json
{
  "supplier": 1,
  "project": 1,
  "week_monday": "2025-01-13",
  "hours": 50
}
```
- **Validation Errors**:
  - `non_field_errors`: ["External capacity already exists for External Vendor on PRJ-001 in week 2025-01-13"]

### Suppliers

#### `GET /api/suppliers/`
**List all suppliers**
- **Query Parameters**:
  - `is_active` (boolean): Active status
  - `search` (string): Search in names
- **Response**: Array of supplier objects

#### `POST /api/suppliers/`
**Create new supplier**
- **Request Body**:
```json
{
  "name": "New Vendor Inc",
  "contact_email": "contact@newvendor.com",
  "budgeted_hours": 1000,
  "hourly_rate": "75.00",
  "notes": "Specialized in robotics",
  "is_active": true
}
```
- **Validation Errors**:
  - `name`: ["Supplier with this Name already exists."]
  - `contact_email`: ["Enter a valid email address."]

### App Settings

#### `GET /api/settings/`
**Get application settings**
- **Response**: Current app settings (singleton)
```json
{
  "id": 1,
  "default_working_hours_per_week": 45
}
```

---

## 2. Dashboard & Analytics APIs

### Capacity Summary

#### `GET /api/capacity/summary/`
**Weekly capacity summary across date range**
- **Query Parameters**:
  - `start` (YYYY-MM-DD): Start date (defaults to this Monday)
  - `weeks` (int): Number of weeks (default 26, max 104)
  - `department` (int/string): Department filter
- **Response**:
```json
{
  "weeks": [
    {
      "week_monday": "2025-01-13",
      "planned_demand": 160,
      "internal_allocated": 120,
      "external_capacity": 40,
      "total_supply": 160,
      "gap": 0,
      "is_overallocated": false,
      "is_underallocated": false
    }
  ]
}
```
- **Validation Errors**:
  - `{"error": "weeks must be a positive integer between 1 and 104"}`
  - `{"error": "Invalid start date format. Use YYYY-MM-DD"}`
  - `{"error": "Department with id 999 not found"}`

### Capacity Gaps

#### `GET /api/capacity/gaps/`
**Find weeks with capacity gaps above threshold**
- **Query Parameters**:
  - `threshold` (int): Minimum gap in man-days (default 20)
  - `department` (int/string): Department filter
- **Response**:
```json
{
  "gaps": [
    {
      "week_monday": "2025-01-13",
      "gap_manhours": 80,
      "gap_man_days": 16.0
    }
  ]
}
```

### Weekly Project Breakdown

#### `GET /api/weekly-project-breakdown/`
**Project-wise weekly breakdown with internal vs external allocation**
- **Query Parameters**:
  - `start` (YYYY-MM-DD): Start date
  - `end` (YYYY-MM-DD): End date
  - `project_code` (string): Specific project filter
- **Response**:
```json
{
  "date_range": {
    "start": "2025-01-06",
    "end": "2025-03-17"
  },
  "data": [
    {
      "project_name": "Test Project",
      "project_code": "TEST-001",
      "manhours": 160,
      "data": {
        "internal": 120,
        "external": 40
      },
      "week_monday": "2025-01-13",
      "calendar_week": "CW03"
    }
  ]
}
```
- **Validation Errors**:
  - `{"error": "Project with code 'INVALID' not found"}`
  - `{"error": "Invalid date format. Use YYYY-MM-DD"}`

### Department Weekly Breakdown

#### `GET /api/department-weekly-breakdown/`
**Department-wise weekly capacity breakdown**
- **Query Parameters**:
  - `start` (YYYY-MM-DD): Start date
  - `end` (YYYY-MM-DD): End date
  - `department` (int/string): Department filter
- **Response**: Complex nested structure with department/project/week data

### Project Role Utilization

#### `GET /api/project-role-utilization/`
**Role-wise utilization within a project**
- **Query Parameters**:
  - `project_code` (string): **Required**
  - `role` (string): Specific role filter
  - `start` (YYYY-MM-DD): Start date
  - `end` (YYYY-MM-DD): End date
- **Response**:
```json
{
  "project": {
    "code": "PRJ-001",
    "name": "Test Project",
    "department": "Engineering → Design"
  },
  "filtered_role": "DES",
  "date_range": {
    "start": "2025-01-06",
    "end": "2025-03-17"
  },
  "data": [
    {
      "role": "DES",
      "role_name": "Designer",
      "week_monday": "2025-01-13",
      "calendar_week": "CW03",
      "week_display": "Jan 13",
      "actual_hours": {
        "internal": 40,
        "external": 20,
        "total": 60
      }
    }
  ]
}
```
- **Validation Errors**:
  - `{"error": "project_code parameter is required"}`
  - `{"error": "Project 'INVALID' not found"}`
  - `{"error": "Invalid role: 'INVALID'. Valid options: DES, SIM, PLC, ROB, OTHER"}`

### Internal Resource Utilization

#### `GET /api/internal-resource-utilization/`
**Weekly utilization of internal resources**
- **Query Parameters**:
  - `department` (int/string): Department filter
  - `resource` (string): Resource name filter
  - `start` (YYYY-MM-DD): Start date
  - `end` (YYYY-MM-DD): End date
- **Response**: Detailed per-resource weekly utilization data

### Department Weekly Detail

#### `GET /api/department-weekly-detail/`
**Department-wise weekly breakdown with project-level detail**
- **Query Parameters**:
  - `department` (int/string): Department filter
  - `start` (YYYY-MM-DD): Start date
  - `end` (YYYY-MM-DD): End date
- **Response**: Hierarchical department/project/week breakdown

### Employee Summary

#### `GET /api/employee-summary/`
**Employee utilization summary with weekly breakdown**
- **Query Parameters**:
  - `department` (int/string): Department filter
  - `resource` (string): Resource name filter
  - `start` (YYYY-MM-DD): Start date
  - `end` (YYYY-MM-DD): End date
  - `active_only` (boolean): Include only active employees
  - `graph` (boolean): Graph-friendly format
- **Response**: Comprehensive employee utilization data

### Project Summary

#### `GET /api/project-summary/`
**Project-wise capacity utilization summary**
- **Query Parameters**:
  - `department` (int/string): Department filter
  - `project` (int/string): Project ID or code
  - `start` (YYYY-MM-DD): Start date
  - `end` (YYYY-MM-DD): End date
  - `graph` (boolean): Graph-friendly format
- **Response**: Detailed project capacity analysis

### Employee Idle Capacity

#### `GET /api/employee-idle-capacity/`
**Employee idle capacity analysis**
- **Query Parameters**:
  - `department` (int/string): Department filter
  - `start` (YYYY-MM-DD): Start date
  - `end` (YYYY-MM-DD): End date
  - `active_only` (boolean): Include only active employees
  - `graph` (boolean): Graph-friendly format
- **Response**: Employee idle capacity metrics

### Department Capacity Summary

#### `GET /api/department-capacity-summary/`
**Department-wise capacity utilization summary**
- **Query Parameters**:
  - `department` (int/string): Department filter
  - `start` (YYYY-MM-DD): Start date
  - `end` (YYYY-MM-DD): End date
- **Response**: Hierarchical department capacity analysis

### Free Capacity Employees

#### `GET /api/free-capacity-employees/`
**List employees with available capacity**
- **Query Parameters**:
  - `start` (YYYY-MM-DD): Start date (default: current year start)
  - `end` (YYYY-MM-DD): End date (default: current year end)
- **Response**:
```json
{
  "date_range": {
    "start": "2025-01-01",
    "end": "2025-12-31",
    "total_weeks": 52
  },
  "total_employees_with_free_capacity": 5,
  "employees": [
    {
      "id": 1,
      "name": "John Doe",
      "role": "DES",
      "department": "Engineering",
      "is_internal": true,
      "effective_availability_per_week": 45
    }
  ]
}
```

### Supplier Master

#### `GET /api/supplier-master/`
**Supplier utilization and capacity analysis**
- **Query Parameters**:
  - `supplier` (string): Supplier name filter
  - `project` (string): Project code filter
  - `start` (YYYY-MM-DD): Start date
  - `end` (YYYY-MM-DD): End date
- **Response**: Detailed supplier utilization data

---

## 3. Bulk Operations APIs

### Project Assignment Bulk Create

#### `POST /api/project-assignments/bulk/`
**Bulk create project assignments**
- **Request Body**: Array of assignment objects (max 100)
```json
[
  {
    "resource": 1,
    "project": 1,
    "week_monday": "2025-01-13",
    "is_lead": false
  }
]
```
- **Success Response**:
```json
{
  "total_requested": 2,
  "created": 2,
  "allocations_created": 2,
  "errors": 0,
  "data": [...]
}
```
- **Error Response**:
```json
{
  "total_requested": 2,
  "created": 0,
  "errors": 1,
  "error_details": [
    {
      "index": 0,
      "data": {...},
      "errors": {
        "non_field_errors": ["Assignment already exists for John Doe on PRJ-001 in week 2025-01-13"]
      }
    }
  ]
}
```

### Project Week Allocation Bulk Create

#### `POST /api/project-week-allocations/bulk/`
**Bulk create planned demand allocations**
- **Request Body**: Array of allocation objects (max 100)
```json
[
  {
    "project_code_input": "PRJ-001",
    "week_monday": "2025-01-13",
    "manhours": 160,
    "notes": "Design freeze week"
  }
]
```
- **Success Response**:
```json
{
  "total_requested": 2,
  "created": 2,
  "errors": 0,
  "data": [...]
}
```
- **Error Response (Capacity Exceeded)**:
```json
{
  "total_requested": 2,
  "created": 0,
  "errors": 1,
  "error": "Cannot create planned allocations - planned demand would exceed project total_manhours",
  "capacity_exceeded": [
    {
      "index": 0,
      "project_code": "PRJ-001",
      "requested_manhours": 200,
      "existing_planned": 50,
      "total_would_be": 250,
      "project_limit": 200
    }
  ]
}
```
- **Validation Errors**:
  - `capacity_exceeded`: Planned demand would exceed project total_manhours
  - `existing_allocations`: Duplicate ProjectWeekAllocation entries
  - `already_allocated_weeks`: Weeks that already have actual allocations

### External Capacity Bulk Create

#### `POST /api/external-capacities/bulk/`
**Bulk create external capacity allocations**
- **Request Body**: Array of capacity objects (max 100)
- **Success/Error Response**: Similar to other bulk operations

---

## 4. Legacy Function-based APIs

### Projects (Function-based)

#### `GET /api/projects/`
#### `POST /api/projects/`
#### `GET /api/projects/{id}/`
#### `PUT /api/projects/{id}/`
#### `PATCH /api/projects/{id}/`
#### `DELETE /api/projects/{id}/`

**Standard CRUD operations for projects**

### Employees (Function-based)

#### `GET /api/employees/`
#### `POST /api/employees/`
#### `GET /api/employees/{id}/`
#### `PUT /api/employees/{id}/`
#### `PATCH /api/employees/{id}/`
#### `DELETE /api/employees/{id}/`

**Standard CRUD operations for resources (employees)**

### Suppliers (Function-based)

#### `GET /api/suppliers/`
#### `POST /api/suppliers/`
#### `GET /api/suppliers/{id}/`
#### `PUT /api/suppliers/{id}/`
#### `PATCH /api/suppliers/{id}/`
#### `DELETE /api/suppliers/{id}/`

**Standard CRUD operations for suppliers**

### Project Assignments (Function-based)

#### `GET /api/project-assignments/`
#### `POST /api/project-assignments/`
#### `GET /api/project-assignments/{id}/`
#### `PUT /api/project-assignments/{id}/`
#### `PATCH /api/project-assignments/{id}/`
#### `DELETE /api/project-assignments/{id}/`

**Standard CRUD operations for project assignments**

### Resource Allocations (Function-based)

#### `GET /api/resource-allocations/`
#### `POST /api/resource-allocations/`
#### `GET /api/resource-allocations/{id}/`
#### `PUT /api/resource-allocations/{id}/`
#### `PATCH /api/resource-allocations/{id}/`
#### `DELETE /api/resource-allocations/{id}/`

**Standard CRUD operations for resource allocations**

### Project Week Allocations (Function-based)

#### `GET /api/project-week-allocations/`
#### `POST /api/project-week-allocations/`
#### `GET /api/project-week-allocations/{id}/`
#### `PUT /api/project-week-allocations/{id}/`
#### `PATCH /api/project-week-allocations/{id}/`
#### `DELETE /api/project-week-allocations/{id}/`

**Standard CRUD operations for planned demand allocations**

### External Capacities (Function-based)

#### `GET /api/external-capacities/`
#### `POST /api/external-capacities/`
#### `GET /api/external-capacities/{id}/`
#### `PUT /api/external-capacities/{id}/`
#### `PATCH /api/external-capacities/{id}/`
#### `DELETE /api/external-capacities/{id}/`

**Standard CRUD operations for external capacity allocations**

---

## Common Validation Error Patterns

### Field-Level Errors
```json
{
  "field_name": ["Error message 1", "Error message 2"]
}
```

### Non-Field Errors
```json
{
  "non_field_errors": ["General validation error message"]
}
```

### Bulk Operation Errors
```json
{
  "error": "Some items already exist in database",
  "duplicates": [
    {
      "index": 0,
      "resource_name": "John Doe",
      "project_code": "PRJ-001",
      "week_monday": "2025-01-13"
    }
  ]
}
```

### HTTP Status Codes
- **200 OK**: Successful GET requests
- **201 Created**: Successful POST requests
- **204 No Content**: Successful DELETE requests
- **400 Bad Request**: Validation errors
- **404 Not Found**: Resource not found
- **409 Conflict**: Unique constraint violations

---

## Authentication & Permissions

- **Current Setting**: `AllowAny` (no authentication required)
- **Production Recommendation**: Change to `IsAuthenticated` in settings
- **Authentication Classes**: JWT, Session, Basic (configurable)

---

## Rate Limiting & Performance

- **Bulk Operations**: Maximum 100 items per request
- **Date Ranges**: Reasonable limits on query spans
- **Database Optimization**: Select/prefetch related objects
- **Caching**: Consider implementing for dashboard endpoints

This comprehensive API documentation covers all endpoints with their request/response formats and validation error handling. Refer to the `VALIDATION_ERRORS.md` file for detailed error format specifications.