import os
import server
import model

with server.app.app_context():
    os.system("dropdb melons")
    os.system("createdb melons")

    model.connect_to_db(server.app)
    model.db.create_all()

    user1 = model.User(username="user1")
    model.db.session.add(user1)
    model.db.session.commit()