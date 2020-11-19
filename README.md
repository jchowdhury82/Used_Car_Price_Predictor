# Springboard_Capstone_UsedCar

curl --header "Content-Type: application/json" \
  --request GET \
  --data '{"year" : 2014, 
            "make" : "toyota", 
            "model" : "corolla", 
            "trim" : "le plus", 
            "odometer" : 20700, 
            "state" :  "AZ", 
            "colorexterior" : "blue", 
            "colorinterior" : "black", 
            "accidenthist" : "n",
            "owner" : 5, 
            "usage" : "personal"}' \
  http://0.0.0.0:5000/getPrice



HealthCheck URL:

curl --request GET http://127.0.0.1:5001/healthcheck


GetPrice URL:

curl -d @input.json -H "Content-Type: application/json" -X POST http://127.0.0.1:5001/getPrice
