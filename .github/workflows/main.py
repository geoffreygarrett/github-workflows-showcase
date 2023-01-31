import os
import sys
import json 
import subprocess

# Get environment variables
github_token = os.environ['GH_TOKEN']
github_workspace = os.environ['GITHUB_WORKSPACE']
github_repository = os.environ['GITHUB_REPOSITORY']
github_event_path = os.environ['GITHUB_EVENT_PATH']
github_event_name = os.environ['GITHUB_EVENT_NAME']

def run_command(command):
    # Function to run shell commands
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr

def git_flow_init():
    # Initialize GitFlow on repository
    run_command(f"git clone https://x-access-token:{github_token}@github.com/{github_repository}.git {github_workspace}")
    os.chdir(github_workspace)
    run_command("git flow init -d")

def start_feature(feature_name):
    # Start a new feature in GitFlow
    run_command(f"git flow feature start {feature_name}")
    run_command("git push --set-upstream origin feature/{feature_name}")

def finish_feature(feature_name):
    # Finish a feature in GitFlow
    run_command(f"git flow feature finish {feature_name}")
    run_command("git push")

def delete_feature(feature_name):
    # Delete a feature in GitFlow
    run_command(f"git flow feature delete {feature_name}")

def main():
  # Handle repository dispatch events
  if github_event_name == "repository_dispatch":
    # Read in payload
    with open(github_event_path, 'r') as f:
      payload = json.load(f)
      print(json.dumps(payload, indent=4, sort_keys=True))
        
    # Handle actions based on the payload
    if payload['action'] == 'start_feature':
      feature_name = payload['feature_name']
      git_flow_init()
      start_feature(feature_name)
    elif payload['action'] == 'finish_feature':
      feature_name = payload['feature_name']
      git_flow_init()
      finish_feature(feature_name)
    elif payload['action'] == 'delete_feature':
      feature_name = payload['feature_name']
      git_flow_init()
      delete_feature(feature_name)

if __name__ == "__main__":
  main()
