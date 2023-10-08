from subprocess import PIPE, Popen
import os
import stat
import json
import platform
import subprocess
import shutil

def run_cmd(command, env=None, capture_output=False, cwd=None):

    try:
        if capture_output:
            result = subprocess.run(command, shell=True, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, check=True, text=True)
        else:
            result = subprocess.run(command, shell=True, env=env, cwd=cwd, check=True)
        
        return result.returncode, result.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stderr

def rmtree(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

class EnvironmentHandler:
	def __init__(self):
		self.modified_env = os.environ.copy()

	def get_env(self):
		return self.modified_env

	def set_environment_variable(self, variable, value):
		self.modified_env[variable] = value

	def reset_environment(self):
		self.modified_env = os.environ.copy()

	def find_and_set_python3(self):
        # check os type
		if platform.system() == "Windows":
			python_executable = "python"
		else:
			python_executable = "python3"

		try:
			run_cmd(f"{python_executable} --version", capture_output=True)
		except Exception:
			return False

        # set PATH
		self.set_environment_variable('PATH', f"{python_executable}:{self.modified_env['PATH']}")

		return True

	def install_python_dependencies(self, deps):

		try:
			result = run_cmd(f"python3 -m pip freeze", env=self.modified_env, capture_output=True)
			pip_packages = result[1].splitlines()
		except Exception:
			print("Error checking installed packages.")
			return

		required_packages = deps
		to_install = [p for p in required_packages if p.lower() not in [pkg.split('==')[0].lower() for pkg in pip_packages]]

		if len(to_install) == 0:
			print("All required Python pip packages are installed")

		for p in to_install:
			print(f'Installing {p} with pip at RT-Thread environment')
			result = run_cmd(f"python3 -m pip install {p}", env=self.modified_env, capture_output=False)

class MetaFileGenerator:
	def __init__(self, path):
		self.meta = {"names": {}}
		self.path = path
		self.save()

	def set_variable(self, package, var, value):
		if package not in self.meta["names"]:
			self.meta["names"][package] = {"cmake-args": []}
		self.meta["names"][package]["cmake-args"].append("-D" + var +  "=" + str(value))
		self.save()

	def save(self):
		with open(self.path, "w") as file:
			file.write(json.dumps(self.meta, indent=4))