"""
================================================================================
Day 22: Python Object-Oriented Programming - Polymorphism Fundamentals & Duck Typing
================================================================================
Polymorphism is the third core pillar of Object-Oriented Programming (OOP),
building directly upon Encapsulation (Day 20) and Inheritance (Day 21).

Core Definition:
The word "Polymorphism" originates from Greek:
  - "poly"  = many
  - "morph" = forms / shapes
In computer science, polymorphism is the ability of different objects to respond
to the same message (method call or operator) in their own unique, specific ways.
It enables a single unified interface to control entities of different types.

Key Concepts Covered in this Script:
1. Conceptual Foundation & The Essence of Polymorphism
2. Dynamic Typing & Python's Duck Typing Philosophy
3. Polymorphism Without Inheritance (Heterogeneous Objects)
4. Built-in Polymorphic Behaviors in Python (len, operators, iteration)
5. Duck Typing Safety: LBYL (Look Before You Leap) vs EAFP (Forgiveness over Permission)
6. Real-World Audio/Media Engine Demonstrating Pure Duck-Typed Polymorphism
================================================================================
"""

from typing import Any, List


def print_separator(title: str) -> None:
    """Utility helper to print structured visual headers for each demonstration."""
    print("\n" + "=" * 75)
    print(f" {title}")
    print("=" * 75)


# ==============================================================================
# 1. WHAT IS POLYMORPHISM? CONCEPTUAL FOUNDATION
# ==============================================================================
# In statically typed languages (like C++ or Java), polymorphism typically
# requires an explicit inheritance hierarchy or interface implementation.
# In Python, thanks to dynamic typing, polymorphism is fundamental, lightweight,
# and ubiquitous.

print_separator("1. Conceptual Foundation: Single Interface, Multiple Forms")

# In real life, think of a "Start Button":
# - Pushing the start button on a Car revs an internal combustion engine.
# - Pushing the start button on a Washing Machine begins a wash cycle.
# - Pushing the start button on a Computer boots the operating system.
# The user uses ONE uniform action: press_start_button(). The outcome depends
# entirely on the object being acted upon.

print("Polymorphism principle:")
print("Client code issues a uniform command -> Receiver determines exact behavior.")


# ==============================================================================
# 2. PYTHON'S DUCK TYPING PHILOSOPHY
# ==============================================================================
# Python adheres to the famous Duck Typing rule:
# "If it walks like a duck and quacks like a duck, it's a duck."
#
# In Python, an object's suitability is determined by the presence of specific
# methods and properties, rather than its explicit class hierarchy or type.

print_separator("2. Duck Typing: Heterogeneous Classes Without Inheritance")

class Duck:
    """A natural waterfowl."""
    def __init__(self, name: str):
        self.name = name

    def quack(self) -> str:
        return f"{self.name} says: Quack! Quack!"

    def fly(self) -> str:
        return f"{self.name} flaps its wings and takes to the skies."


class RobotDuck:
    """A mechanical automaton mimicking a duck - completely unrelated class!"""
    def __init__(self, serial_number: str):
        self.serial_number = serial_number

    def quack(self) -> str:
        return f"Unit {self.serial_number} synthesized audio: [SYNTH-QUACK 440Hz]"

    def fly(self) -> str:
        return f"Unit {self.serial_number} activates jet thrusters: [THRUST ENGAGED]"


class PersonInDuckCostume:
    """A human dressed as a duck - another completely independent class!"""
    def __init__(self, actor_name: str):
        self.actor_name = actor_name

    def quack(self) -> str:
        return f"{self.actor_name} screams: 'QUACK!' into the mascot megaphone."

    def fly(self) -> str:
        return f"{self.actor_name} jumps off the stage, flapping arms awkwardly."


# Polymorphic Client Function
def make_it_quack_and_fly(duck_like_entity: Any) -> None:
    """
    Consumes any object that supports quack() and fly().
    Notice: No isinstance check! No base class requirement!
    """
    print(f"[Duck Test] Quack: {duck_like_entity.quack()}")
    print(f"[Duck Test] Fly:   {duck_like_entity.fly()}")


# Instantiate completely unrelated types
mallard = Duck("Donald")
robo = RobotDuck("TX-800")
actor = PersonInDuckCostume("Charlie")

# Execute polymorphic function over heterogeneous instances
print("Executing polymorphic client function across 3 independent types:")
make_it_quack_and_fly(mallard)
print("-" * 50)
make_it_quack_and_fly(robo)
print("-" * 50)
make_it_quack_and_fly(actor)


# ==============================================================================
# 3. POLYMORPHISM IN BUILT-IN FUNCTIONS AND OPERATORS
# ==============================================================================
# Python's built-in functions demonstrate polymorphism continuously:
# 1. len() invokes __len__() on strings, lists, tuples, dicts, custom objects.
# 2. The '+' operator invokes __add__() on numbers, strings, lists.
# 3. The '*' operator multiplies numbers or repeats sequences.

print_separator("3. Built-in Polymorphic Functions and Operators")

# 1. Polymorphism with len()
print("--- Polymorphism with len() ---")
print(f"len('Python Masterclass'): {len('Python Masterclass')} (String character count)")
print(f"len([10, 20, 30, 40]):      {len([10, 20, 30, 40])} (List item count)")
print(f"len({{'a': 1, 'b': 2}}):       {len({'a': 1, 'b': 2})} (Dictionary key count)")

# Custom class supporting len() polymorphically
class BookShelf:
    def __init__(self, books: List[str]):
        self.books = books

    def __len__(self) -> int:
        return len(self.books)

shelf = BookShelf(["Clean Code", "Design Patterns", "Fluent Python"])
print(f"len(shelf):                 {len(shelf)} (Custom BookShelf object)")

