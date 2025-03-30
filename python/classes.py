from dataclasses import dataclass

@dataclass
class User:
	name: str
	age: int
	city: str

new_user = User(name="John", age=30, city="New York")