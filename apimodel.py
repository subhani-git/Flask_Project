import os 
import pymongo 
from pymongo import MongoClient
from os import path
from flask import Flask ,render_template,request , send_from_directory

app = Flask(__name__,static_folder="images")
URI = 'mongodb://127.0.0.1:27017'
Client = pymongo.MongoClient(URI)
DB=Client['Upload_tutorial']
images = DB.images


APP_ROOT= os.path.dirname(os.path.abspath(__file__)) #finding absolute path of the current directory
print('uploadedfiles'+APP_ROOT)

@app.route("/")   #we use route to tell flask what url should trigger our function
def index():

	return render_template("upload.html")

@app.route("/upload",methods =['Post'])
def upload():
	target = os.path.join(APP_ROOT,'images/')
	print('targetfile'+target)
	


	if not os.path.isdir(target):  #make the directory if its not there
		os.mkdir(target)

	for upload in request.files.getlist("file"): #using request methods to take filesname from server 
		print(upload)
		filename=upload.filename
		print('filename'+filename)

		destination="/".join([target,filename]) 


		images.insert_one({"_id":31,"filenames":destination})
		 #seeting detination and concation filename into targersou
		print('destination'+ destination)
		upload.save(destination)
	#return send_from_directory("images",filename)	

	return render_template("Complete.html", image_name=filename)	


@app.route('/upload/<filename>')
def send_image(filename):
	image= images.find_one({"_id":31})
	head,tail = os.path.split(image["filename"])
	print('head'+head)
	print('tail'+tail)
   
	return send_from_directory(head, filename)


@app.route('/gallery')
def get_gallery():
	image_names=os.listdir('./images')
	return render_template("gallery.html",image_names=image_names)	

if __name__ == '__main__':
	
	app.run(port=4555, debug=True)	