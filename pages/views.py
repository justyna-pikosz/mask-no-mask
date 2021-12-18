from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import ImageForm
from django.conf import settings

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import numpy as np
import os 

class HomePageView(TemplateView):
    template_name = "home.html"

    def get(self, request):
        form = ImageForm()
        return render(request, self.template_name, {'form': form})


class Detect(TemplateView):
    template_name = "result.html"

    def get(self, request):
        return render(request, self.template_name)


    def post(self, request):
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    form.save()
                except Exception as e:
                    print("yolo")
                    
                img_obj = form.instance
                result = self.whatIsIt(img_obj)
                return render(request, self.template_name, {'form': form, 'img_obj': img_obj, 'result': result})
        else:
            form = ImageForm()
        return render(request, self.template_name, {'form': form})    


    def whatIsIt(self, img_obj):
        model = load_model(os.getcwd() + "/pages/mask_detector.model")
        image = tf.keras.preprocessing.image.load_img(os.getcwd() + img_obj.image.url, target_size=(224, 224))
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.array([input_arr])
        input_arr = input_arr.astype('float32') / 255.  
        preds = model.predict(input_arr)
        for pred in preds:
            (mask, withoutMask) = pred
            return "Mask" if mask > withoutMask else "No Mask"

        return "no result, something went wrong :C"