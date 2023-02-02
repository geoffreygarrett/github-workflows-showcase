from .run import run_command
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FeatureNotFoundError(Exception):
    pass


class ReleaseNotFoundError(Exception):
    pass


class CommandExecutionError(Exception):
    pass


def configure_user():
    # Configure user
    try:
        stdout1, stderr1 = run_command("git config user.name github-actions[bot]")
        stdout2, stderr2 = run_command("git config user.email github-actions@github.com")
        if stderr1 or stderr2:
            raise CommandExecutionError(f"Error while configuring user: {stderr1.decode()}{stderr2.decode()}")

        logger.info(f"User configured successfully.")
    except Exception as error:
        logger.error(f"An error occurred while configuring user: {error}")


def git_flow_init(github_token, github_workspace, github_repository):
    # Initialize GitFlow on repository
    try:
        run_command(
            f"git clone https://x-access-token:{github_token}@github.com/{github_repository}.git {github_workspace}")
        os.chdir(github_workspace)
        run_command("git flow init -d")
        logger.info(f"GitFlow initialized successfully for repository '{github_repository}'.")
    except Exception as error:
        logger.error(f"An error occurred while initializing GitFlow for repository '{github_repository}': {error}")


def start_feature(feature_name, github_repository):
    # Start a new feature in GitFlow
    try:
        run_command(f"git flow feature start {feature_name}")
        run_command(f"git push --set-upstream origin feature/{feature_name}")
        logger.info(f"Feature '{feature_name}' started successfully in repository '{github_repository}'.")
    except Exception as error:
        logger.error(
            f"An error occurred while starting the feature '{feature_name}' in repository '{github_repository}': {error}")


def finish_feature(feature_name, github_repository):
    # Finish a feature in GitFlow
    try:
        run_command(f"git branch feature/{feature_name}")
        run_command(f"git flow feature finish {feature_name}")
        run_command("git push")
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
