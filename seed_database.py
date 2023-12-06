import os
import server
import model

with server.app.app_context():
    os.system("dropdb melons")
    os.system("createdb melons")

    model.connect_to_db(server.app)
    model.db.create_all()