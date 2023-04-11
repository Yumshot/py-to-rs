import os
import subprocess
import shutil

class RustProject:
    def __init__(self, project_name: str, project_type: str = "lib", dependencies: list = None):
        self.project_name = project_name
        self.project_type = project_type
        self.project_path = None
        self.dependencies = dependencies if dependencies else []

    def _check_cargo_installed(self):
        try:
            subprocess.run(["cargo", "--version"], check=True)
        except FileNotFoundError:
            print("Error: Cargo is not installed. Please install Rust and Cargo.")
            return False
        return True

    def create_project(self):
        if not self._check_cargo_installed():
            return

        project_type_flag = "--lib" if self.project_type == "lib" else "--bin"
        try:
            subprocess.run(["cargo", "new", project_type_flag, self.project_name], check=True)
            self.project_path = self.project_name
            self._add_dependencies()
        except subprocess.CalledProcessError as e:
            print(f"Error creating new Rust {self.project_type} project: {str(e)}")

    def _add_dependencies(self):
        if not self.dependencies:
            return

        try:
            for dependency in self.dependencies:
                subprocess.run(["cargo", "add", dependency], check=True, cwd=self.project_path)
        except subprocess.CalledProcessError as e:
            print(f"Error adding dependency: {str(e)}")

    def write_code(self, rust_code: str):
        if self.project_path is None:
            print("Error: Rust project not created.")
            return

        src_file_name = "lib.rs" if self.project_type == "lib" else "main.rs"
        src_file_path = os.path.join(self.project_path, "src", src_file_name)
        with open(src_file_path, "w") as rust_file:
            rust_file.write(rust_code)

    def build_and_run(self):
        if self.project_path is None:
            print("Error: Rust project not created.")
            return

        if not self._check_cargo_installed():
            return

        try:
            subprocess.run(["cargo", "run"], check=True, cwd=self.project_path)
        except subprocess.CalledProcessError as e:
            print(f"Error running Rust code: {str(e)}")

    def cleanup(self):
        if self.project_path is not None:
            shutil.rmtree(self.project_path)
            self.project_path = None
