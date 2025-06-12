from flask import Flask, render_template, request
from gitlab_release_notes import generate_release_notes

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('form.html')


@app.route('/', methods=['POST'])
def release_notes():
    project_id = request.form['project_id']
    url = request.form['url']
    private_token = request.form['private_token']
    target_branch = request.form['target_branch']

    try:
        changelog = generate_release_notes(
            project_id,
            endstr='  <br>',
            since=None,
            url=url,
            private_token=private_token,
            target_branch=target_branch,
        )
        return changelog
    except ValueError as e:
        return f"An error occurred: {str(e)}"
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}") # Good for server-side debugging
        return "An unexpected error occurred. Please check the server logs."


if __name__ == '__main__':
    app.run(debug=False)
