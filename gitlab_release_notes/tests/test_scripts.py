from subprocess import run

def test_generate_release_notes():
    run(['gitlab-release-notes', '14117', '--url', 'https://gitlab.in2p3.fr'])

