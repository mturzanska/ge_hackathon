from flask import Flask

app = Flask(__name__)
from peacemaker import views
