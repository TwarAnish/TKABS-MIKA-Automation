# Capacity Planning API - Validation Error Reference

## Overview
This document outlines all validation error formats that frontend applications need to handle when interacting with the Capacity Planning API. Errors are returned in Django REST Framework's standard format.

## Error Response Structure
All validation errors follow this general structure:
```json
{
  "field_name": ["Error message 1", "Error message 2"],
  "another_field": ["Another error message"],
  "non_field_errors": ["General error message"]
}
```

---

## 1. Model-Level Validation Errors

### Resource Model Errors
**Endpoint**: `POST/PUT/PATCH /api/resources/`

```json
// External resource without supplier
{
  "non_field_errors": ["External resource must have a supplier."]
}

// Internal resource with supplier
{
  "non_field_errors": ["Internal resource cannot have a supplier."]
}
```

### Project Model Errors
**Endpoint**: `POST/PUT/PATCH /api/projects/`

```json
// End date before start date
{
  "non_field_errors": ["End date cannot be before start date."]
}

// Total capacity exceeded
{
  "non_field_errors": ["Total allocated capacity (150 hours) exceeds the project's total manhours (100)."]
}
```

### ResourceAllocation Model Errors
**Endpoint**: `POST/PUT/PATCH /api/resource-allocations/`

```json
// Before project start
{
  "non_field_errors": ["Cannot allocate internal capacity before the project's start date."]
}

// After project end
{
  "non_field_errors": ["Cannot allocate internal capacity after the project's end date."]
}

// Capacity limit exceeded
{
  "non_field_errors": ["Total allocated capacity (110 hours) would exceed the project's total manhours (100)."]
}

// Hours exceed 45 (field-level validation)
{
  "hours": ["Ensure this value is less than or equal to 45."]
}
```

### ExternalCapacity Model Errors
**Endpoint**: `POST/PUT/PATCH /api/external-capacities/`

```json
// Before project start
{
  "non_field_errors": ["Cannot allocate external capacity before the project's start date."]
}

// After project end
{
  "non_field_errors": ["Cannot allocate external capacity after the project's end date."]
}

// Capacity limit exceeded
{
  "non_field_errors": ["Total allocated capacity (110 hours) would exceed the project's total manhours (100)."]
}
```

---

## 2. Serializer-Level Validation Errors

### Resource Serializer Errors
**Endpoint**: `POST/PUT/PATCH /api/resources/`

```json
// Department not found
{
  "department_name_input": ["Department 'NonExistent Dept' not found"]
}
```

### Project Serializer Errors
**Endpoint**: `POST/PUT/PATCH /api/projects/`

```json
// Department not found
{
  "department_name_input": ["Department 'Invalid Department' not found"]
}
```

### ProjectAssignment Serializer Errors
**Endpoint**: `POST/PUT/PATCH /api/project-assignments/`

```json
// Project code not found
{
  "project_code_input": ["Project with code 'INVALID-001' not found"]
}

// Resource name not found
{
  "resource_name_input": ["Resource 'NonExistent Resource' not found"]
}

// Multiple resources with same name
{
  "resource_name_input": ["Multiple resources found with name 'John Doe'. Use resource_id instead."]
}

// Assignment already exists
{
  "non_field_errors": ["Assignment already exists for John Doe on PRJ-001 in week 2025-01-13"]
}
```

### ResourceAllocation Serializer Errors
**Endpoint**: `POST/PUT/PATCH /api/resource-allocations/`

```json
// Resource already allocated in week
{
  "non_field_errors": ["Resource John Doe already has an allocation in week 2025-01-13."]
}

// Capacity limit exceeded
{
  "non_field_errors": ["Total allocated capacity (110 hours) would exceed the project's total manhours (100)."]
}

// Before project start
{
  "non_field_errors": ["Cannot allocate capacity before the project's start date (2025-01-06)."]
}

// After project end
{
  "non_field_errors": ["Cannot allocate capacity after the project's end date (2025-03-17)."]
}
```

### ProjectWeekAllocation Serializer Errors
**Endpoint**: `POST/PUT/PATCH /api/project-week-allocations/`

```json
// Project code not found
{
  "project_code_input": ["Project with code 'INVALID-001' not found"]
}

// Allocation already exists
{
  "non_field_errors": ["Allocation already exists for project 'PRJ-001' on 2025-01-13"]
}
```

### ExternalCapacity Serializer Errors
**Endpoint**: `POST/PUT/PATCH /api/external-capacities/`

```json
// Project code not found
{
  "project_code_input": ["Project with code 'INVALID-001' not found"]
}

// External capacity already exists
{
  "non_field_errors": ["External capacity already exists for External Vendor on PRJ-001 in week 2025-01-13"]
}

// Capacity limit exceeded
{
  "non_field_errors": ["Total allocated capacity (110 hours) would exceed the project's total manhours (100)."]
}

// Before project start
{
  "non_field_errors": ["Cannot allocate external capacity before the project's start date (2025-01-06)."]
}

// After project end
{
  "non_field_errors": ["Cannot allocate external capacity after the project's end date (2025-03-17)."]
}
```

