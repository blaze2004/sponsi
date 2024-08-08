"""App Entrypoint"""

import os
from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "True").capitalize() == "True")
