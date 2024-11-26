"""App Entrypoint"""

import os
from src.app import create_app, db
from src.app.models.user import create_superadmin

app = create_app()

with app.app_context():
    db.create_all()
    create_superadmin()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "True").capitalize() == "True")
