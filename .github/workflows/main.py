import json
import logging
import os

from gitflow.gitflow import (git_flow_init, start_feature_branch, finish_feature_branch, git_configure)

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


# TODO: Add enforcement of commit message format.
# - https://github.com/lumapps/commit-message-validator

# TODO: Choose bump2version or re-ver and add init action and other.


# TODO: Add re-render actions.

def main():
    # Handle repository dispatch events
    if github_event_name == "repository_dispatch":
        # Read in payload
        with open(github_event_path, 'r') as f:
            payload = json.load(f)
            # pretty print
            print(json.dumps(payload, indent=4, sort_keys=True))

        inputs = payload['client_payload']['inputs']

        # Configure git
        git_configure(key='user.name', value='github-actions[bot]')
        git_configure(key='user.email', value='github-actions@github.com')
        git_configure(key='gitflow.branch.master', value='main')
        git_configure(key='gitflow.branch.develop', value='develop')
        git_configure(key='gitflow.prefix.feature', value='feature/')
        git_configure(key='gitflow.prefix.release', value='release/')
        git_configure(key='gitflow.prefix.hotfix', value='hotfix/')
        git_configure(key='gitflow.prefix.support', value='support/')
        git_configure(key='gitflow.prefix.versiontag', value='v')

        # change chdir to github_workspace
        os.chdir(github_workspace)

        # Handle start_feature event
        if payload['action'] == "start_feature":
            logger.info(f"Creating feature branch feature/{inputs['feature_name']} from develop")
            git_flow_init()
            start_feature_branch(inputs['feature_name'])

        # Handle finish_feature event
        elif payload['action'] == "finish_feature":
            logger.info(f"Merging feature/{inputs['feature_name']} into develop, then deleting feature")
            git_flow_init()
            finish_feature_branch(inputs['feature_name'])

        # Handle start_release event
        elif payload['action'] == "start_release":
            logger.info(f"Creating release branch release/{inputs['release_name']} from develop")
            git_flow_init()
            start_release_branch(inputs['release_name'])


if __name__ == "__main__":
    main()
