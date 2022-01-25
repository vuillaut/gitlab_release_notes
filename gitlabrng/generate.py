import gitlab
from datetime import datetime


def generate_release_notes(project_id, **config):
    """
    Generate the release notes of a gitlab project from the last release

    Parameters
    ----------
    project_id: int
        ID of the project
    config: dict
        url: Optional[str] = None,
        private_token: Optional[str] = None,
        oauth_token: Optional[str] = None,
        job_token: Optional[str] = None,
        ssl_verify: Union[bool, str] = True,
        http_username: Optional[str] = None,
        http_password: Optional[str] = None,
        timeout: Optional[float] = None,
        api_version: str = '4',
        session: Optional[requests.sessions.Session] = None,
        per_page: Optional[int] = None,
        pagination: Optional[str] = None,
        order_by: Optional[str] = None,
        user_agent: str = 'python-gitlab/3.1.0',
        retry_transient_errors: bool = False,
    """
    endstr = '    <br>'

    gl = gitlab.Gitlab(**config)
    project = gl.projects.get(project_id)

    if not project.mergerequests.list(state='merged'):
        raise ValueError(f"There is not merged merge request for project {project_id} {project.name}")

    if not project.releases.list():
        log = f"Changelog of {project.name}:{endstr}"
    else:
        last_release = project.releases.list()[0]
        log = f"Changelog since release {last_release.name} of {project.name}:{endstr}"

    print(log)
    page = 0
    list_mrs = project.mergerequests.list(state='merged',
                                          order_by='updated_at',
                                          updated_after=last_release.released_at,
                                          page=page)
    if not list_mrs:
        raise ValueError(f"There is no merged merge request after the last release {last_release.name}")

    while list_mrs:
        for mr in list_mrs:
            line = f" * {mr.title} (@{mr.author['username']}){endstr}"
            log += line
            print(line)

        page += 1
        list_mrs = project.mergerequests.list(state='merged',
                                              order_by='updated_at',
                                              updated_after=last_release.released_at,
                                              page=page
                                              )

    return log


def main():
    import argparse
    parser = argparse.ArgumentParser("Generate release notes for a gitlab repository \
                                    based on merge requests titles since last release")

    # Required
    parser.add_argument("project_id", type=int)
    # Optional
    parser.add_argument("--url", default="https://gitlab.com", required=False)
    parser.add_argument("--private_token", type=str, required=False, default=None)

    args = parser.parse_args()

    notes = generate_release_notes(args.project_id, url=args.url, private_token=args.private_token)


if __name__ == "__main__":
    main()
