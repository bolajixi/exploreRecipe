import base64
import os
from google.cloud import vision
import cv2
import numpy as np
from PIL import ImageDraw


def encode_image(image):
  image_content = image.read()
  return base64.b64encode(image_content)

def draw_boxes(image, bounds, color,width=5):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        draw.line([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y,
            bound.vertices[0].x, bound.vertices[0].y],fill=color, width=width)
    return image


def localize_objects(path):

    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    output = []
    for object_ in objects:
        #print('\n{} (confidence: {})'.format(object_.name, object_.score))
        #print('Normalized bounding polygon vertices: ')
        vertices = []
        for vertex in object_.bounding_poly.normalized_vertices:
            vertices.append([vertex.x, vertex.y])
        #    print(' - ({}, {})'.format(vertex.x, vertex.y))
        output.append([vertices])

    return np.asarray(output)



path = os.getcwd()+"/images/image_02.jpg"
#localize_objects(path)

def crop_image(image, vertices):
    """
    Crop an image using the provided vertices.
    """
    # Create a mask with the same dimensions as the input image.
    mask = np.zeros(image.shape, dtype=np.uint8)
    #get image shape
    h, w, c = image.shape
    # Fill the mask with white polygon.
    vertices = (vertices * np.array([[h, w]])).astype(np.int32)
    cv2.fillPoly(mask, vertices, (255, 255, 255))
    print(vertices)
    # Apply the mask to the input image.

    #NOTE: ignored bitwise mask due to scaling issues.
    #result = cv2.bitwise_and(image, mask)
    count = 1
    for vertex in vertices:
        Y = vertex[0][0][1]
        X = vertex[0][0][0]
        H = vertex[0][3][1]
        W = vertex[0][1][0]
        save_dir = os.getcwd() + "/image_cache/image_" + str(count) + ".jpg"
        count += 1
        cv2.imwrite(save_dir,image[X:X+W, Y:Y+H])

# Test the function.
image = cv2.imread('images/image_02.jpg')
objects = localize_objects(os.getcwd()+"/images/image_02.jpg")
crop_image(image, objects)



"""

Gcloud output example 


Lemon (confidence: 0.8731716275215149)
Normalized bounding polygon vertices: 
 - (0.5756075978279114, 0.49277710914611816)
 - (0.7025125026702881, 0.49277710914611816)
 - (0.7025125026702881, 0.7706408500671387)
 - (0.5756075978279114, 0.7706408500671387)

Food (confidence: 0.7212815284729004)
Normalized bounding polygon vertices: 
 - (0.00225278758443892, 0.6021723747253418)
 - (0.12584806978702545, 0.6021723747253418)
 - (0.12584806978702545, 0.9256262183189392)
 - (0.00225278758443892, 0.9256262183189392)


"""



