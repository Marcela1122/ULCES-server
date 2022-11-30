#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 12:34:37 2022

Server ULCES
"""

from flask import request, Blueprint, jsonify
from flask import current_app as app
from werkzeug.utils import secure_filename
import os
import imageio.v2 as imageio
from Homogenization_functions import enhance_image
import matplotlib.pyplot as plt
from datetime import datetime

# TODO: Handle image processing outside of the uploader function. That is, create a separate function.
# TODO: Resize rendered images to be the same size as input images (original/raw).


bp_image = Blueprint('bp_image', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@bp_image.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response
'''
    ---------------------------------------------------------------------------
         Register a function to run after each request to this object
    ---------------------------------------------------------------------------

    The function is called with the response object, and must return a response object.
    This allows the functions to modify or replace the response before it is sent.
'''


# Make sure the input files are image files:
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# To upload the image and process it:
@bp_image.route("/upload", methods=['POST'])
def uploader():
    if request.method == 'POST' and 'archivo' in request.files:
        file = request.files['archivo']

        now = datetime.now()

        args = request.form.to_dict()
        dni = args.get("dni")
        opt1 = args.get("opt1")
        opt2 = args.get("opt2")
        opt3 = args.get("opt3")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename1 = secure_filename(str(now.day) + str(now.month) + str(now.year) + str(now.hour) + "_" + str(dni) + "." + str(filename).split('.')[1])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            image = imageio.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

            parameters = {}
            parameters['mid_tones'] = 0.5
            parameters['tonal_width'] = 0.5
            parameters['areas_bright'] = 0.0
            parameters['brightness'] = 0.13
            parameters['preserve_tones'] = True
            parameters['color_correction'] = False

            if opt1.lower() == "true":
                parameters['local_contrast'] = 1.0
                parameters['areas_dark'] = 0.0
                parameters['saturation_degree'] = 1.0

                photo = str(filename1).split('.')[0] + "_OPT1enhanced." + str(filename1).split('.')[1]
                image_enhanced = enhance_image(image, parameters, verbose=False)
                dir_name = app.config['UPLOAD_FOLDER']
                plt.rcParams["savefig.directory"] = os.chdir(dir_name)
                plt.imshow(image_enhanced, vmin=0, vmax=255)
                plt.axis('off')
                plt.savefig(photo, transparent=True, bbox_inches='tight', pad_inches=0)

            if opt2.lower() == "true":
                parameters['local_contrast'] = 0.0
                parameters['areas_dark'] = 1.0
                parameters['saturation_degree'] = 0.5

                photo2 = str(filename1).split('.')[0] + "_OPT2enhanced." + str(filename1).split('.')[1]

                image_enhanced2 = enhance_image(image, parameters, verbose=False)

                plt.imshow(image_enhanced2, vmin=0, vmax=255)
                plt.axis('off')
                plt.savefig(photo2, transparent=True, bbox_inches='tight', pad_inches=0)

            if opt3.lower() == "true":
                parameters['local_contrast'] = 1.5
                parameters['areas_dark'] = 0.5
                parameters['saturation_degree'] = 1.2

                photo3 = str(filename1).split('.')[0] + "_OPT3enhanced." + str(filename1).split('.')[1]

                image_enhanced3 = enhance_image(image, parameters, verbose=False)
                plt.imshow(image_enhanced3, vmin=0, vmax=255)
                plt.axis('off')
                plt.savefig(photo3, transparent=True, bbox_inches='tight', pad_inches=0)

            else:
                print('Please, choose an option')

        else:
            print('File invalid')
        # return redirect(url_for('bp_main.upload_file'))
        return jsonify({'Image_processed':'successfully'})

'''
    ---------------------------------------------------------------------------
         Upload the input image to the "photos" folder and processes it.
    ---------------------------------------------------------------------------
The input image is saved in the folder called "photos". This image is renamed with the following format: 
daymonthyeartime_DNI.Extension. 

The DNI is information supplied by the user, and like the choice of processing options, it is stored within the "args" variable.
 
Depending on the processing option chosen, the processed images will be saved inside the same folder as the original 
image with the aforementioned format + "OPT" # (processing option number) + the word "enhanced". 
   
    OUTPUT
    ------
    Two, three or four images: original and processed image(s) in the "photos" folder.
    The user can choose, within three processing options, how they prefers the output image.
    All three options have set parameters.

    '''

'''
BIBLIOGRAPHY: 

1. API (no date) API - Flask Documentation (2.2.x). Available at: https://flask.palletsprojects.com/en/2.2.x/api/ 
'''