# 2. Polymorphism with the '+' Operator
print("\n--- Polymorphism with '+' Operator ---")
print(f"50 + 25           = {50 + 25} (Numeric Addition)")
print(f"'Master' + 'class' = '{'Master' + 'class'}' (String Concatenation)")
print(f"[1, 2] + [3, 4]   = {[1, 2] + [3, 4]} (List Merging)")

# 3. Polymorphism with iteration
print("\n--- Polymorphism with for-loop iteration ---")
items_to_iterate = [
    "AI",                           # String (sequence of characters)
    [100, 200, 300],                # List (sequence of numbers)
    {"status": 200, "ok": True},   # Dict (keys iteration)
    (x ** 2 for x in range(1, 4))   # Generator expression
]

for idx, collection in enumerate(items_to_iterate, start=1):
    output = [item for item in collection]
    print(f"Collection {idx} ({type(collection).__name__}): {output}")


# ==============================================================================
# 4. DUCK TYPING SAFETY: EAFP VS LBYL
# ==============================================================================
# Because duck typing does not enforce types, how do we handle objects safely?
# Python offers two approaches:
# 1. LBYL: Look Before You Leap (using hasattr(), callable())
# 2. EAFP: Easier to Ask for Forgiveness than Permission (using try...except)
# EAFP is universally recognized as the more Pythonic pattern.

print_separator("4. Duck Typing Safety: LBYL vs EAFP Patterns")

class Dog:
    def speak(self) -> str:
        return "Woof!"

class Cat:
    def speak(self) -> str:
        return "Meow!"

class Rock:
    """An object without speak() behavior."""
    pass


# Approach 1: LBYL (Look Before You Leap) - Explicit checking
def communicate_lbyl(entity: Any) -> None:
    """LBYL checks if the attribute exists and is callable before executing."""
    if hasattr(entity, "speak") and callable(getattr(entity, "speak")):
        print(f"[LBYL] Recognized speaker: {entity.speak()}")
    else:
        print(f"[LBYL] Rejected: {type(entity).__name__} cannot speak!")


# Approach 2: EAFP (Easier to Ask for Forgiveness than Permission) - Pythonic!
def communicate_eafp(entity: Any) -> None:
    """EAFP attempts execution directly and gracefully catches failures."""
    try:
        print(f"[EAFP] Recognized speaker: {entity.speak()}")
    except AttributeError:
        print(f"[EAFP] Gracefully caught: {type(entity).__name__} does not have a speak() method.")


sample_entities = [Dog(), Cat(), Rock()]

print("Testing LBYL (Look Before You Leap):")
for item in sample_entities:
    communicate_lbyl(item)

print("\nTesting EAFP (Easier to Ask for Forgiveness than Permission):")
for item in sample_entities:
    communicate_eafp(item)


# ==============================================================================
# 5. REAL-WORLD DEMONSTRATOR: MULTI-FORMAT AUDIO PLAYBACK ENGINE
# ==============================================================================
# Illustrates a professional production system where a MediaPlayer consumes
# audio formats that are completely separate classes with no shared inheritance,
# yet they behave polymorphically via a shared contract.

print_separator("5. Real-World Demonstrator: Audio Player System")

class MP3Audio:
    """Compressed lossy audio file."""
    def __init__(self, filename: str, bitrate_kbps: int):
        self.filename = filename
        self.bitrate = bitrate_kbps

    def play(self) -> str:
        return f"Decoding MP3 '{self.filename}' @ {self.bitrate} kbps..."

    def pause(self) -> str:
        return f"Buffering MP3 frame pointer for '{self.filename}'."

    def get_codec(self) -> str:
        return "MPEG-1 Audio Layer III"


class FLACAudio:
    """Lossless studio master audio file."""
    def __init__(self, filename: str, bit_depth: int):
        self.filename = filename
        self.bit_depth = bit_depth

    def play(self) -> str:
        return f"Streaming Bit-Perfect FLAC '{self.filename}' @ {self.bit_depth}-bit..."

    def pause(self) -> str:
        return f"Holding PCM audio buffer for FLAC '{self.filename}'."

    def get_codec(self) -> str:
        return "Free Lossless Audio Codec (FLAC)"


class StreamingPodcast:
    """Live networked audio stream over HTTP."""
    def __init__(self, stream_url: str):
        self.stream_url = stream_url

    def play(self) -> str:
        return f"Connecting socket to live stream '{self.stream_url}'..."

    def pause(self) -> str:
        return f"Pausing socket read queue on '{self.stream_url}'."

    def get_codec(self) -> str:
        return "Opus/WebRTC"


class MediaPlayerController:
    """
    Central player engine. It operates completely polymorphically:
    it doesn't care whether the source is MP3, FLAC, or a Live Stream!
    """
    def __init__(self):
        self.playlist: List[Any] = []

    def load_track(self, track: Any) -> None:
        self.playlist.append(track)
        print(f"[Player] Loaded: {type(track).__name__} (Codec: {track.get_codec()})")

    def play_all(self) -> None:
        print("\n--- Starting Playback of Queue ---")
        for track in self.playlist:
            # Polymorphic method invocation
            print(f"> PLAY:  {track.play()}")
            print(f"> PAUSE: {track.pause()}")


# Instantiate controller and load heterogeneous audio sources
player = MediaPlayerController()
player.load_track(MP3Audio("synthwave_sunset.mp3", 320))
player.load_track(FLACAudio("orchestral_symphony.flac", 24))
player.load_track(StreamingPodcast("https://stream.radio.fm/live-python"))

# Play all tracks polymorphically
player.play_all()

print("\n[Summary] Polymorphism enables dynamic, decoupled, and extensible designs!")
