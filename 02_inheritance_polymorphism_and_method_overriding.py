"""
================================================================================
Day 22: Python Object-Oriented Programming - Inheritance Polymorphism & Method Overriding
================================================================================
While Python supports Duck Typing (polymorphism without inheritance), Classical
Subtype Polymorphism models hierarchies where derived classes inherit and
specialize contracts defined by a common base class.

Core Definition:
Subtype Polymorphism allows derived classes to override methods inherited from a
parent class, substituting their own domain-specific algorithms while preserving
the same signature. Callers interact with the base type abstraction, and Python's
dynamic dispatch runtime automatically executes the child's specialized version.

Key Concepts Covered in this Script:
1. Subtype Polymorphism Foundations: Base Contract & Overridden Logic
2. Method Overriding in Practice: Corporate Compensation Hierarchy
3. The Liskov Substitution Principle (LSP) in Polymorphic Design
4. Processing Heterogeneous Collections of Polymorphic Objects
5. Cooperative Method Overriding Using super()
6. Dynamic Method Resolution & Polymorphic Introspection
================================================================================
"""

from typing import List


def print_separator(title: str) -> None:
    """Utility helper to print structured visual headers for each demonstration."""
    print("\n" + "=" * 75)
    print(f" {title}")
    print("=" * 75)


# ==============================================================================
# 1. SUBTYPE POLYMORPHISM & METHOD OVERRIDING IN ACTION
# ==============================================================================
# In a corporate payroll system, all employees have an identity and receive pay,
# but their compensation calculations differ fundamentally (salaried, hourly, commission).

print_separator("1. Subtype Polymorphism: Corporate Employee Hierarchy")

class Employee:
    """
    Base class defining the unified interface contract for all employees.
    """
    def __init__(self, emp_id: str, name: str, department: str):
        self.emp_id = emp_id
        self.name = name
        self.department = department

    def calculate_payroll(self) -> float:
        """Base method to be overridden by subclasses."""
        raise NotImplementedError("Subclasses must override calculate_payroll()")

    def get_role_description(self) -> str:
        """Base description method."""
        return f"Standard Employee ({self.department})"

    def generate_pay_stub(self) -> str:
        """Template method relying on polymorphic calculate_payroll()."""
        net_pay = self.calculate_payroll()
        return (
            f"[PAY STUB] ID: {self.emp_id} | Name: {self.name:<15} | "
            f"Role: {self.get_role_description():<22} | Net Pay: ${net_pay:,.2f}"
        )


class SalariedEmployee(Employee):
    """Full-time employee with a fixed monthly salary and annual bonus."""
    def __init__(self, emp_id: str, name: str, department: str, monthly_salary: float, performance_bonus: float = 0.0):
        super().__init__(emp_id, name, department)
        self.monthly_salary = monthly_salary
        self.performance_bonus = performance_bonus

    def calculate_payroll(self) -> float:
        """Specialized payroll: salary + bonus."""
        return self.monthly_salary + self.performance_bonus

    def get_role_description(self) -> str:
        return f"Full-Time Salaried ({self.department})"


class HourlyEmployee(Employee):
    """Contractor or part-time staff compensated per hour with 1.5x overtime."""
    def __init__(self, emp_id: str, name: str, department: str, hourly_rate: float, hours_worked: float):
        super().__init__(emp_id, name, department)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_payroll(self) -> float:
        """Specialized payroll: regular hours + 1.5x overtime beyond 40 hours."""
        if self.hours_worked <= 40:
            return self.hours_worked * self.hourly_rate
        regular_pay = 40 * self.hourly_rate
        overtime_hours = self.hours_worked - 40
        overtime_pay = overtime_hours * (self.hourly_rate * 1.5)
        return regular_pay + overtime_pay

    def get_role_description(self) -> str:
        return f"Hourly Contractor ({self.hours_worked} hrs)"


class CommissionEmployee(Employee):
    """Sales professional earning a base salary plus a percentage of gross sales."""
    def __init__(self, emp_id: str, name: str, department: str, base_salary: float, sales_volume: float, commission_rate: float):
        super().__init__(emp_id, name, department)
        self.base_salary = base_salary
        self.sales_volume = sales_volume
        self.commission_rate = commission_rate

    def calculate_payroll(self) -> float:
        """Specialized payroll: base salary + (sales * commission rate)."""
        return self.base_salary + (self.sales_volume * self.commission_rate)

    def get_role_description(self) -> str:
        return f"Sales Specialist ({self.commission_rate*100:.0f}% comm)"


# ==============================================================================
# 2. UNIFORM PROCESSING OF HETEROGENEOUS COLLECTIONS
# ==============================================================================
# The power of polymorphism: the client code iterates over a list of 'Employee'
# instances and invokes methods uniformly without needing conditional type checks
# (e.g., no if isinstance(emp, SalariedEmployee)...).

print_separator("2. Processing Heterogeneous Collections Uniformly")

