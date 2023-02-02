import os

import logging
from enum import Enum

# get logger from .__init__.py

# - https://medium.com/itrevolution/five-minute-devops-gitflow-best-practices-a6cd1265de24
# - https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Gitflow-release-branch-process-start-finish
# - https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow
# - https://git.logikum.hu/flow/

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


class GitFlowInitError(RunCommandError):
    """Raised if "git flow init" fails
    """
    pass


def git_flow_init():
    logger.info("Initializing git flow")
    try:
        result = subprocess.run(
            ["git", "flow", "init", "-d"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as error:
        logger.error("Error initializing git flow")
        logger.error("Return code: %d", error.returncode)
        logger.error("Stdout:\n%s", error.stdout.decode().strip())
        logger.error("Stderr:\n%s", error.stderr.decode().strip())
        raise error


class GitConfigError(Exception):
    def __init__(self, message):
        self.message = message


def git_configure_user(name, email):
    logger.info(f"Configuring git user name to {name}, and email to {email}")
    try:
        _ = subprocess.run(
            ["git", "config", "--global", "user.name", name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as error:
        logger.error("Error configuring git user name")
        logger.error("Return code: %d", error.returncode)
        logger.error("Stdout:\n%s", error.stdout.decode().strip())
        logger.error("Stderr:\n%s", error.stderr.decode().strip())
        raise GitConfigError("Error configuring git user name")

    try:
        _ = subprocess.run(
            ["git", "config", "--global", "user.email", email],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as error:
        logger.error("Error configuring git user email")
        logger.error("Return code: %d", error.returncode)
        logger.error("Stdout:\n%s", error.stdout.decode().strip())
        logger.error("Stderr:\n%s", error.stderr.decode().strip())
        raise GitConfigError("Error configuring git user email")


# class ReconcileDivergentBranches(Enum):
#     MERGE = "merge"
#     REBASE = "rebase"
#     FAST_FORWARD = "fast-forward"


def start_feature_branch(feature_name):
    try:
        _ = subprocess.run(
            ["git", "flow", "feature", "start", feature_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as error:
        logger.error("Error starting feature branch %s", feature_name)
        logger.error("Return code: %d", error.returncode)
        logger.error("Stdout:\n%s", error.stdout.decode().strip())
        logger.error("Stderr:\n%s", error.stderr.decode().strip())
        raise error

    # push
    try:
        _ = subprocess.run(
            ["git", "push", "--set-upstream", "origin", "feature/%s" % feature_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as error:
        logger.error("Error pushing feature branch %s", feature_name)
        logger.error("Return code: %d", error.returncode)
        logger.error("Stdout:\n%s", error.stdout.decode().strip())
        logger.error("Stderr:\n%s", error.stderr.decode().strip())
        raise error


class FeatureBranchMergeError(Exception):
    def __init__(self, message):
        self.message = message


def finish_feature_branch(feature_name):
    feature_branch = "feature/%s" % feature_name
    logger.info("Tracking feature branch %s", feature_branch)
    try:
        _ = subprocess.run(
            ["git", "flow", "feature", "track", feature_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as error:
        logger.error("Error tracking feature branch %s", feature_branch)
        logger.error("Return code: %d", error.returncode)
        logger.error("Stdout:\n%s", error.stdout.decode().strip())
        logger.error("Stderr:\n%s", error.stderr.decode().strip())
        message = "Error tracking feature branch. \n"
        message += "Make sure you have git and git flow installed and that you are in the root of a git repository."
        raise FeatureBranchMergeError(message)

    logger.info("Running command: git flow feature finish %s", feature_name)
    try:
        _ = subprocess.run(
            ["git", "flow", "feature", "finish", feature_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as error:
        logger.error("Error finishing feature branch %s", feature_branch)
        logger.error("Return code: %d", error.returncode)
        logger.error("Stdout:\n%s", error.stdout.decode().strip())
        logger.error("Stderr:\n%s", error.stderr.decode().strip())
        if b"have diverged" in error.stderr:
            message = "Branches 'develop' and 'origin/develop' have diverged."
            message += "Resolve the conflict by running the following commands:\n"
            message += "\t- git checkout develop\n"
            message += "\t- git pull origin develop\n"
            message += "\t- git checkout %s\n" % feature_branch
            message += "\t- git merge develop\n"
            message += "\t- Resolve any conflicts (commit the changes) and then run: git flow feature finish %s\n" % feature_name
            raise FeatureBranchMergeError(message)
        if b"CONFLICT (content): Merge conflict in" in error.stdout:
            message = "There are merge conflicts. Resolve the conflict by running the following commands:\n"
            message += "\t- git checkout develop\n"
            message += "\t- git pull origin develop\n"
            message += "\t- git checkout %s\n" % feature_branch
            message += "\t- git merge develop\n"
            message += "\t- Resolve any conflicts (commit the changes) and then run: git flow feature finish %s\n" % feature_name
            raise FeatureBranchMergeError(message)
        else:
            raise error
