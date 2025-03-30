from dataclasses import dataclass

@dataclass
class Project:
	name: str
	payment: int
	client: str

new_project = Project(client="Client Name", name="App",  payment=2000)

print(new_project)