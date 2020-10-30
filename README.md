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
