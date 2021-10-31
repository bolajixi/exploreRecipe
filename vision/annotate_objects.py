import json
import urllib.request as urllib2
import requests
from io import StringIO  
from contextlib import closing
import argparse
from PIL import Image
from PIL import ImageDraw
from google.cloud import vision

client = vision.ImageAnnotatorClient()

def highlight_objects(image_url, objects, output_filename):
    
    with closing(urllib2.urlopen(image_url)) as img:
        if img.headers.maintype != "image":
            raise TypeError("Invalid filetype given")
        img_file = StringIO(img.read())

    im = Image.open(img_file)
    draw = ImageDraw.Draw(im)

    for face in objects["responses"][0]["cropHintsAnnotations"]:
        box = [(v.get("x", 0.0), v.get("y", 0.0)) for v in
               face["boundingPoly"]["vertices"]]
        draw.line(box + [box[0]], width=5, fill="#00ff00")

    del draw
    im.save(output_filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Detection in the given image."
    )
    parser.add_argument(
        "-i", "--image_url",
        help="The image URL to send to Google Cloud Vision API ",
        required=True
    )
    parser.add_argument(
        "-m", "--max_results",
        help="max entities to detect. Default: %(default)s",
        default=4,
        type=int
    )
    parser.add_argument(
        "-e", "--endpoint",
        help="The API endpoint to use",
        required=True
    )
    parser.add_argument(
        "-o", "--output",
        help="The filename of the output. Default: %(default)s",
        default="images/annotated_image.jpg"
    )

    args = parser.parse_args()

    post_params = {
        "image_url": args.image_url,
        "detect_type": "OBJECT_LOCALIZATION",
        "max_results": args.max_results
    }
    r = requests.post(args.endpoint,
                      data=json.dumps(post_params),
                      headers={'content-type': 'application/json'})
    detection_results = r.json()

    highlight_objects(args.image_url, detection_results, args.output)