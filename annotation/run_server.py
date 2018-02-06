import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from annotation.application.application import app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)
