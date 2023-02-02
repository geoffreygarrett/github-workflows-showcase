import subprocess
import logging

logger = logging.getLogger(__name__)


class CommandExecutionError(Exception):
    pass


def run_command(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise CommandExecutionError(f"Error while executing command: {stderr.decode()}")
        return stdout, stderr
    except Exception as e:
        logger.error(f"Error while executing command '{command}': {e}")
        raise
