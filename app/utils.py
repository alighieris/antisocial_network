from base64 import b64encode
def render_picture(data):

    render_pic = b64encode(data).decode('ascii') 
    return render_pic

def image2db(file):
	imageData = file.read()
	rendered_image = render_picture(imageData)
	return imageData, rendered_image