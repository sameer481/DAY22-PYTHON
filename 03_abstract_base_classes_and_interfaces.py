"""
================================================================================
Day 22: Python Object-Oriented Programming - Abstract Base Classes & Protocols
================================================================================
While pure Duck Typing provides supreme flexibility, large enterprise systems
often require formal contracts to ensure that polymorphic objects satisfy an
exact interface before runtime execution.

Python provides two powerful mechanisms for formal polymorphic interfaces:
1. Abstract Base Classes (ABCs) via the `abc` module (Nominal Subtyping)
2. Structural Subtyping (Protocols) via `typing.Protocol` (PEP 544)

Key Concepts Covered in this Script:
1. The Pitfalls of Implicit Duck Typing in Large Codebases
2. Defining Strict Interfaces with `abc.ABC` and `@abstractmethod`
3. Abstract Properties and Abstract Class Methods
4. Virtual Subclasses via `abc.register()` (Structural Subtyping via ABCs)
5. Modern Duck Typing with `typing.Protocol` & `@runtime_checkable`
6. ABCs vs Protocols: Architectural Trade-Offs & Decision Matrix
7. Real-World Enterprise Storage Repository Architecture
================================================================================
"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Dict, Any, List, Optional


def print_separator(title: str) -> None:
    """Utility helper to print structured visual headers for each demonstration."""
    print("\n" + "=" * 75)
    print(f" {title}")
    print("=" * 75)


# ==============================================================================
# 1. THE PROBLEM WITH IMPLICIT CONTRACTS
# ==============================================================================
# In pure duck typing, if a developer forgets to implement a required method,
# no error occurs when the class is defined or instantiated.
# The program crashes much later at runtime during customer execution!

print_separator("1. The Problem with Pure Duck Typing: Late Runtime Failures")

class UnverifiedDatabaseService:
    def connect(self) -> None:
        print("Connected to database.")
    # Notice: Developer forgot to implement query() and disconnect()!

def execute_pipeline(service: Any) -> None:
    service.connect()
    # Late crash!
    try:
        service.query("SELECT * FROM users")
    except AttributeError as exc:
        print(f"[!] Runtime Crash: Object failed polymorphic contract: {exc}")

execute_pipeline(UnverifiedDatabaseService())


# ==============================================================================
# 2. FORMAL POLYMORPHIC CONTRACTS VIA abc.ABC
# ==============================================================================
# Abstract Base Classes (ABCs) enforce that all derived classes MUST implement
# every decorated @abstractmethod. If any method is missing, Python prevents
# instantiation immediately with a clear TypeError!

print_separator("2. Abstract Base Classes (ABCs) and @abstractmethod")

class DatabaseDriver(ABC):
    """
    Formal interface defining the contract for all database drivers.
    Cannot be instantiated directly.
    """

    @abstractmethod
    def connect(self, connection_string: str) -> bool:
        """Establish connection to the database server."""
        pass

    @abstractmethod
    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """Execute a query and return tabular rows."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close connection and flush pool."""
        pass

    # ABCs can also provide concrete helper methods!
    def ping(self) -> str:
        return "PONG (Driver is alive)"


# Test 1: Attempting to instantiate the abstract class itself
try:
    driver = DatabaseDriver()  # type: ignore
except TypeError as exc:
    print(f"[OK] Caught expected ABC instantiation rejection:\n     -> {exc}")


# Test 2: Incomplete subclass missing abstract methods
class IncompletePostgresDriver(DatabaseDriver):
    def connect(self, connection_string: str) -> bool:
        return True
    # Missing execute_query() and disconnect()!

try:
    pg = IncompletePostgresDriver()  # type: ignore
except TypeError as exc:
    print(f"[OK] Instantiation rejected at creation time for incomplete subclass:\n     -> {exc}")


# Test 3: Fully compliant concrete implementation
class PostgreSQLDriver(DatabaseDriver):
    def __init__(self):
        self._connected = False

    def connect(self, connection_string: str) -> bool:
        self._connected = True
        print(f"[PostgreSQL] Connected via '{connection_string}'.")
        return True

    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        if not self._connected:
            raise RuntimeError("Database not connected!")
        print(f"[PostgreSQL] Executing SQL: {sql}")
        return [{"id": 1, "username": "admin"}, {"id": 2, "username": "dev"}]

    def disconnect(self) -> None:
        self._connected = False
        print("[PostgreSQL] Connection closed.")


