from flask import Flask,render_template,request,redirect
import requests
from anton import Anton

app  = Flask(__name__)
myanton = Anton()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    source = request.args.get("source")
    if source == None:
        return {"SCC":False,"out":[]}
    city = request.args.get("city")
    state = request.args.get("state")
    if city == None or state == None:
        return {"SCC":False,"out":[]}
    data= []
    if source =="zillow":
        data = myanton.getZillowData(city=city,state=state,)
    if source =="realtor":
        data = myanton.getData(city=city,state=state)

    return {"SCC":True,"out":data}

if __name__ == "__main__":
    app.run(debug=True)
