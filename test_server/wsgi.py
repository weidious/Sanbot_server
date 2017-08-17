import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from test_server import application
from werkzeug.contrib.fixers import ProxyFix

application.wsgi_app = ProxyFix(application.wsgi_app)

if __name__ == "__main__":
    application.run(threaded=True)
