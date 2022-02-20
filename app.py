from pyexpat import model
from flask import Flask, render_template
from flask import request
app = Flask(__name__)

##TODO:

def trainModel():
   ## TOOD: Wait on Tristan to finish
   ...
   return model

model = trainModel()

@app.route('/')
def home():
   return render_template('ui.html')

@app.route('/submitModelData')
def submitModelData():
   try:
      postcode = request.args["pcode"]
      bedrooms = request.args["bedrms"]
      bathrooms = request.args["bthrms"]
      receptions = request.args["rcptns"]
      for arg in arguments:
         if arg == "":
            raise Exception
   except:
      return "Bad Request", 400

   arguments = [postcode, bedrooms, bathrooms, receptions]
   
   try:
      ## TODO: We may need to change the price
      estimatedPrice = model.predict(arguments)
      return estimatedPrice
   except Exception:
      return "Internal Server Error", 500



if __name__ == '__main__':
   app.run()