staff_roster: List[Employee] = [
    SalariedEmployee("EMP-101", "Alice Jenkins", "Engineering", monthly_salary=8500.0, performance_bonus=1200.0),
    HourlyEmployee("EMP-102", "Bob Martinez", "DevOps", hourly_rate=65.0, hours_worked=48.0),
    CommissionEmployee("EMP-103", "Clara Sterling", "Enterprise Sales", base_salary=3000.0, sales_volume=120000.0, commission_rate=0.08),
    HourlyEmployee("EMP-104", "David Kim", "Support", hourly_rate=35.0, hours_worked=38.0),
    SalariedEmployee("EMP-105", "Elena Rostova", "AI Research", monthly_salary=11000.0)
]

total_corporate_payroll = 0.0

print("Generating Corporate Payroll via Polymorphic Dispatch:")
for employee in staff_roster:
    # Polymorphic call: calculates net pay depending on specific subclass
    pay_stub = employee.generate_pay_stub()
    print(pay_stub)
    total_corporate_payroll += employee.calculate_payroll()

print("-" * 75)
print(f"Total Disbursed Payroll: ${total_corporate_payroll:,.2f}")


# ==============================================================================
# 3. THE LISKOV SUBSTITUTION PRINCIPLE (LSP)
# ==============================================================================
# Formulated by Barbara Liskov (1987), the LSP states:
# "Subtypes must be substitutable for their base types without altering
# any of the desirable properties of the program (correctness, behavior, etc.)."
#
# Classic Violation: The Rectangle and Square Problem.
# Mathematically, a square is a rectangle. But in object-oriented code, mutating
# width independently of height is an invariant of Rectangle that Square breaks!

print_separator("3. The Liskov Substitution Principle (LSP) In Polymorphism")

class Rectangle:
    """Base class modeling a 2D rectangle."""
    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = value

    def area(self) -> float:
        return self._width * self._height


# ANTI-PATTERN: Violating LSP
class BadSquare(Rectangle):
    """
    Subclass attempting to force Square into Rectangle.
    Violates LSP because changing width mutates height, breaking caller expectations!
    """
    def __init__(self, size: float):
        super().__init__(size, size)

    @Rectangle.width.setter
    def width(self, value: float) -> None:
        self._width = value
        self._height = value  # Side effect breaks Rectangle invariant!

    @Rectangle.height.setter
    def height(self, value: float) -> None:
        self._width = value
        self._height = value


def verify_rectangle_contract(rect: Rectangle) -> None:
    """Client function assuming standard Rectangle behavior."""
    rect.width = 10
    rect.height = 5
    expected_area = 50.0
    actual_area = rect.area()
    print(f"Testing {type(rect).__name__}: Expected area = {expected_area}, Actual area = {actual_area}")
    if actual_area != expected_area:
        print(f"  [!] LSP VIOLATION DETECTED: Subtype {type(rect).__name__} broke base class contract!")
    else:
        print(f"  [OK] LSP COMPLIANT: Subtype adheres to contract.")


normal_rect = Rectangle(2, 4)
violating_square = BadSquare(4)

verify_rectangle_contract(normal_rect)
verify_rectangle_contract(violating_square)

# THE CORRECT ARCHITECTURAL DESIGN FOR LSP:
# Both Square and Rectangle should inherit from an abstract Shape, or be immutable,
# or avoid forcing an 'Is-A' relationship when state mutation invariants diverge.

class Shape:
    def area(self) -> float:
        raise NotImplementedError


class GoodRectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class GoodSquare(Shape):
    def __init__(self, side: float):
        self.side = side

    def area(self) -> float:
        return self.side * self.side


print("\nCorrect Polymorphic Design (Shared Shape Abstraction):")
shapes: List[Shape] = [GoodRectangle(10, 5), GoodSquare(5)]
for s in shapes:
    print(f"  Shape {type(s).__name__:<15} Area: {s.area()}")


# ==============================================================================
# 4. COOPERATIVE METHOD OVERRIDING WITH super()
# ==============================================================================
# Subclasses do not always completely replace parent logic; often they extend it
# cooperatively by calling super().method().

print_separator("4. Cooperative Method Overriding with super()")

class LoggerService:
    def log(self, message: str) -> None:
        print(f"[BASE LOG] {message}")


class TimestampLogger(LoggerService):
    def log(self, message: str) -> None:
        # Prepend timestamp, then delegate to parent
        decorated = f"[2026-10-17 09:30:00 UTC] {message}"
        super().log(decorated)


class EncryptedLogger(TimestampLogger):
    def log(self, message: str) -> None:
        # Simulate simple encryption hash
        encrypted = f"AES256({message})"
        super().log(encrypted)


logger = EncryptedLogger()
logger.log("User authentication token created.")


# ==============================================================================
# 5. DYNAMIC METHOD RESOLUTION & INTROSPECTION
# ==============================================================================
print_separator("5. Dynamic Method Resolution & Introspection")

# Python determines which method to call at runtime via the Method Resolution Order (MRO).
for employee in staff_roster[:3]:
    target_func = employee.calculate_payroll
    print(f"Employee: {employee.name:<15} -> Method Bound to: {target_func.__qualname__}")

print(f"\nSalariedEmployee MRO: {[cls.__name__ for cls in SalariedEmployee.__mro__]}")
