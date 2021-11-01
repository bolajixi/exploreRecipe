import model
import os
import torch
from label_prediction import get_labels, binarise, soft_max_squeeze,predict
from gc_batch_segmentation import localize_objects, crop_image


model_param_dir = os.getcwd() + "/models/fine_tuned_model.pth"
prediction_model = model.ConvNet(300)
prediction_model.load_state_dict(torch.load(model_param_dir, map_location=torch.device('cpu')))

#TODO remove, outline model architecture.
print(prediction_model.eval())


#loads cached images from the 'image_cache' directory. Assumes these images are a results the segmented out of gcloud.
#outputs a list of predicted food labels
def load_predictions():
    source_path = os.getcwd() + "/image_cache/"
    images = [source_path + str(img) for img in os.listdir(source_path)]
    predictions = []

    for image in images:
        predicted_ingredients = predict(image, prediction_model)
        predicted_ingredients = soft_max_squeeze(predicted_ingredients)
        predictions += get_labels(binarise(predicted_ingredients))
    return predictions


#segments provided images based on bounding boxes predicted from gclooud.
#no return value, override images present in 'image_cache'

def segment_image(image_path):
    crop_image(image_path, localize_objects(image_path))


#to run just execute 'segment_image' then detect labels from the segments using 'load_predictions'