from flask import Flask, render_template, request, jsonify, Response
from config_cardata import *
import json


app = Flask(__name__)


# route for health check
@app.route("/healthcheck", methods = ['GET'])
def getHealthCheck():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

# route for form to enter car details for prediction
@app.route("/dataform", methods = ['GET'])
def dataform():
    return render_template('dataform.html')

# route for form to upload car data in csv file for prediction
@app.route("/upload", methods = ['GET'])
def upload():
    return render_template('upload.html')

# route for serving predictions for csv
@app.route("/generatePrices", methods = ['POST'])
def generatePrices():
    content_type = request.mimetype
    try:
        if content_type == 'multipart/form-data':
            f = request.files['file']
            df = pd.read_csv(f.stream)
    except Exception as e:
        response_message = 'ERROR in parsing file. Please contact the administrator. ' + e

    else:
        try:
            df_final = cardata_transform_pipeline.transform(df)
            Y = stack_model.predict(df_final)
            df['predicted_price'] = Y
        except Exception as e:
            response_message = 'ERROR in prediction. Please contact the administrator. ' + e

    finally:
        return Response(df.to_csv(),
                        mimetype="text/csv",
                        headers={"Content-disposition": "attachment; filename=carprice_predictions.csv"})


# route for serving predictions for single requests from forms or from curl/postman (API)
@app.route("/getPrice", methods = ['POST'])
def getPrice():
    content_type = request.mimetype
    response_message = None
    try:
        # if the request is from a web form
        if content_type == 'application/x-www-form-urlencoded':
            year = int(request.form.get("year"))
            make = request.form.get("make")
            model = request.form.get("model")
            trim = request.form.get("trim")
            odometer = int(request.form.get("odometer"))
            state = request.form.get("state")
            colorexterior = request.form.get("colorexterior")
            colorinterior = request.form.get("colorinterior")
            accidenthist = request.form.get("accidenthist")
            owner = int(request.form.get("owner"))
            usage = request.form.get("usage")
            df = pd.DataFrame(columns =  ['year','make','model','trim','odometer','state','colorexterior','colorinterior','accidenthist','owner','usage'])
            df.loc[0] = [year,make,model,trim,odometer,state,colorexterior,colorinterior,accidenthist,owner,usage]
        # if the request is an API call with json
        elif content_type == 'application/json':
            json_data = request.get_json()
            df = pd.DataFrame([json_data])

    except Exception as e:
        response_message = 'ERROR in parsing data. Please contact the administrator. ' + e

    else:
        try:
            df_final = cardata_transform_pipeline.transform(df)
            Y = stack_model.predict(df_final)
            response_message = f'The predicted price for this car is : {Y[0]:.0f}'
        except Exception as e:
            response_message = 'ERROR in prediction. Please contact the administrator. ' + e

    finally:
        return jsonify(response = response_message)

# wsgy load balancing
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=False)

