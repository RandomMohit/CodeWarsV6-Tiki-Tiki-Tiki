# scripts/bot.py

import importlib
import ast
import os
from . import helpers


def validate_script(script_name):
    path = os.path.join("scripts", f"{script_name}.py")

    if not os.path.exists(path):
        raise ValueError("Script file not found.")

    with open(path, "r") as f:
        source = f.read()

    tree = ast.parse(source)

    found_run = False

    for node in ast.walk(tree):

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Imports are not allowed in scripts.")

        if isinstance(node, ast.ClassDef):
            raise ValueError("Classes are not allowed in scripts.")

        if isinstance(node, ast.FunctionDef):
            if node.name != "run":
                raise ValueError("Only a function named 'run' is allowed.")
            found_run = True

    if not found_run:
        raise ValueError("Script must define a function named 'run'.")


class Bot:

    def __init__(self, player_id, script_name):
        self.player_id = player_id
        self.memory = ""
        self.state = None

        validate_script(script_name)
        module = importlib.import_module(f"scripts.{script_name}")

        # Inject helper functions into script namespace
        for name in dir(helpers):
            if not name.startswith("_"):
                setattr(module, name, getattr(helpers, name))

        self.script = module

    def update_state(self, world_data, gun_spawns, inventory_data, collision_map, grid_size):
        self.state = helpers.build_state(
            self.player_id,
            world_data,
            collision_map,
            grid_size
        )

    def get_action(self):

        if self.state is None:
            return helpers._get_action()

        helpers._reset_action_buffer()

        self.memory = self.memory[:100]

        try:
            new_memory = self.script.run(self.state, self.memory)
            if isinstance(new_memory, str):
                self.memory = new_memory[:100]
            else:
                self.memory = ""
        except Exception as e:
            # If script crashes, fail safe
            print("SCRIPT ERROR:", e)
            self.memory = ""
            raise

        return helpers._get_action()
