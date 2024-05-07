
from flask import Flask,redirect,url_for,render_template,request,session,jsonify
from Search_full_code import search_model,search_algo
import json
from datetime import timedelta
app = Flask(__name__)
app.config["SECRET_KEY"]= "quoccr7"
app.permanent_session_lifetime = timedelta(seconds=20)
@app.route('/quoc')
def hello_world():
    return "<h1> Vienam1 </h1>"

@app.route('/admin', methods = ["POST","GET"])
def helloadmin():
    if request.method == "POST":
        username = request.form["name"]
        session["user"]=username
        session.permanent=True
        return redirect(url_for("user",name=username))
    if "user" in session:
        return redirect(url_for("user",name=session["user"]))
    return render_template("home.html")

@app.route('/user')
def user():
    if "user" in session:
        name = session["user"]
        return f"<h1>Xin chao {name} </h1>"
    return redirect(url_for("helloadmin"))
    

@app.route('/login')
def hello():
    return redirect(url_for("helloadmin"))

@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect(url_for("helloadmin"))

@app.route("/data",methods=["POST"])
def get_data():
    inputdata=request.data.decode("utf-8")
    respond= search_algo(inputdata)
    return jsonify(respond)

if __name__ =="__main__":
    app.run(debug=True)
    