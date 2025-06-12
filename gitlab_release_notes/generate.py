import datetime
import gitlab
import os.path
import sys
from .version import __version__

def generate_release_notes(project_id, endstr='  <br>', since=None, target_branch=None, **config):
    """
    Generate the release notes of a gitlab project.

    Parameters
    ----------
    project_id: int
        ID of the project
    endstr: str
        String to use for line endings (e.g., '  <br>' for HTML, '\n' for plain text)
    since: Optional[str]
        A date string (YYYY-MM-DDTHH:MM:SSZ) or a tag/reference.
        If provided, release notes will be generated for MRs merged after this point.
        Overrides fetching MRs since the last release.
    target_branch: Optional[str]
        The target branch to filter merge requests by.
    config: dict
        Additional keyword arguments for the gitlab.Gitlab client, such as:
        url: Optional[str] = None,
        private_token: Optional[str] = None,
        # ... (other gitlab.Gitlab config options)
    """

    gl = gitlab.Gitlab(**config)
    project = gl.projects.get(project_id)

    # Initial check for any merged MRs (can be refined if needed)
    # This check doesn't use target_branch yet, it's a general check.
    # Consider if this check should also incorporate target_branch if provided.
    # For now, keeping it as is.
    initial_mr_check_params = {'state': 'merged', 'per_page': 1}
    if target_branch: # Optionally make the initial check more specific
        initial_mr_check_params['target_branch'] = target_branch
    
    if not project.mergerequests.list(get_all=False, **initial_mr_check_params):
        error_message = f"There are no merged merge requests for project {project_id} ({project.name})"
        if target_branch:
            error_message += f" on branch '{target_branch}'"
        raise ValueError(error_message)

    if since:
        log = f"Changelog of {project.name}"
        if target_branch:
            log += f" for branch '{target_branch}'"
        log += f" since {since}:{endstr}"
        last_date = since # Assuming 'since' is a date string 'YYYY-MM-DDTHH:MM:SSZ'
                          # If 'since' can be a tag, you'd need to resolve its date
    else:
        releases = project.releases.list()
        if not releases:
            log = f"Changelog of {project.name}"
            if target_branch:
                log += f" for branch '{target_branch}'"
            log += f":{endstr}"
            last_date = '0000-01-01T00:00:00Z'
        else:
            last_release = releases[0]
            log = f"Changelog since release {last_release.name} of {project.name}"
            if target_branch:
                log += f" for branch '{target_branch}'"
            log += f":{endstr}"
            last_date = last_release.released_at

    page = 1
    list_mrs_params = {
        'state': 'merged',
        'order_by': 'updated_at',
        'updated_after': last_date,
        # 'scope': 'all' # Ensure we get MRs the user has access to, default is 'created_by_me' or 'assigned_to_me'
                       # The python-gitlab default for list() is all MRs the user can view.
    }
    if target_branch:
        list_mrs_params['target_branch'] = target_branch

    # Fetch the first page
    list_mrs = project.mergerequests.list(page=page, get_all=False, **list_mrs_params)
    
    found_mrs = False
    while list_mrs:
        found_mrs = True
        for mr in list_mrs:
            line = f" * {mr.title} (@{mr.author['username']}){endstr}"
            log += line

        page += 1
        list_mrs = project.mergerequests.list(page=page, get_all=False, **list_mrs_params)

    if not found_mrs:
        no_mrs_message = "There is no new merged merge request"
        if target_branch:
            no_mrs_message += f" for branch '{target_branch}'"
        if since:
            no_mrs_message += f" since {since}."
        else:
            no_mrs_message += f" after {last_date}."
        log += no_mrs_message
        return log

    return log


def main():
    import argparse
    parser = argparse.ArgumentParser("Generate release notes for a gitlab repository \
                                    based on merge requests titles since last release")

    # Required
    parser.add_argument("project_id", type=int)
    # Optional
    parser.add_argument("--url", default="https://gitlab.com", required=False, help="GitLab base URL, e.g., https://gitlab.com")
    parser.add_argument("--private_token", type=str, required=False, default=None, help="GitLab private token")
    parser.add_argument('--version', action='version', version=__version__, help="Show the version and exit")
    parser.add_argument('--html', action='store_true', help="Generate HTML output")
    # Add CLI arguments for since and target_branch if you want to use them from CLI
    parser.add_argument("--since", type=str, required=False, default=None,
                        help="Generate notes since this date (YYYY-MM-DDTHH:MM:SSZ) or tag.")
    parser.add_argument("--target_branch", type=str, required=False, default=None,
                        help="Filter merge requests by target branch.")


    args = parser.parse_args()

    if args.html:
        endstr = '  <br>'
    else:
        endstr = '\n'
    
    # Pass since and target_branch to generate_release_notes
    notes = generate_release_notes(
        args.project_id,
        url=args.url,
        endstr=endstr,
        private_token=args.private_token,
        since=args.since,
        target_branch=args.target_branch
    )
    print(notes)


if __name__ == "__main__":
    main()
