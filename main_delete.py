#!/usr/bin/python3
""" Test delete feature """
from models.engine.file_storage import FileStorage
from models.state import State

fs = FileStorage()

all_states = fs.all(State)
print("All States: {}".format(len(all_states.keys())))

new_state = State()
new_state.name = "California"
fs.new(new_state)
fs.save()
print("New State: {}".format(new_state))

all_states = fs.all(State)
print("All States: {}".format(len(all_states.keys())))

another_state = State()
another_state.name = "Nevada"
fs.new(another_state)
fs.save()

fs.delete(new_state)

all_states = fs.all(State)
print("All States: {}".format(len(all_states.keys())))
