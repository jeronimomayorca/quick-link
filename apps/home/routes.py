# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import string
import random
from apps.home import blueprint
from flask import app, redirect, render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound

shortened_urls = {}


@blueprint.route("/home")
def index():
    return render_template("home/home.html", segment="home")


@blueprint.route("/", methods=["POST", "GET"])
def shorten_url():
    if request.method == "POST":
        long_url = request.form["long_url"]
        short_url = generate_short_url()
        while short_url in shortened_urls:
            short_url = generate_short_url()

        shortened_urls[short_url] = long_url
        print(long_url)
        return f"Shortened URL: {request.url_root}{short_url}"
    return render_template("home/home.html", segment="home")


@blueprint.route("/<template>")
@login_required
def route_template(template):

    try:

        if not template.endswith(".html"):
            template += ".html"

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template("home/page-404.html"), 404

    except:
        return render_template("home/page-500.html"), 500


@blueprint.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL Not Found", 404


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split("/")[-1]

        if segment == "":
            segment = "index"

        return segment

    except:
        return None


def generate_short_url(lenght=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(lenght))

    return short_url