pg_driver = PostgreSQLDriver()
pg_driver.connect("postgresql://admin:secret@localhost:5432/master_db")
results = pg_driver.execute_query("SELECT id, username FROM users")
print(f"[PostgreSQL] Returned {len(results)} rows: {results}")
print(f"[PostgreSQL] Concrete inherited ping: {pg_driver.ping()}")
pg_driver.disconnect()


# ==============================================================================
# 3. ABSTRACT PROPERTIES AND ABSTRACT CLASS METHODS
# ==============================================================================
# In addition to regular methods, interfaces can mandate properties or classmethods.

print_separator("3. Abstract Properties and Class Methods")

class CloudComputeResource(ABC):
    @property
    @abstractmethod
    def hourly_cost(self) -> float:
        """Subclasses must define an hourly rate property."""
        pass

    @classmethod
    @abstractmethod
    def provider_name(cls) -> str:
        """Subclasses must define a class method identifying provider."""
        pass


class AWSInstance(CloudComputeResource):
    @property
    def hourly_cost(self) -> float:
        return 0.096

    @classmethod
    def provider_name(cls) -> str:
        return "Amazon Web Services (AWS EC2)"


aws = AWSInstance()
print(f"Provider:    {AWSInstance.provider_name()}")
print(f"Hourly Cost: ${aws.hourly_cost:.3f}")


# ==============================================================================
# 4. VIRTUAL SUBCLASSES VIA abc.register()
# ==============================================================================
# What if a class comes from a 3rd-party library and satisfies an ABC's interface,
# but was written without inheriting from our ABC?
# Python allows registering it as a "virtual subclass" using .register()!

print_separator("4. Virtual Subclasses via abc.register()")

class Serializable(ABC):
    @abstractmethod
    def serialize(self) -> str:
        pass


class ExternalThirdPartyReport:
    """Class from an external library that has a serialize() method."""
    def serialize(self) -> str:
        return "<xml><status>Approved</status></xml>"


# Register external class without modifying its inheritance hierarchy!
Serializable.register(ExternalThirdPartyReport)

report = ExternalThirdPartyReport()
print(f"Is instance of Serializable? {isinstance(report, Serializable)}")
print(f"Is subclass of Serializable? {issubclass(ExternalThirdPartyReport, Serializable)}")
print(f"Serialized output:           {report.serialize()}")


# ==============================================================================
# 5. MODERN DUCK TYPING: typing.Protocol (PEP 544)
# ==============================================================================
# Introduced in Python 3.8+, Protocols provide Structural Subtyping:
# "Static Duck Typing". A class implements a Protocol simply by having matching
# method names and signatures—NO inheritance or registration required!
# With @runtime_checkable, isinstance() checks work at runtime too!

print_separator("5. Structural Subtyping with typing.Protocol & @runtime_checkable")

@runtime_checkable
class DocumentRenderable(Protocol):
    """Protocol defining anything that can be rendered to document format."""
    def render(self) -> str:
        ...

    def get_word_count(self) -> int:
        ...


# Concrete classes do NOT inherit from DocumentRenderable!
class Invoice:
    def __init__(self, inv_id: str, amount: float):
        self.inv_id = inv_id
        self.amount = amount

    def render(self) -> str:
        return f"INVOICE #{self.inv_id}: Total ${self.amount:,.2f}"

    def get_word_count(self) -> int:
        return 4


class BlogPost:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def render(self) -> str:
        return f"# {self.title}\n\n{self.content}"

    def get_word_count(self) -> int:
        return len(self.content.split())


class AudioFile:
    """Does not satisfy the protocol."""
    def play(self) -> None:
        pass


def publish_document(doc: DocumentRenderable) -> None:
    """Polymorphic consumer using Protocol type annotation."""
    if isinstance(doc, DocumentRenderable):
        print(f"[PUBLISHER] Verified Document ({type(doc).__name__}):")
        print(f"            Content: {doc.render()}")
        print(f"            Word Count: {doc.get_word_count()}")
    else:
        print(f"[!] Object {type(doc).__name__} does not conform to DocumentRenderable Protocol!")


