import numpy as np
# from keras.preprocessing import image
from tensorflow.keras.preprocessing import image
from keras.models import model_from_json
import os
from flask import Flask, render_template, flash, request, redirect, url_for
  
app = Flask(__name__)
app.secret_key = "123"
    
app.config['UPLOAD_FOLDER'] = "static/images"
  
@app.route('/') 
def index():
    return render_template('index1.html')

# @app.route('/upload', methods=['POST'])  
# def upload():
#     file = request.files['file']
#     # do something with the file here, such as save it to disk
#     return 'File uploaded successfully!' 
 
@app.route("/upload", methods=['GET','POST'])
def upload():
    if request.method=='POST':
        upload_image=request.files['upload_image']
        print("first")
        if upload_image.filename!='':
            print("second")
            filepath=os.path.join(app.config["UPLOAD_FOLDER"], upload_image.filename)
            print(filepath)
            upload_image.save(filepath)
            path=filepath
            flash("File Upload Successfully", "success")
    return redirect(url_for("display_image",mess=path))

@app.route('/display')
def display_image():
    json_file = open('model1.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    loaded_model.load_weights("model1.h5")
    print("Loaded model from disk")
    label = ["Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___Healthy",
             "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Corn_(maize)___Common_rust_",
             "Corn_(maize)___Healthy", "Corn_(maize)___Northern_Leaf_Blight", "Grape___Black_rot",
             "Grape___Esca_(Black_Measles)", "Grape___Healthy", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
             "Potato___Early_blight", "Potato___Healthy", "Potato___Late_blight", "Tomato___Bacterial_spot",
             "Tomato___Early_blight", "Tomato___Healthy", "Tomato___Late_blight", "Tomato___Leaf_Mold",
             "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite", "Tomato___Target_Spot",
             "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus"]

    path2 = request.args.get("mess")

    print(path2)

    test_image = image.load_img(path2, target_size=(128, 128))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = loaded_model.predict(test_image)
    print(result)
    
    return render_template('uploadedImage.html', result=label[result.argmax()],imgh=path2.replace("\\","/"))

    # return label[result.argmax()]

if __name__ == "__main__":
    app.run(debug=True)

