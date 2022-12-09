from django.shortcuts import render
from django.conf import settings
from .forms import ImageForm
from .models import Image as modelI
import base64
import json
import io
import os
import requests
import numpy as np
from PIL import Image

def image_upload_view(request):
    url = 'https://resnet-service-roycard0828.cloud.okteto.net/v1/models/resnet:predict'
    """Process images uploaded by users"""

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            #img_obj = form.instance
            image = modelI.objects.last()
            url_image = "http://127.0.0.1:8000{}".format(image.image.url)
            dl_request = requests.get(url_image, stream=True)
            dl_request.raise_for_status() 
            
            jpeg_bytes = base64.b64encode(dl_request.content).decode("utf-8")
            predict_request = '{"instances": [ {"b64": "%s"} ]}' % jpeg_bytes
            response = requests.post(url, data=predict_request)
            prediction = response.json()['predictions'][0]['classes']
            print(prediction)
            
            file_path = os.path.join(settings.BASE_DIR, 'public/imagenet_class_index.json')
            f = open(file_path)

            data = json.load(f)
            item_prediction = data[str(prediction)]
            name_prediction = item_prediction[1]           

            return render(request, 'resnet/image.html', {'form': form, 'img_obj': image, 'id_prediction': prediction, 'name_prediction': name_prediction})
    else:
        form = ImageForm()
    return render(request, 'resnet/image.html', {'form': form})
  