"""
================================================================================
Day 22: Python Object-Oriented Programming - Dunder Methods & Operator Overloading
================================================================================
In Python, operator polymorphism allows user-defined classes to intercept and
customize standard language operators (+, -, *, ==, <, [], in, ()).

Core Definition:
Operator Overloading is a form of syntactic polymorphism where the same operator
symbol behaves differently depending on the operand types. Python implements this
via "Dunder" (Double Underscore) or Magic Methods (e.g., __add__, __eq__, __getitem__).

Key Concepts Covered in this Script:
1. The Magic Behind Python Operators: Syntactic Sugar Mapping
2. Complete Arithmetic Overloading with a Mathematical Vector2D Class
3. Reflected/Reverse Operators (__radd__, __rmul__) & In-Place Operators (__iadd__)
4. String Representation Polymorphism: __repr__ vs __str__ vs __format__
5. Rich Comparison Operators & @functools.total_ordering
6. Container/Sequence Protocol: Creating Custom Collection Objects
7. Callable Objects (Functors) via __call__
================================================================================
"""

import math
from functools import total_ordering
from typing import Any, List, Union


def print_separator(title: str) -> None:
    """Utility helper to print structured visual headers for each demonstration."""
    print("\n" + "=" * 75)
    print(f" {title}")
    print("=" * 75)


# ==============================================================================
# 1. ARITHMETIC OPERATOR OVERLOADING: 2D VECTOR
# ==============================================================================
# When you write `a + b`, Python translates that internally to `a.__add__(b)`.
# If `a` doesn't know how to add `b` (returns NotImplemented), Python tries
# `b.__radd__(a)`.

print_separator("1. Arithmetic Operator Overloading: 2D Physics Vector")

class Vector2D:
    """
    Represents a mathematical 2-dimensional vector supporting full arithmetic
    and magnitude calculations.
    """
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    # 1. Unambiguous developer representation
    def __repr__(self) -> str:
        return f"Vector2D(x={self.x}, y={self.y})"

    # 2. Readable string representation
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    # 3. Custom format specifier (e.g., f"{v:.2f}")
    def __format__(self, format_spec: str) -> str:
        if format_spec:
            return f"({format(self.x, format_spec)}, {format(self.y, format_spec)})"
        return str(self)

    # 4. Binary Addition: v1 + v2
    def __add__(self, other: Any) -> "Vector2D":
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        return NotImplemented

    # 5. Binary Subtraction: v1 - v2
    def __sub__(self, other: Any) -> "Vector2D":
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        return NotImplemented

    # 6. Multiplication: Vector * scalar (scaling) or Vector * Vector (dot product)
    def __mul__(self, other: Union[int, float, "Vector2D"]) -> Union["Vector2D", float]:
        if isinstance(other, (int, float)):
            return Vector2D(self.x * other, self.y * other)
        if isinstance(other, Vector2D):
            # Dot product: x1*x2 + y1*y2
            return (self.x * other.x) + (self.y * other.y)
        return NotImplemented

    # 7. Reflected Multiplication: scalar * Vector (e.g., 3 * v)
    def __rmul__(self, other: Union[int, float]) -> "Vector2D":
        # Multiplication is commutative
        return self.__mul__(other)  # type: ignore

    # 8. True Division: Vector / scalar
    def __truediv__(self, scalar: Union[int, float]) -> "Vector2D":
        if isinstance(scalar, (int, float)):
            if scalar == 0:
                raise ZeroDivisionError("Cannot divide vector by zero scalar!")
            return Vector2D(self.x / scalar, self.y / scalar)
        return NotImplemented

    # 9. Negation: -v
    def __neg__(self) -> "Vector2D":
        return Vector2D(-self.x, -self.y)

    # 10. Magnitude: abs(v)
    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    # 11. Equality: v1 == v2
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Vector2D):
            return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
        return False


v1 = Vector2D(3, 4)
v2 = Vector2D(1, 2)

print(f"v1               = {v1}  [Repr: {repr(v1)}]")
print(f"v2               = {v2}")
print(f"v1 + v2          = {v1 + v2}")
print(f"v1 - v2          = {v1 - v2}")
print(f"v1 * 2.5 (scale) = {v1 * 2.5}")
print(f"3 * v1   (rmul)  = {3 * v1}")
print(f"v1 * v2  (dot)   = {v1 * v2}")
print(f"v1 / 2           = {v1 / 2}")
print(f"-v1      (neg)   = {-v1}")
print(f"abs(v1)  (mag)   = {abs(v1):.2f}")
print(f"Formatted:         {v1:.4f}")
print(f"v1 == Vector2D(3, 4): {v1 == Vector2D(3, 4)}")


# ==============================================================================
# 2. RICH COMPARISONS & @functools.total_ordering
# ==============================================================================
# Implementing comparison operators (__lt__, __le__, __gt__, __ge__, __eq__)
# manually is repetitive. Using the `@total_ordering` decorator, you only need
# to implement `__eq__` and one ordering method (usually `__lt__`), and Python
# derives all other comparisons automatically!

