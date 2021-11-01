from PIL import Image
import warnings
import torchvision.transforms as transforms
import torch
import torch.nn.functional as F
import os

warnings.filterwarnings("ignore")

INPUT_SIZE = 224
TRANSFORM = transforms.Compose([
    transforms.Resize((INPUT_SIZE, INPUT_SIZE)),
    transforms.ToTensor()
])

POS_THRESHOLD = 0.55 #NOTE: Most important param
NOISE_SCALE_FACTOR = 5
PIC_COUNT = 1


def predict(image_path, model):
    with torch.no_grad():
        lst = []
        image = TRANSFORM(Image.open(image_path).convert("RGB")).unsqueeze(0)
        prediction = model.encoder(image)
        return prediction

def binarise(prediction):
    return (F.sigmoid(prediction) > POS_THRESHOLD).int().squeeze(0)

def soft_max_squeeze(prediction):
    return F.sigmoid(prediction).squeeze(0)

def get_labels(pred):
    file = open(os.getcwd()+'/models/ingredient_labels.txt', 'r')
    label_names = [line.rstrip() for line in file.readlines()]
    predicted_labels = []
    for i in range(len(pred)):
        if pred[i] == 1:
            predicted_labels.append(label_names[i])
    return predicted_labels

