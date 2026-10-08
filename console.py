#!/usr/bin/python3
"""Command interpreter for the AirBnB clone."""

import cmd
import re
import shlex

from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter."""

    prompt = "(hbnb) "

    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program."""
        print()
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered."""
        pass

    def do_create(self, arg):
        """Create a new instance of a class with optional params.
        Usage: create <Class name> <key>=<value> ..."""
        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        new_instance = self.classes[class_name]()

        for param in args[1:]:
            if "=" not in param:
                continue
            key, value = param.split("=", 1)
            if not key:
                continue

            is_str = len(value) >= 2 and value[0] == value[-1] == '"'
            if is_str:
                inner = value[1:-1]
                if re.search(r'(?<!\\)"', inner):
                    continue
                value = inner.replace('\\"', '"').replace("_", " ")
            elif "." in value:
                try:
                    value = float(value)
                except ValueError:
                    continue
            else:
                try:
                    value = int(value)
                except ValueError:
                    continue

            setattr(new_instance, key, value)

        try:
            new_instance.save()
        except Exception:
            print("** could not create instance **")
            return
        print(new_instance.id)

    def do_show(self, arg):
        """Show an instance based on class name and id."""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        all_objects = storage.all()

        if key not in all_objects:
            print("** no instance found **")
            return

        print(all_objects[key])

    def do_destroy(self, arg):
        """Destroy an instance based on class name and id."""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        all_objects = storage.all()

        if key not in all_objects:
            print("** no instance found **")
            return

        storage.delete(all_objects[key])
        storage.save()

    def do_all(self, arg):
        """Show all instances or all instances of a class."""
        args = shlex.split(arg)
        all_objects = storage.all()

        if args:
            class_name = args[0]

            if class_name not in self.classes:
                print("** class doesn't exist **")
                return

            print([
                str(obj)
                for obj in all_objects.values()
                if obj.__class__.__name__ == class_name
            ])
            return

        print([str(obj) for obj in all_objects.values()])

    def do_update(self, arg):
        """Update an instance with a new attribute value."""
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        all_objects = storage.all()

        if key not in all_objects:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        attribute_name = args[2]

        if len(args) < 4:
            print("** value missing **")
            return

        attribute_value = args[3]
        instance = all_objects[key]

        if hasattr(instance, attribute_name):
            current_value = getattr(instance, attribute_name)

            if isinstance(current_value, int):
                attribute_value = int(attribute_value)
            elif isinstance(current_value, float):
                attribute_value = float(attribute_value)

        setattr(instance, attribute_name, attribute_value)
        instance.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