print_separator("2. Comparison Polymorphism: Semantic Versioning")

@total_ordering
class SemVer:
    """Represents a Semantic Version (Major.Minor.Patch)."""
    def __init__(self, major: int, minor: int, patch: int):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __repr__(self) -> str:
        return f"v{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SemVer):
            return NotImplemented
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, SemVer):
            return NotImplemented
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)


v_alpha = SemVer(1, 2, 0)
v_beta = SemVer(1, 2, 4)
v_release = SemVer(2, 0, 0)

print(f"{v_alpha} < {v_beta}:   {v_alpha < v_beta}")
print(f"{v_beta} <= {v_alpha}:  {v_beta <= v_alpha}")
print(f"{v_release} > {v_beta}: {v_release > v_beta}")
print(f"{v_alpha} == SemVer(1, 2, 0): {v_alpha == SemVer(1, 2, 0)}")

# Polymorphic sorting! Python's sorted() uses __lt__ automatically:
unsorted_versions = [v_release, v_alpha, v_beta, SemVer(1, 0, 9), SemVer(2, 1, 0)]
sorted_versions = sorted(unsorted_versions)
print(f"Sorted versions list: {sorted_versions}")


# ==============================================================================
# 3. CONTAINER & SEQUENCE PROTOCOL OVERLOADING
# ==============================================================================
# You can make your custom objects act like Python sequences or mappings by
# implementing __len__, __getitem__, __setitem__, __delitem__, __contains__, and __iter__.

print_separator("3. Container Protocol: Custom Music Album Sequence")

class SongTrack:
    def __init__(self, title: str, duration_sec: int):
        self.title = title
        self.duration_sec = duration_sec

    def __repr__(self) -> str:
        return f"'{self.title}' ({self.duration_sec // 60}:{self.duration_sec % 60:02d})"


class Album:
    """Custom collection container implementing sequence dunder methods."""
    def __init__(self, album_title: str, artist: str):
        self.album_title = album_title
        self.artist = artist
        self._tracks: List[SongTrack] = []

    def add_track(self, track: SongTrack) -> None:
        self._tracks.append(track)

    # 1. len(album)
    def __len__(self) -> int:
        return len(self._tracks)

    # 2. album[index] and slicing album[0:2]
    def __getitem__(self, index: Union[int, slice]) -> Any:
        return self._tracks[index]

    # 3. track in album
    def __contains__(self, item: Any) -> bool:
        if isinstance(item, str):
            return any(t.title.lower() == item.lower() for t in self._tracks)
        return item in self._tracks

    # 4. for track in album
    def __iter__(self):
        return iter(self._tracks)


album = Album("The Dark Side of the Code", "Pythoneers")
album.add_track(SongTrack("Speak to My Compiler", 90))
album.add_track(SongTrack("On the CPU Run", 215))
album.add_track(SongTrack("Async Time", 425))
album.add_track(SongTrack("The Great Exception in the Sky", 280))

print(f"Album Length:      {len(album)} tracks")
print(f"First Track:       {album[0]}")
print(f"Slice [1:3]:       {album[1:3]}")
print(f"'Async Time' in album? {'Async Time' in album}")
print(f"'Pop Song' in album?   {'Pop Song' in album}")

print("\nIterating album polymorphically via for-loop:")
for i, track in enumerate(album, start=1):
    print(f"  Track #{i}: {track}")


# ==============================================================================
# 4. CALLABLE OBJECTS (FUNCTORS) VIA __call__
# ==============================================================================
# Implementing __call__ allows an instance of a class to be invoked as if it
# were a function. This is powerful for stateful functions, decorators, and pipelines.

print_separator("4. Callable Objects (Functors) via __call__")

class ExponentialBackoffRetry:
    """Stateful retry calculator maintaining invocation counts."""
    def __init__(self, base_delay_sec: float = 1.0, factor: float = 2.0, max_delay: float = 30.0):
        self.base_delay = base_delay_sec
        self.factor = factor
        self.max_delay = max_delay
        self.attempt_count = 0

    def __call__(self) -> float:
        """Invoked when the object is called like a function: retry()"""
        delay = min(self.base_delay * (self.factor ** self.attempt_count), self.max_delay)
        self.attempt_count += 1
        return delay

    def reset(self) -> None:
        self.attempt_count = 0


# Create the functor instance
retry_policy = ExponentialBackoffRetry(base_delay_sec=1.5, factor=2.0)

# Invoke it directly as a callable:
print("Simulating network retries:")
for _ in range(5):
    next_delay = retry_policy()  # Calls __call__() polymorphically!
    print(f"  Attempt {retry_policy.attempt_count}: Wait {next_delay:.2f} seconds before retry.")

print(f"Is callable? {callable(retry_policy)}")

print("\n[Summary] Dunder methods empower custom types with first-class Python syntax!")
