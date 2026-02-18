
# Centralized error handling and logging utilities
import logging
from colorama import Fore, Style

logging.basicConfig(filename='scanner.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def log_error(message):
	"""Log and print an error message in red."""
	print(Fore.RED + Style.BRIGHT + f"Error: {message}")
	logging.error(message)

def log_warning(message):
	"""Log and print a warning message in yellow."""
	print(Fore.YELLOW + Style.BRIGHT + f"Warning: {message}")
	logging.warning(message)

def log_info(message):
	"""Log and print an info message in green."""
	print(Fore.GREEN + f"{message}")
	logging.info(message)

def handle_exception(e, context=""):
	"""Log and print an exception with context."""
	msg = f"Exception in {context}: {e}"
	log_error(msg)
