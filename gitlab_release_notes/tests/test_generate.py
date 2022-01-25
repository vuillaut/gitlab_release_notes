from gitlab_release_notes import generate_release_notes


def test_generate_release_notes():
    # TODO: replace with a dedicated test repo
    notes = generate_release_notes(14117, url='https://gitlab.in2p3.fr')