---

## 3. Bulk Operation Errors

### ProjectAssignment Bulk Create Errors
**Endpoint**: `POST /api/project-assignments/` (bulk)

```json
{
  "error": "Some assignments already exist in database",
  "duplicates": [
    {
      "index": 0,
      "resource_name": "John Doe",
      "project_code": "PRJ-001",
      "week_monday": "2025-01-13"
    }
  ]
}

// Or duplicate within request
{
  "non_field_errors": ["Duplicate entry at index 1: John Doe → PRJ-001 on 2025-01-13"]
}
```

### ProjectWeekAllocation Bulk Create Errors
**Endpoint**: `POST /api/project-week-allocations/` (bulk)

```json
{
  "error": "Cannot create planned allocations for weeks that are already allocated or have existing planned allocations",
  "existing_allocations": [
    {
      "index": 0,
      "project_code": "PRJ-001",
      "week_monday": "2025-01-13",
      "reason": "ProjectWeekAllocation already exists"
    }
  ],
  "already_allocated_weeks": [
    {
      "index": 1,
      "project_code": "PRJ-001",
      "week_monday": "2025-01-20",
      "has_resource_allocation": true,
      "has_external_capacity": false
    }
  ]
}

// Or duplicate within request
{
  "non_field_errors": ["Duplicate entry at index 1: Project PRJ-001 on 2025-01-13"]
}
```

### ExternalCapacity Bulk Create Errors
**Endpoint**: `POST /api/external-capacities/` (bulk)

```json
{
  "error": "Some external capacities already exist in database",
  "duplicates": [
    {
      "index": 0,
      "supplier_name": "External Vendor",
      "project_code": "PRJ-001",
      "week_monday": "2025-01-13"
    }
  ]
}

// Or duplicate within request
{
  "non_field_errors": ["Duplicate entry at index 1: External Vendor → PRJ-001 on 2025-01-13"]
}
```

---

## 4. Database Constraint Errors

### Unique Constraint Violations
When database unique constraints are violated, you may receive:

```json
{
  "non_field_errors": ["Weekly Resource Allocation with this Resource and Week monday already exists."]
}
```

---

## Frontend Error Handling Guidelines

### 1. **Field-Specific Errors**
- Check for errors in specific fields like `"hours"`, `"department_name_input"`, `"project_code_input"`, etc.
- Display these errors next to the corresponding form fields.

### 2. **Non-Field Errors**
- Check for `"non_field_errors"` array for general validation issues.
- Display these as general form errors or notifications.

### 3. **Bulk Operation Errors**
- For bulk operations, check for structured error objects with `"error"`, `"duplicates"`, `"existing_allocations"`, etc.
- Handle each error type appropriately, showing which items failed and why.

### 4. **HTTP Status Codes**
- **400 Bad Request**: Validation errors (covered above)
- **404 Not Found**: Resource not found
- **409 Conflict**: Unique constraint violations
- **500 Internal Server Error**: Server errors

### 5. **Error Message Patterns**
- Look for dynamic values in error messages (project codes, dates, resource names, hour counts)
- Parse these to provide contextual feedback to users

### 6. **Common Error Patterns to Handle**

#### Date Range Errors
```javascript
if (error.non_field_errors?.some(msg => msg.includes('before the project') || msg.includes('after the project'))) {
  // Handle date range violations
  showDateRangeError();
}
```

#### Capacity Limit Errors
```javascript
if (error.non_field_errors?.some(msg => msg.includes('would exceed') || msg.includes('exceeds'))) {
  // Handle capacity limit violations
  showCapacityLimitError();
}
```

#### Duplicate/Constraint Errors
```javascript
if (error.non_field_errors?.some(msg => msg.includes('already exists'))) {
  // Handle duplicate entries
  showDuplicateError();
}
```

#### Field-Specific Validation
```javascript
// Handle field-specific errors
Object.keys(error).forEach(fieldName => {
  if (fieldName !== 'non_field_errors') {
    // Display error next to the field
    showFieldError(fieldName, error[fieldName]);
  }
});
```

---

## Error Categories Summary

| Category | Error Location | Common Fields | Example Use Case |
|----------|----------------|---------------|------------------|
| **Model Validation** | `non_field_errors` | Business rules | Date ranges, capacity limits |
| **Field Validation** | Field name | Django validators | Max value, required fields |
| **Serializer Validation** | Field name | Custom logic | Lookup failures, duplicates |
| **Bulk Operations** | Structured objects | `error`, `duplicates` | Mass data operations |
| **Database Constraints** | `non_field_errors` | Unique violations | Integrity constraints |

This comprehensive error reference ensures robust error handling in your frontend application.