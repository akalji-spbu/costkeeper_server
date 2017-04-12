from PIL import Image
import io

def save_b64_picture(b64image, folder, fname):
    import base64
    status = True
    response = ""
    byte_picture = base64.b64decode(b64image)
    del b64image
    try:
        picture = Image.open(io.BytesIO(byte_picture))
        if picture.format == "JPEG":
            picture.close()
            del picture
            file = open(folder + fname + ".jpg", "wb")
            file.write(byte_picture)
            file.close()
        else:
            picture.save(folder + fname+".jpg")
    except OSError as e:
        if e.args[0][0:26] == "cannot identify image file":
            status = False
            response = {
                "STATUS":"ERROR_NON_PICTURE_TYPE"
            }

    return status, response

def save_url_picture(url, folder, fname):
    import urllib.request
    status = True
    response = ""
    try:
        byte_picture = urllib.request.urlopen(url).read()
    except:
        pass

    try:
        picture = Image.open(io.BytesIO(byte_picture))
        if picture.format == "JPEG":
            picture.close()
            del picture
            file = open(folder + fname + ".jpg", "wb")
            file.write(byte_picture)
            file.close()
        else:
            picture.save(folder + fname+".jpg")
            picture.close()
    except OSError as e:
        if e.args[0][0:26]=="cannot identify image file":
            status = False
            response = {
                "STATUS": "ERROR_NON_PICTURE_TYPE"
            }

    return status, response