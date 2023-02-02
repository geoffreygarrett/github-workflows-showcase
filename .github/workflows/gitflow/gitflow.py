from .run import run_command
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import logging
from .run import run_command

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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


def configure_user():
    """Configure user for Git operations"""
    try:
        stdout1, stderr1 = run_command("git config user.name github-actions[bot]")
        stdout2, stderr2 = run_command("git config user.email github-actions@github.com")
        if stderr1 or stderr2:
            raise GitConfigError(f"Error while configuring user: {stderr1.decode()}{stderr2.decode()}")

        logger.info(f"User configured successfully.")
    except Exception as error:
        logger.error(f"An error occurred while configuring user: {error}")


def git_flow_init(github_repository):
    """Initialize GitFlow on repository"""
    try:
        run_command("git flow init -d")
        logger.info(f"GitFlow initialized successfully for repository '{github_repository}'.")
    except Exception as error:
        logger.error(f"An error occurred while initializing GitFlow for repository '{github_repository}': {error}")


def start_feature(feature_name, github_repository):
    """Start a new feature in GitFlow"""
    try:
        run_command(f"git flow feature start {feature_name}")

        stdout, stderr = run_command(f"git push --set-upstream origin feature/{feature_name}")
        if stderr:
            raise GitFeaturePushError(f"Error while pushing feature '{feature_name}' to remote: {stderr.decode()}")

        logger.info(f"Feature '{feature_name}' started successfully in repository '{github_repository}'.")
    except Exception as error:
        logger.error(
            f"An error occurred while starting the feature '{feature_name}' in repository '{github_repository}': {error}")


def finish_feature(feature_name, github_repository):
    """
    Finishes a feature in GitFlow

    Args:
    - feature_name (str): name of the feature to finish
    - github_repository (str): name of the github repository

    Raises:
    - GitPullError: raised when there is an error while pulling from remote
    - FeatureNotFoundError: raised when the feature is not found in the repository
    - GitPushError: raised when there is an error while pushing to remote

    Returns:
    None
    """
    try:
        stdout, stderr = run_command(f"git pull")
        if stderr:
            raise GitPullError(f"Error while pulling '{feature_name}' from remote: {stderr.decode()}")

        stdout, stderr = run_command(f"git branch feature/{feature_name}")
        if stderr:
            raise FeatureNotFoundError(
                f"Feature '{feature_name}' not found in repository '{github_repository}': {stderr.decode()}")

        run_command(f"git flow feature finish {feature_name}")
        stdout, stderr = run_command(f"git push --set-upstream origin develop")
        if stderr:
            raise GitPushError(f"Error while pushing '{feature_name}' to remote: {stderr.decode()}")

        logger.info(f"Feature '{feature_name}' finished successfully in repository '{github_repository}'.")

    except Exception as error:
        logger.error(
            f"An error occurred while finishing the feature '{feature_name}' in repository '{github_repository}': {error}")


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
