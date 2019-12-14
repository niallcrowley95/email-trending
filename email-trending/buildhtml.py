from flask import render_template, Flask

# app = Flask(__name__)
#
# from app import routes
#
# from app import app
#
# @app.route('/')
# @app.route('/templates')
def get_full(style, sections):
    """
    Build and returns entire html email
    """
    email_html = render_template("templates/fullpage.html",
                                 style=style,
                                 sections=sections)
    return email_html
