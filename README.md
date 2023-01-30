# GitFlow Workflows

GitFlow is a popular Git branching model used for software development. It defines a strict branching model designed around the project release.

## Develop Workflow
The develop branch is where active development takes place. All feature branches are created from develop, and merged back into develop when complete. The Develop Workflow is initiated with the `start_feature` action, which creates a new feature branch. The feature branch is then tested and merged back into develop with the `finish_feature` action.

A dev_release (unstable) can also be created from develop with the `unstable_release` action. This will create a new branch named `dev_release`, which is used to finalize and test a release before merging back into develop and main. The version bump, whether it be a major, minor or patch update, should be specified during the `unstable_release` action.

## Feature Workflow
The feature workflow applies to the feature branches created from develop. The `finish_feature` action is used to merge the feature branch back into develop. Before merging, the feature branch should be tested using the `test_feature` action.

## Release Workflow
The release workflow applies to the `dev_release` branch, created from develop. The `finalize_release` action is used to merge the `dev_release` branch back into develop and main.

## Hotfix Workflow
The hotfix workflow is initiated when an issue is detected in the main branch. A hotfix branch is created from main, and the issue is fixed. The `finish_hotfix` action is then used to merge the hotfix branch back into both develop and main.

It is important to note that changes should never be directly made to the main branch. All changes should be made in a feature or hotfix branch, and then merged into main via a pull request.

## This Repository 
This GitHub repository has been set up with actions to automate the GitFlow workflow process, making it easier to follow the branching model. The individual workflows are defined in the following files:

- `gitflow_develop.yaml`
- `gitflow_feature.yaml`
- `gitflow_release.yaml`
- `gitflow_hotfix.yaml`

To use the GitFlow workflows, simply navigate to the Actions tab in the repository, and choose the appropriate workflow based on the branch you are working on.
