import pickle
from dataclasses import dataclass
from classes import User

def serialize_user(user: User):
    return pickle.dumps(user)

def deserialize_user(data: bytes):
    return pickle.loads(data)

def write_to_file(data: bytes, path: str):
    with open(path, 'wb') as file:
        file.write(data)

def read_from_file(path: str):
    with open(path, 'rb') as file:
        return file.read()


def main():
    user = User(name="John", age=30, city="New York")
    serialized_user = serialize_user(user)
    write_to_file(serialized_user, 'user.txt')
    serialized_user_from_file = read_from_file('user.txt')
    deserialized_user = deserialize_user(serialized_user_from_file)
    print(deserialized_user)

main()
    