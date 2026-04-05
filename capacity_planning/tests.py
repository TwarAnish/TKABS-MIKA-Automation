from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import date, timedelta
from decimal import Decimal

from .models import *
from accounts.models import *


class DateRangeValidationTest(TestCase):
    """Test 1: Date Range Validation - Internal & External allocations must fall within project start_monday to end_monday"""

    def setUp(self):
        """Set up test data"""
        self.department = Department.objects.create(
            name="Engineering",
            icon_text="ENG"
        )
        self.supplier = Supplier.objects.create(
            name="External Vendor",
            contact_email="vendor@example.com"
        )
        self.project = Project.objects.create(
            name="Test Project",
            project_code="TEST-001",
            status="PLANNED",
            total_manhours=1000,
            allotted_weeks=10,
            department=self.department,
            start_monday=date(2025, 1, 6),  # Jan 6, 2025
            end_monday=date(2025, 3, 17)    # Mar 17, 2025 (10 weeks)
        )
        self.internal_resource = Resource.objects.create(
            name="John Doe",
            role="DES",
            is_internal=True,
            department=self.department,
            availability_per_week=40
        )
        self.external_resource = Resource.objects.create(
            name="Jane Smith",
            role="DES",
            is_internal=False,
            supplier=self.supplier,
            availability_per_week=40
        )

    def test_internal_allocation_before_project_start_fails(self):
        """Internal allocation before project start should fail"""
        allocation = ResourceAllocation(
            resource=self.internal_resource,
            project=self.project,
            week_monday=date(2024, 12, 30),  # Before project start
            hours=40
        )
        with self.assertRaises(ValidationError) as context:
            allocation.clean()
        self.assertIn("before the project's start date", str(context.exception))

    def test_internal_allocation_after_project_end_fails(self):
        """Internal allocation after project end should fail"""
        allocation = ResourceAllocation(
            resource=self.internal_resource,
            project=self.project,
            week_monday=date(2025, 3, 24),  # After project end
            hours=40
        )
        with self.assertRaises(ValidationError) as context:
            allocation.clean()
        self.assertIn("after the project's end date", str(context.exception))

    def test_internal_allocation_within_date_range_succeeds(self):
        """Internal allocation within project date range should succeed"""
        allocation = ResourceAllocation(
            resource=self.internal_resource,
            project=self.project,
            week_monday=date(2025, 1, 13),  # Within project range
            hours=40
        )
        try:
            allocation.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly")

    def test_external_capacity_before_project_start_fails(self):
        """External capacity before project start should fail"""
        capacity = ExternalCapacity(
            supplier=self.supplier,
            project=self.project,
            week_monday=date(2024, 12, 30),  # Before project start
            hours=40
        )
        with self.assertRaises(ValidationError) as context:
            capacity.clean()
        self.assertIn("before the project's start date", str(context.exception))

    def test_external_capacity_after_project_end_fails(self):
        """External capacity after project end should fail"""
        capacity = ExternalCapacity(
            supplier=self.supplier,
            project=self.project,
            week_monday=date(2025, 3, 24),  # After project end
            hours=40
        )
        with self.assertRaises(ValidationError) as context:
            capacity.clean()
        self.assertIn("after the project's end date", str(context.exception))

    def test_external_capacity_within_date_range_succeeds(self):
        """External capacity within project date range should succeed"""
        capacity = ExternalCapacity(
            supplier=self.supplier,
            project=self.project,
            week_monday=date(2025, 1, 13),  # Within project range
            hours=40
        )
        try:
            capacity.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly")


