from PIL import Image
import io
import base64

def save_picture(b64image, folder, fname):
    byte_picture = base64.b64decode(b64image)
    picture = Image.open(io.BytesIO(byte_picture))
    if picture.format == "JPEG":
        picture.close()
        file = open(fname + ".jpg", "wb")
        file.write(byte_picture)
        print(picture.format)
        print("format JPEG")

    else:
        picture.save(fname+".jpg")
