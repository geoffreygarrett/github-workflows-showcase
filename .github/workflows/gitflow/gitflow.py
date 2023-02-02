from .run import run_command
import os

import logging
from .run import run_command

# get logger from .__init__.py


from . import logger


class GitError(Exception):
    """Base error for Git operations"""
    pass


def GitPullError(GitError):
    """Error for pulling from remote"""
    pass


def GitPushError(GitError):
    """Error for pushing to remote"""
    pass


class GitConfigError(GitError):
    """Error for configuring user"""
    pass


class GitFlowInitError(GitError):
    """Error for initializing GitFlow on repository"""
    pass


class GitFeatureError(GitError):
    """Base error for Git feature operations"""
    pass


class GitFlowFeatureStartError(GitFeatureError):
    """Error for starting a feature"""
    pass


class GitFlowFeatureFinishError(GitFeatureError):
    """Error for finishing a feature"""
    pass


class GitFeatureNotFoundError(GitFeatureError):
    """Error for not finding the specified feature"""
    pass


class GitFeaturePushError(GitFeatureError):
    """Error for pushing feature to remote"""
    pass


class GitFeaturePullError(GitFeatureError):
    """Error for pulling feature from remote"""
    pass


class FeatureNotFoundError(GitFeatureError):
    """Error for not finding the specified feature"""
    pass


class GitReleaseError(GitError):
    """Base error for Git release operations"""
    pass


class GitReleaseNotFoundError(GitReleaseError):
    """Error for not finding the specified release"""
    pass


class GitReleasePushError(GitReleaseError):
    """Error for pushing release to remote"""
    pass


class GitReleasePullError(GitReleaseError):
    """Error for pulling release from remote"""
    pass


def configure_user(raise_error=False, log_error=True):
    """Configure user for Git operations"""
    try:
        stdout1, stderr1 = run_command("git config user.name github-actions[bot]")
        stdout2, stderr2 = run_command("git config user.email github-actions@github.com")
        if stderr1 or stderr2:
            error_msg = f"Error while configuring user: {stderr1.decode()}{stderr2.decode()}"
            if log_error:
                logger.error(error_msg)
            if raise_error:
                raise GitConfigError(error_msg)
        else:
            logger.info("User configured successfully.")

    except Exception as error:
        error_msg = f"An error occurred while configuring user: {error}"
        if log_error:
            logger.error(error_msg)
        if raise_error:
            raise error


def git_flow_init(raise_error=False):
    """Initialize Git Flow repository"""
    try:
        stdout, stderr = run_command("git flow init -d")
        if stderr:
            error_message = f"Error while initializing Git Flow repository: {stderr.decode()}"
            if raise_error:
                raise GitFlowInitError(error_message)
            else:
                logger.error(error_message)
        else:
            logger.info(f"Git Flow repository initialized successfully.")
    except Exception as error:
        logger.error(f"An error occurred while initializing Git Flow repository: {error}")


def start_feature(feature_name, raise_error=False):
    """Start a new Git Flow feature"""
    try:
        stdout, stderr = run_command(f"git flow feature start {feature_name}")
        if stderr:
            error_message = f"Error while starting Git Flow feature '{feature_name}': {stderr.decode()}"
            if raise_error:
                raise GitFlowFeatureStartError(error_message)
            else:
                logger.error(error_message)
        else:
            logger.info(f"Git Flow feature '{feature_name}' started successfully.")
    except Exception as error:
        logger.error(f"An error occurred while starting Git Flow feature '{feature_name}': {error}")


def finish_feature(feature_name, raise_error=False):
    """Finish an existing Git Flow feature"""
    try:
        stdout, stderr = run_command(f"git flow feature finish {feature_name}")
        if stderr:
            error_message = f"Error while finishing Git Flow feature '{feature_name}': {stderr.decode()}"
            if raise_error:
                raise GitFlowFeatureFinishError(error_message)
            else:
                logger.error(error_message)
        else:
            logger.info(f"Git Flow feature '{feature_name}' finished successfully.")
    except Exception as error:
        logger.error(f"An error occurred while finishing Git Flow feature '{feature_name}': {error}")


def delete_feature(feature_name, github_repository):
    # Delete a feature in GitFlow
    try:
        run_command(f"git flow feature delete {feature_name}")
        logger.info(f"Feature '{feature_name}' deleted successfully in repository '{github_repository}'.")
    except Exception as error:
        logger.error(
            f"An error occurred while deleting the feature '{feature_name}' in repository '{github_repository}': {error}")


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
