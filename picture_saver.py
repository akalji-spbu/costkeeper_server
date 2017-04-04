from PIL import Image
import io
import base64

def save_picture(b64image, folder, fname):
    status = True
    response = ""
    byte_picture = base64.b64decode(b64image)
    del b64image
    try:
        picture = Image.open(io.BytesIO(byte_picture))
        if picture.format == "JPEG":
            picture.close()
            del picture
            file = open(fname + ".jpg", "wb")
            file.write(byte_picture)
        else:
            picture.save(fname+".jpg")
    except OSError as e:
        if e.args[0][0:26]=="cannot identify image file":
            status = False
            response = "NON_PICTURE_TYPE"

    return status, response