class NoEmployeeWeekDuplicatesTest(TestCase):
    """Test 2: No Employee Week Duplicates - Single resource cannot have multiple allocations in the same week"""

    def setUp(self):
        """Set up test data"""
        self.department = Department.objects.create(
            name="Engineering",
            icon_text="ENG"
        )
        self.project = Project.objects.create(
            name="Test Project",
            project_code="TEST-002",
            status="PLANNED",
            total_manhours=1000,
            allotted_weeks=10,
            department=self.department,
            start_monday=date(2025, 1, 6),
            end_monday=date(2025, 3, 17)
        )
        self.resource = Resource.objects.create(
            name="John Doe",
            role="DES",
            is_internal=True,
            department=self.department,
            availability_per_week=40
        )

    def test_same_resource_same_week_different_project_fails(self):
        """Same resource cannot have allocations in same week across different projects"""
        # Create first allocation
        ResourceAllocation.objects.create(
            resource=self.resource,
            project=self.project,
            week_monday=date(2025, 1, 13),
            hours=40
        )

        # Try to create another project
        project2 = Project.objects.create(
            name="Test Project 2",
            project_code="TEST-002-2",
            status="PLANNED",
            total_manhours=500,
            allotted_weeks=5,
            department=self.department,
            start_monday=date(2025, 1, 6),
            end_monday=date(2025, 3, 17)
        )

        # Try to create duplicate allocation - should fail due to unique constraint
        # The unique constraint is enforced via full_clean() which raises ValidationError
        allocation = ResourceAllocation(
            resource=self.resource,
            project=project2,
            week_monday=date(2025, 1, 13),  # Same week
            hours=20
        )
        with self.assertRaises(ValidationError) as context:
            allocation.save()
        self.assertIn("Weekly Resource Allocation with this Resource and Week monday already exists", str(context.exception))

    def test_same_resource_different_week_succeeds(self):
        """Same resource can have allocations in different weeks"""
        ResourceAllocation.objects.create(
            resource=self.resource,
            project=self.project,
            week_monday=date(2025, 1, 13),
            hours=40
        )
        
        # This should succeed - different week
        allocation2 = ResourceAllocation.objects.create(
            resource=self.resource,
            project=self.project,
            week_monday=date(2025, 1, 20),
            hours=40
        )
        self.assertIsNotNone(allocation2.pk)

    def test_different_resource_same_week_succeeds(self):
        """Different resources can have allocations in same week"""
        resource2 = Resource.objects.create(
            name="Jane Doe",
            role="DES",
            is_internal=True,
            department=self.department,
            availability_per_week=40
        )
        
        ResourceAllocation.objects.create(
            resource=self.resource,
            project=self.project,
            week_monday=date(2025, 1, 13),
            hours=40
        )
        
        # This should succeed - different resource
        allocation2 = ResourceAllocation.objects.create(
            resource=resource2,
            project=self.project,
            week_monday=date(2025, 1, 13),
            hours=40
        )
        self.assertIsNotNone(allocation2.pk)


class ProjectTotalCapacityLimitsTest(TestCase):
    """Test 3: Project Total Capacity Limits - Combined Internal + External capacity cannot exceed project total_manhours"""

    def setUp(self):
        """Set up test data"""
        self.department = Department.objects.create(
            name="Engineering",
            icon_text="ENG"
        )
        self.supplier = Supplier.objects.create(
            name="External Vendor",
            contact_email="vendor@example.com"
        )
        self.project = Project.objects.create(
            name="Test Project",
            project_code="TEST-003",
            status="PLANNED",
            total_manhours=100,  # Total capacity: 100 hours
            allotted_weeks=5,
            department=self.department,
            start_monday=date(2025, 1, 6),
            end_monday=date(2025, 2, 3)
        )
        self.internal_resource = Resource.objects.create(
            name="John Doe",
            role="DES",
            is_internal=True,
            department=self.department,
            availability_per_week=40
        )

    def test_internal_capacity_exceeding_total_manhours_fails(self):
        """Total internal capacity exceeding project total_manhours should fail"""
        # Add allocations that would exceed total (using max 45 hours per allocation)
        ResourceAllocation.objects.create(
            resource=self.internal_resource,
            project=self.project,
            week_monday=date(2025, 1, 6),
            hours=45  # First allocation (max allowed for internal)
        )

        # This should fail - would exceed total (45 + 60 = 105 > 100, but can't use 60 for internal)
        # So test with valid internal hours that exceed limit
        # Need a different test case - let's add more allocations
        ResourceAllocation.objects.create(
            resource=self.internal_resource,
            project=self.project,
            week_monday=date(2025, 1, 20),
            hours=45  # Total now 90
        )

        # Now try to add another that would exceed
        allocation = ResourceAllocation(
            resource=self.internal_resource,
            project=self.project,
            week_monday=date(2025, 1, 27),
            hours=45  # Would make total 135 > 100
        )
        with self.assertRaises(ValidationError) as context:
            allocation.clean()
        self.assertIn("exceed the project's total manhours", str(context.exception))

    def test_external_capacity_exceeding_total_manhours_fails(self):
        """External capacity combined with internal exceeding total should fail"""
        # Add internal allocation
        ResourceAllocation.objects.create(
            resource=self.internal_resource,
            project=self.project,
            week_monday=date(2025, 1, 6),
            hours=45
        )

        # This should fail - 45 + 60 = 105 > 100 (external can have >45 hours)
        capacity = ExternalCapacity(
            supplier=self.supplier,
            project=self.project,
            week_monday=date(2025, 1, 13),
            hours=60  # External can have >45 hours
        )
        with self.assertRaises(ValidationError) as context:
            capacity.clean()
        self.assertIn("exceed the project's total manhours", str(context.exception))

    def test_combined_internal_external_exact_limit_succeeds(self):
        """Combined internal + external exactly at total_manhours should succeed"""
        ResourceAllocation.objects.create(
            resource=self.internal_resource,
            project=self.project,
            week_monday=date(2025, 1, 6),
            hours=45
        )

        # External capacity can be up to fill remaining (100 - 45 = 55)
        ExternalCapacity.objects.create(
            supplier=self.supplier,
            project=self.project,
            week_monday=date(2025, 1, 13),
            hours=55  # Exactly fills to 100
        )
        # Total = 100, which equals total_manhours

        self.assertTrue(True)  # No exception means success

    def test_combined_under_limit_succeeds(self):
        """Combined internal + external under total_manhours should succeed"""
        ResourceAllocation.objects.create(
            resource=self.internal_resource,
            project=self.project,
            week_monday=date(2025, 1, 6),
            hours=30
        )
        
        ExternalCapacity.objects.create(
            supplier=self.supplier,
            project=self.project,
            week_monday=date(2025, 1, 13),
            hours=30
        )
        # Total = 60 < 100
        
        self.assertTrue(True)