publish_document(Invoice("INV-8910", 4500.00))
publish_document(BlogPost("Polymorphism in Python", "Polymorphism allows objects to take multiple forms."))
publish_document(AudioFile())  # type: ignore


# ==============================================================================
# 6. ARCHITECTURAL COMPARISON: ABCs VS PROTOCOLS
# ==============================================================================
print_separator("6. Comparison Matrix: ABCs vs Protocols vs Duck Typing")

comparison_table = [
    ("Feature", "Pure Duck Typing", "Abstract Base Classes (ABCs)", "typing.Protocol (PEP 544)"),
    ("Typing Style", "Dynamic Typing", "Nominal Subtyping", "Structural Subtyping"),
    ("Inheritance", "Not required", "Required (or .register())", "Not required (Implicit)"),
    ("Instantiation Check", "None (Fails late)", "Immediate TypeError", "Static analyzer (Mypy/Pyright)"),
    ("Runtime isinstance()", "Manual / hasattr", "Supported natively", "Supported with @runtime_checkable"),
    ("Shared Code/State", "No", "Yes (Can have concrete methods)", "No (pure interface definitions)"),
    ("Best Use Case", "Quick scripts & small code", "Large enterprise frameworks", "Modern typed libraries & APIs")
]

for row in comparison_table:
    print(f"{row[0]:<23} | {row[1]:<22} | {row[2]:<30} | {row[3]}")


# ==============================================================================
# 7. REAL-WORLD DEMONSTRATOR: STORAGE REPOSITORY PATTERN
# ==============================================================================
print_separator("7. Real-World Demonstrator: Storage Repository Pattern")

class StorageRepository(ABC):
    """Abstract interface for persistent storage engines."""

    @abstractmethod
    def save(self, key: str, payload: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def find_by_key(self, key: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        pass


class InMemoryCacheRepository(StorageRepository):
    """In-memory dictionary repository for high-speed local testing."""
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def save(self, key: str, payload: Dict[str, Any]) -> bool:
        self._store[key] = payload
        print(f"[InMemory] Saved record under key '{key}'")
        return True

    def find_by_key(self, key: str) -> Optional[Dict[str, Any]]:
        return self._store.get(key)

    def delete(self, key: str) -> bool:
        return self._store.pop(key, None) is not None


class CloudS3Repository(StorageRepository):
    """Simulated AWS S3 cloud object store."""
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self._cloud_store: Dict[str, Dict[str, Any]] = {}

    def save(self, key: str, payload: Dict[str, Any]) -> bool:
        s3_uri = f"s3://{self.bucket_name}/{key}.json"
        self._cloud_store[s3_uri] = payload
        print(f"[S3 Storage] Uploaded payload to {s3_uri}")
        return True

    def find_by_key(self, key: str) -> Optional[Dict[str, Any]]:
        s3_uri = f"s3://{self.bucket_name}/{key}.json"
        return self._cloud_store.get(s3_uri)

    def delete(self, key: str) -> bool:
        s3_uri = f"s3://{self.bucket_name}/{key}.json"
        return self._cloud_store.pop(s3_uri, None) is not None


# Polymorphic Service consuming any StorageRepository
class UserProfileService:
    def __init__(self, repository: StorageRepository):
        self.repository = repository

    def register_user(self, user_id: str, username: str, email: str) -> None:
        user_data = {"user_id": user_id, "username": username, "email": email}
        self.repository.save(user_id, user_data)

    def fetch_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.repository.find_by_key(user_id)


# Demonstrate swapping storage backends polymorphically:
print("Executing with InMemory repository:")
in_mem_service = UserProfileService(InMemoryCacheRepository())
in_mem_service.register_user("usr_001", "alice", "alice@example.com")
print(f"Retrieved: {in_mem_service.fetch_user('usr_001')}")

print("\nExecuting with S3 Cloud repository without changing UserProfileService code:")
s3_service = UserProfileService(CloudS3Repository("production-user-backups"))
s3_service.register_user("usr_002", "bob", "bob@cloud.io")
print(f"Retrieved: {s3_service.fetch_user('usr_002')}")

print("\n[Summary] ABCs and Protocols enable rock-solid, production-grade polymorphic architectures!")
