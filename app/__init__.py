from flask import Flask,Blueprint
from app.views.incidents import incident
from app.views.users import user

app=Flask(__name__)
app.register_blueprint(incident)
app.register_blueprint(user)
