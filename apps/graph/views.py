from flask import Blueprint, render_template

graph = Blueprint(
    "graph",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@graph.route("/graphs", methods=["POST"])
def graphs():
    return render_template("graphs.html")


