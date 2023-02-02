import os

import logging

# get logger from .__init__.py


from . import logger
import subprocess


class UnknownException(Exception):
    message = "Unknown exception occurred, please check the logs for more information." \
              " Contact the developers with the logs if the problem persists."


class RunCommandError(Exception):
    pass


class CommandNotFoundError(RunCommandError):
    """Raised if "Command <command> not found" is in stderr
    """
    pass


class GitNotInstalledError(RunCommandError):
    """Raised if "Command 'git' not found" is in stderr
    """
    re = "Command 'git' not found"
    pass

class GitFlowNotInstalledError(RunCommandError):
    """Raised if "is not a git command" is in stderr
    """
    re = "is not a git command"
    pass

def run_command(command, **kwargs):
    log_command = kwargs.get("log_command", True)
    raise_error = kwargs.get("raise_error", True)
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return_code = process.returncode
        if return_code != 0:
            if log_command:
                logger.error(f"Command '{command}' returned non-zero status: {return_code}")
            if raise_error:
                if "Command not found" in stderr.decode("utf-8"):
                    raise CommandNotFoundError(f"Command '{command}' not found")
                else:
                    raise RunCommandError(
                        f"Command '{command}' returned non-zero status: {return_code}"
                        f" with stderr: {stderr.decode('utf-8')}"
                        f" and stdout: {stdout.decode('utf-8')}"
                        )
        return stdout, stderr, return_code
    except Exception as e:
        if log_command:
            logger.exception(f"Error occurred while running command '{command}'")
        raise e


class GitConfigError(RunCommandError):
    """Error for configuring user

    This command will fail with non-zero status upon error. Some exit codes are:
    The section or key is invalid (ret=1),
    no section or name was provided (ret=2),
    the config file is invalid (ret=3),
    the config file cannot be written (ret=4),
    you try to unset an option which does not exist (ret=5),
    you try to unset/set an option for which multiple lines match (ret=5), or
    you try to use an invalid regexp (ret=6).
    On success, the command returns the exit code 0.
    """
    pass

def git_configure_user(name, email):
    command = f"git config --global user.name '{name}'"
    stdout, stderr, return_code = run_command(command)
    if return_code != 0:
        # this error is not recoverable, so we raise an exception
        raise GitConfigError(f"Error occurred while configuring user name: {stderr}")

    command = f"git config --global user.email '{email}'"
    stdout, stderr, return_code = run_command(command)
    if return_code != 0:
        # this error is not recoverable, so we raise an exception
        raise GitConfigError(f"Error occurred while configuring user email: {stderr}")


import re


class GitFlowInitError(UnknownException):
    pass


def git_flow_init(**kwargs):
    log_command = kwargs.get("log_command", True)
    raise_error = kwargs.get("raise_error", True)
    command = "git flow init -d"
    stdout, stderr, return_code = run_command(command)

    if return_code != 0:
        if re.match(GitNotInstalledError.re, stderr.decode("utf-8")):
            # this error is not recoverable, so we raise an exception
            if log_command:
                logger.error(f"Error occurred while initializing GitFlow (GitNotInstalledError): {stderr}")
            raise GitNotInstalledError(f"Error occurred while initializing GitFlow: {stderr}")
        elif re.match(GitFlowNotInstalledError.re, stderr.decode("utf-8")):
            # this error is not recoverable, so we raise an exception
            if log_command:
                logger.error(f"Error occurred while initializing GitFlow (GitFlowNotInstalledError): {stderr}")
            raise GitFlowNotInstalledError(f"Error occurred while initializing GitFlow: {stderr}")
        else:
            # this error is not recoverable, so we raise an exception
            if log_command:
                logger.error(f"Error occurred while initializing GitFlow: {stderr}")
            raise GitFlowInitError(f"Error occurred while initializing GitFlow: {stderr}")


# git flow init wrapper
def git_flow_init_wrapper(fn):
    def wrapper(*args, **kwargs):
        try:
            git_flow_init(**kwargs)
        except GitFlowInitError:
            logger.info("GitFlow already initialized")
        return fn(*args, **kwargs)
    return wrapper


class GitFlowStartFeatureError(UnknownException):
    pass

@git_flow_init_wrapper
def start_feature(feature_name, **kwargs):
    """
    Start a new feature
    Args:
        feature_name:
        **kwargs:

    Returns:

    Raises:
        - GitFlowInitError
        - GitNotInstalledError
        - GitFlowNotInstalledError
    """
    log_command = kwargs.get("log_command", True)
    raise_error = kwargs.get("raise_error", True)

    command = f"git flow feature start {feature_name}"  # <--------------
    stdout, stderr, return_code = run_command(command)

    if return_code != 0:
        if log_command:
            logger.error(f"Error occurred while starting feature '{feature_name}': {stderr}")
        if raise_error:
            raise GitFlowStartFeatureError(f"Error occurred while starting feature '{feature_name}': {stderr}")

    command = f"git flow feature publish {feature_name}"  # <------------
    stdout, stderr, return_code = run_command(command)
    if return_code != 0:
        if log_command:
            logger.error(f"Error occurred while pushing feature '{feature_name}': {stderr}")
        if raise_error:
            raise GitFlowStartFeatureError(f"Error occurred while pushing feature '{feature_name}': {stderr}")


class GitFlowFeatureFinishError(UnknownException):
    pass

