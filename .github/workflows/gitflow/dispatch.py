import requests
import logging

logger = logging.getLogger(__name__)


class DispatchTriggerError(Exception):
    """Custom exception for errors encountered while triggering a repository dispatch event."""
    pass


class InvalidTokenError(DispatchTriggerError):
    """Custom exception for errors encountered when the token is invalid."""
    pass


class RepositoryNotFoundError(DispatchTriggerError):
    """Custom exception for errors encountered when the repository cannot be found."""
    pass


class EventTypeNotFoundError(DispatchTriggerError):
    """Custom exception for errors encountered when the event type is not recognized."""
    pass


def trigger_repository_dispatch(repository, event_type, access_token, payload=None):
    """Helper function for triggering a repository dispatch event.

    Args:
        repository (str): The repository in the format 'OWNER/REPO'.
        event_type (str): The type of event to trigger.
        access_token (str): The GitHub API access token.
        payload (dict, optional): The payload to send with the event. Defaults to None.

    Returns:
        None

    Raises:
        InvalidTokenError: If the access token is invalid.
        RepositoryNotFoundError: If the repository cannot be found.
        EventTypeNotFoundError: If the event type is not recognized.
        DispatchTriggerError: If any other error is encountered while triggering the event.
    """
    url = f"https://api.github.com/repos/{repository}/dispatches"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {access_token}"
    }
    data = {"event_type": event_type}
    if payload:
        data["client_payload"] = payload

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        logger.info(f"Repository dispatch event '{event_type}' triggered successfully for repository '{repository}'.")
    except requests.exceptions.HTTPError as error:
        if response.status_code == 401:
            raise InvalidTokenError("The access token is invalid.")
        elif response.status_code == 404:
            raise RepositoryNotFoundError(f"The repository '{repository}' cannot be found.")
        elif response.status_code == 422:
            raise EventTypeNotFoundError(f"The event type '{event_type}' is not recognized.")
        else:
            raise DispatchTriggerError(
                f"An error occurred while triggering the repository dispatch event '{event_type}': {error}")
