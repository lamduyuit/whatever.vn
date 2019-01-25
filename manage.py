# -*- coding: utf-8 -*-
# import io
import os
import sys

from flask_script import Manager, Server
from application import create_app
from flask import redirect

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")
    # return render_template('404.html'), 404


manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 5000)))
)

if __name__ == "__main__":
    manager.run()
