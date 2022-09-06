
from __future__ import absolute_import
from flask import Flask

app = Flask(__name__)

# import view app initialized
# Flask use this line to find routes
import bworker_views

