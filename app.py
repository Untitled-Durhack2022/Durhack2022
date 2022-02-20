from pyexpat import model
from flask import Flask, render_template
from flask import request
from model import predict, getRelated

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('ui.html')

@app.route('/submitModelData')
def submitModelData():
   try:
      print(request.args)
      postcode = request.args["pcode"]
      bedrooms = request.args["bedrms"]
      bathrooms = request.args["bthrms"]
      receptions = request.args["rcptns"]
      arguments = [postcode, bedrooms, bathrooms, receptions]
      for arg in arguments:
         if arg == "":
            print(arg)
            raise SyntaxError
   except SyntaxError:
      return "Bad Request", 400

   
   try:
      ## TODO: We may need to change the price
      # estimatedPrice = model.predict(arguments)

      ## TODO: Remove this estimatedPrice with the modelpredict
      estimatedPrice = "£" + str(round(predict(bedrooms, receptions, bathrooms, postcode)))
      medians = getRelated(postcode)
      return estimatedPrice, 200
   except Exception as e:
      return "Internal Server Error", 500

if __name__ == '__main__':
   app.run()