class PerAllocationHourLimitsTest(TestCase):
    """Test 4: Per-Allocation Hour Limits - Internal: Max 45h, External: No per-allocation limit but cannot exceed project total_manhours"""

    def setUp(self):
        """Set up test data"""
        self.department = Department.objects.create(
            name="Engineering",
            icon_text="ENG"
        )
        self.supplier = Supplier.objects.create(
            name="External Vendor",
            contact_email="vendor@example.com"
        )
        self.project = Project.objects.create(
            name="Test Project",
            project_code="TEST-004",
            status="PLANNED",
            total_manhours=500,  # Large capacity for external testing
            allotted_weeks=10,
            department=self.department,
            start_monday=date(2025, 1, 6),
            end_monday=date(2025, 3, 17)
        )
        self.internal_resource = Resource.objects.create(
            name="John Doe",
            role="DES",
            is_internal=True,
            department=self.department,
            availability_per_week=40
        )

    def test_internal_allocation_at_45_hours_succeeds(self):
        """Internal allocation at exactly 45 hours should succeed"""
        allocation = ResourceAllocation(
            resource=self.internal_resource,
            project=self.project,
            week_monday=date(2025, 1, 13),
            hours=45
        )
        try:
            allocation.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError for 45 hours")

    def test_internal_allocation_above_45_hours_fails(self):
        """Internal allocation above 45 hours should fail (test via save())"""
        allocation = ResourceAllocation(
            resource=self.internal_resource,
            project=self.project,
            week_monday=date(2025, 1, 13),
            hours=46
        )
        # The MaxValueValidator(45) is enforced in the model's save() via full_clean()
        with self.assertRaises(ValidationError) as context:
            allocation.save()
        self.assertIn("hours", context.exception.message_dict)
        self.assertIn("Ensure this value is less than or equal to 45", str(context.exception))

    def test_external_capacity_no_per_allocation_limit(self):
        """External capacity has no per-allocation limit (but limited by project total)"""
        # Create external capacity with more than 45 hours
        # Should not raise ValidationError from MaxValueValidator
        capacity = ExternalCapacity(
            supplier=self.supplier,
            project=self.project,
            week_monday=date(2025, 1, 13),
            hours=100  # More than 45, but this is allowed for external
        )
        try:
            capacity.clean()
        except ValidationError as e:
            # Should only fail due to total_manhours, not per-allocation limit
            self.assertIn("total manhours", str(e))
            
    def test_external_capacity_within_total_manhours_succeeds(self):
        """External capacity within project total_manhours should succeed"""
        capacity = ExternalCapacity(
            supplier=self.supplier,
            project=self.project,
            week_monday=date(2025, 1, 13),
            hours=100  # Within 500 total_manhours
        )
        try:
            capacity.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError for external capacity within limit")
            
    def test_external_capacity_exceeding_total_manhours_fails(self):
        """External capacity exceeding project total_manhours should fail"""
        # First, add some internal capacity to reduce available budget
        ResourceAllocation.objects.create(
            resource=self.internal_resource,
            project=self.project,
            week_monday=date(2025, 1, 6),
            hours=45  # Uses 45 of 500
        )

        # Now try to add external capacity that would exceed total
        capacity = ExternalCapacity(
            supplier=self.supplier,
            project=self.project,
            week_monday=date(2025, 1, 13),
            hours=456  # Would make total 501 > 500
        )
        with self.assertRaises(ValidationError) as context:
            capacity.clean()
        self.assertIn("exceed the project's total manhours", str(context.exception))

    def test_planned_demand_exceeding_total_manhours_fails(self):
        """Planned demand (ProjectWeekAllocation) exceeding project total_manhours should fail"""
        allocation = ProjectWeekAllocation(
            project=self.project,
            week_monday=date(2025, 1, 13),
            manhours=600  # Exceeds 500 total_manhours
        )
        with self.assertRaises(ValidationError) as context:
            allocation.clean()
        self.assertIn("exceed the project's total manhours", str(context.exception))

    def test_planned_demand_within_total_manhours_succeeds(self):
        """Planned demand within project total_manhours should succeed"""
        allocation = ProjectWeekAllocation(
            project=self.project,
            week_monday=date(2025, 1, 13),
            manhours=300  # Within 500 total_manhours
        )
        try:
            allocation.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError for planned demand within limit")
