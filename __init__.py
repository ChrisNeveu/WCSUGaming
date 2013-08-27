from flask import Flask, render_template, request, session, \
                  g, redirect, url_for, abort, flash
from flaskext.creole import Creole

app = Flask(__name__)
app.config.from_object("WCSUGaming.config")

creole = Creole(app)

import WCSUGaming.views