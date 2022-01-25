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
    gl = gitlab.Gitlab(**config)
    project = gl.projects.get(project_id)

    if not project.mergerequests.list(state='merged'):
        raise ValueError(f"There is not merged merge request for project {project_id} {project.name}")

    last_mr_date = datetime.fromisoformat(project.mergerequests.list(state='merged', order_by='updated_at', per_page=1)[0].merged_at)
    if not project.releases.list():
        last_release_date = datetime(1900, 1, 1)
        log = f"Changelog of {project.name}:\n"
    else:
        last_release =  project.releases.list()[0]
        last_release_date = datetime.fromisoformat(last_release.created_at)
        if last_mr_date < last_release_date:
            raise ValueError(f"There is no merged merge request after the last release {last_release.name}")
        log = f"Changelog since release {last_release.name} of {project.name}:\n"

    print(log)
    page = 0
    while last_mr_date > last_release_date:
        for imr, mr in enumerate(project.mergerequests.list(state='merged', order_by='updated_at', page=page)):
            last_mr_date = datetime.fromisoformat(mr.merged_at)
            if last_mr_date < last_release_date:
                continue
            line = f" * {mr.title} (@{mr.author['username']})"
            log += line
            print(line)
        page+=1