class ReconcileDivergentBranches(Exception):
    MERGE = "merge"
    REBASE = "rebase"
    FAST_FORWARD = "fast-forward"


@git_flow_init_wrapper
def finish_feature(feature_name, **kwargs):
    """
    Finish a feature
    Args:
        feature_name:
        **kwargs:

    Returns:

    Raises:
        - GitFlowInitError
        - GitNotInstalledError
        - GitFlowNotInstalledError
    """
    # http://danielkummer.github.io/git-flow-cheatsheet/
    log_command = kwargs.get("log_command", True)
    raise_error = kwargs.get("raise_error", True)
    reconcile_divergent_branches = kwargs.get("reconcile_divergent_branches", ReconcileDivergentBranches.MERGE)

    feature_track_command = f"git flow feature track {feature_name}"  # <--------------
    stdout, stderr, return_code = run_command(feature_track_command)

    if return_code != 0:
        if log_command:
            logger.error(f"Error occurred while checking feature '{feature_name}': {stderr}")
        if raise_error:
            raise GitFlowFeatureFinishError(f"Error occurred while checking feature '{feature_name}': {stdout}")

    feature_finish_command = f"git flow feature finish {feature_name}"  # <-------------
    stdout, stderr, return_code = run_command(feature_finish_command, raise_error=False)

    if return_code != 0:
        if 'have diverged' in stderr.decode("utf-8"):
            # https://stackoverflow.com/questions/10197188/git-flow-branches-have-diverged
            if reconcile_divergent_branches == ReconcileDivergentBranches.MERGE:
                _, _, _ = run_command(f"git config pull.rebase false")
            elif reconcile_divergent_branches == ReconcileDivergentBranches.REBASE:
                _, _, _ = run_command(f"git config pull.rebase true")
            elif reconcile_divergent_branches == ReconcileDivergentBranches.FAST_FORWARD:
                _, _, _ = run_command(f"git config pull.ff only")

                # stdout, stderr, return_code = run_command(feature_finish_command, raise_error=True)

            _, _, _ = run_command(f"git checkout develop && git pull origin develop")
            # _, _, _ = run_command(f"git flow feature rebase {feature_name}")
            _, _, _ = run_command(feature_finish_command, raise_error=True)

        if log_command:
            logger.error(f"Error occurred while finishing feature '{feature_name}': {stderr}")

        if raise_error:
            raise GitFlowFeatureFinishError(f"Error occurred while finishing feature '{feature_name}': {stdout}")

    command = f"git push origin"  # <------------------------------------
    stdout, stderr, return_code = run_command(command)

    if return_code != 0:
        if log_command:
            logger.error(f"Error occurred while pushing develop branch: {stderr}")
        if raise_error:
            raise GitFlowFeatureFinishError(f"Error occurred while pushing develop branch: {stdout}")

#
# class GitFlowDeleteFeatureError(UnknownException):
#     pass
#
#
# def delete_feature(feature_name, **kwargs):
#     """
#     Delete a feature
#     Args:
#         feature_name:
#         **kwargs:
#
#     Returns:
#
#     Raises:
#         - GitFlowInitError
#         - GitNotInstalledError
#         - GitFlowNotInstalledError
#     """
#
#     log_command = kwargs.get("log_command", True)
#     raise_error = kwargs.get("raise_error", True)
#
#     command = f"git branch feature/{feature_name}"
#     stdout, stderr, return_code = run_command(command)
#
#     if return_code != 0:
#         if log_command:
#             logger.error(f"Error occurred while checking feature '{feature_name}': {stderr}")
#         if raise_error:
#             raise GitFlowDeleteFeatureError(f"Error occurred while checking feature '{feature_name}': {stderr}")
#
#     command = f"git flow feature delete {feature_name}"
#     stdout, stderr, return_code = run_command(command)
#
#     if return_code != 0:
#         if log_command:
#             logger.error(f"Error occurred while deleting feature '{feature_name}': {stderr}")
#         if raise_error:
#             raise GitFlowDeleteFeatureError(f"Error occurred while deleting feature '{feature_name}': {stderr}")
#
#     command = f"git push origin --delete feature/{feature_name}"
#     stdout, stderr, return_code = run_command(command)
#
#     if return_code != 0:
#         if log_command:
#             logger.error(f"Error occurred while deleting remote feature '{feature_name}': {stderr}")
#         if raise_error:
#             raise GitFlowDeleteFeatureError(f"Error occurred while deleting remote feature '{feature_name}': {stderr}")



def start_release(release_name, github_repository):
    # Start a new release in GitFlow
    try:
        run_command(f"git flow release start {release_name}")
        run_command("git push --set-upstream origin release/{release_name}")
        logger.info(f"Release '{release_name}' started successfully in repository '{github_repository}'.")
    except Exception as error:
        logger.error(
            f"An error occurred while starting the release '{release_name}' in repository '{github_repository}': {error}")


def finish_release(release_name, github_repository):
    # Finish a release in GitFlow
    try:
        run_command(f"git branch -D release/{release_name}")
        run_command(f"git flow release finish {release_name}")
        run_command("git push")
        logger.info(f"Release '{release_name}' finished successfully in repository '{github_repository}'.")
    except Exception as error:
        logger.error(
            f"An error occurred while finishing the release '{release_name}' in repository '{github_repository}': {error}")
