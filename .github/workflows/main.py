import os
import json
import logging

from gitflow.gitflow import (git_flow_init, start_feature, finish_feature, delete_feature,
                             start_release, finish_release, configure_user)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Get environment variables
github_token = os.environ['GH_TOKEN']
github_workspace = os.environ['GITHUB_WORKSPACE']
github_repository = os.environ['GITHUB_REPOSITORY']
github_event_path = os.environ['GITHUB_EVENT_PATH']
github_event_name = os.environ['GITHUB_EVENT_NAME']

# print environment variables
print(f"GITHUB_WORKSPACE: {github_workspace}")
print(f"GITHUB_REPOSITORY: {github_repository}")
print(f"GITHUB_EVENT_PATH: {github_event_path}")
print(f"GITHUB_EVENT_NAME: {github_event_name}")


def main():
    # Handle repository dispatch events
    if github_event_name == "repository_dispatch":
        # Read in payload
        with open(github_event_path, 'r') as f:
            payload = json.load(f)

        # Initialize GitFlow
        configure_user()  # github-actions[bot]
        # change chdir to github_workspace
        os.chdir(github_workspace)
        git_flow_init(github_repository)

        # Handle start_feature event
        if payload['action'] == "start_feature":

            # Start feature
            start_feature(payload['client_payload']['feature_name'], github_repository)

        # Handle finish_feature event
        elif payload['action'] == "finish_feature":

            # Finish feature
            finish_feature(payload['client_payload']['feature_name'], github_repository)

        # Handle delete_feature event
        elif payload['action'] == "delete_feature":

            # Delete feature
            delete_feature(payload['client_payload']['feature_name'], github_repository)

        # Handle start_release
        elif payload['action'] == "start_release":

            # Start release
            start_release(payload['client_payload']['release_name'], github_repository)

        # Handle finish_release
        elif payload['action'] == "finish_release":

            # Finish release
            finish_release(payload['client_payload']['release_name'], github_repository)


if __name__ == "__main__":
    main()
