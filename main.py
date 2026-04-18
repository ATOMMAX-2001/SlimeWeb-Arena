from slimeweb import Slime
from slimeweb.slime import SlimeCompression
import json


app = Slime(__file__)


def load_json_processing_file():
    with open("dataset.json","r") as file:
        return json.load(file)


JSON_DATASET = load_json_processing_file()




@app.route("/baseline11",method=["GET","POST"])
def baseline_test(req,resp):
    if req.method == "GET":
        result = 0
        for q_val in req.query.values():
            try:
                result += int(q_val)
            except ValueError: pass
        return resp.plain(str(result))
    else:
        result =0
        for q_val in req.query.values():
            try:
                result +=int(q_val)
            except ValueError: pass
        try:
            result += int(req.text)
        except ValueError: pass
        return resp.plain(str(result))


@app.route("/pipeline",method="GET")
def pipeline_test(req,resp):
    return resp.plain("ok")

# body_size by default it will read 10MB
# setting read_size as 25MB
@app.route("/upload",method="POST",body_size=1024*1024*25)
def upload_test(req,resp):
    result = len(req.body)
    return resp.plain(str(result))



@app.route("/json/{count}",method="GET",compression=SlimeCompression.Gzip,comp_level=1)
def json_test(req,resp):
    global JSON_DATASET
    count = int(req.params["count"])
    multiplier = int(req.query["m"])
    result =[]
    for data in JSON_DATASET[:count]:
        result.append({
            "id":data["id"],
            "name":data["name"],
            "category":data["category"],
            "price": data["price"],
            "quantity": data["quantity"],
            "active": data["active"],
            "tags": data["tags"],
            "rating": {
                "score":data["rating"]["score"],
                "count": data["rating"]["count"],
            },
            "total": data["price"] * data["quantity"] * multiplier

        })
    return resp.json({"items":result,"count":count})


# Websocket in slime are event driven so had to create handler 
# message event
@app.websocket("/ws")
def websocket_test(req,resp):
    def echo_me(msg):
        resp.send(msg)
    resp.on_message(echo_me)



if __name__ == "__main__":
    app.serve(dev=True)
