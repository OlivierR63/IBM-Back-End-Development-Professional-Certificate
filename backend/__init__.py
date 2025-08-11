from flask import Flask

# Create Flask application
app = Flask(__name__)

# Import application routes AFTER the Flask app instance is created.
# This line is crucial for Flask to discover and register the routes
# defined in 'routes.py'.
#
# The '# noqa: F401, E402' directive is added for linters like Flake8.
# - F401: Disables the "module imported but unused" warning. Although
#         'routes' isn't directly referenced in this file, importing it
#         executes the code within 'routes.py', which in turn configures
#         the URL paths using Flask's decorators (e.g., @app.route()).
#         Thus, the import is functionally necessary.
# - E402: Disables the "module level import not at top of file" warning.
#         The import of 'routes' is intentionally placed here AFTER the
#         'app' instance is created. This is a common practice in Flask
#         to prevent circular import issues. If 'routes.py' needs the
#         'app' object (which is typical for defining routes), and 'routes'
#         were imported before 'app' was fully defined, it would lead to
#         an import error.
from backend import routes  # noqa: F401, E402
