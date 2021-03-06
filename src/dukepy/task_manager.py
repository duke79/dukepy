import sys
import uuid
from multiprocessing import Process, Event

from core.singleton import Singleton


class Ledger():
	__metaclass__ = Singleton

	all_tasks = []
	events = {}
	logs_files = {}


class Task(Process):
	def __init__(self, *args, **kwargs):
		# A unique id goes a long way
		self.uid = uuid.uuid4()

		# No harm in having a human readable identifier
		self.tag = kwargs.pop("tag", "Anonymous task")

		# Logs file path
		Ledger().logs_files[self.uid] = kwargs.pop("logs_file", str(self.uid) + ".out")
		self._logs_files = Ledger().logs_files

		# Base constructor
		Process.__init__(self, *args, **kwargs)

		# Add self to the tasks lists
		Ledger().all_tasks.append(self)

		# Init empty predecessor
		self._predecessors = []

		# Create an unset event entry for self
		Ledger().events[self.uid] = Event()

		# Keep a copy to access in Run (otherwise it won't work)
		self._events = Ledger().events

		# Save the user inputs
		self._target = kwargs["target"]
		self._args = kwargs["args"]

	def run(self):
		# Wait until predecessor finishes
		for predecessor in self._predecessors:
			while not self._events[predecessor.uid].is_set():
				pass

		# Redirect the output
		sys.stdout = open(self._logs_files[self.uid], "w")

		# Call the target
		self._target(*self._args)

		# Notify done
		self._events[self.uid].set()

	def terminate(self):
		self._events[self.uid].set()
		Process.terminate(self)

	def start_after(self, p):
		self._predecessors = p
		self.start()


def task_cb(args):
	print(args)


def main():
	p1 = Task(target=task_cb, args=("task1",), logs_file="sab1.oo", tag="Task1_tag")
	p2 = Task(target=task_cb, args=("task2",), logs_file="sab2.oo")
	p3 = Task(target=task_cb, args=("task3",))
	p1.start_after([p2, p3])
	# p1.start()
	# p2.start()
	p2.start()
	p3.start()
	# p1.terminate()
	# p2.terminate()  # Makes p1 run in advance
	# p3.terminate()

	# Print logs
	# p1.join()

	for task in Ledger().all_tasks:
		while task.is_alive():
			pass
		try:
			with open(Ledger().logs_files[task.uid], "r") as f:
				print(task.is_alive())
				print(f.read())
				print(task.tag)
		except Exception as e:
			pass


if __name__ == "__main__":
	main()
