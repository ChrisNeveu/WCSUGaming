from flask import Flask, render_template, request, session, \
                  g, redirect, url_for, abort, flash

app = Flask(__name__)
app.config.from_object("WCSUGaming.config")

import WCSUGaming.views