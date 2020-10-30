from flask import Flask, request
from CustomTransformers import *

app = Flask(__name__)

# health route return a 200
# POST and use if statement to check mime type - csv (batch) or json - flexible option to download
# writeen to sharted location

# docker compose
# nginx
# onboarding doc

@app.route("/getPrice", methods = ['GET'])
def getPrice():
    req_data = request.get_json()
    df = pd.DataFrame.from_dict(req_data, orient='index').T
    df_final = model_pipeline.transform(df)
    Y = stack_model.predict(df_final)
    return f'\n\n The predicted price is: {Y[0]} \n\n\n'

# wsgy load balancing
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,threaded=False,debug=False)

