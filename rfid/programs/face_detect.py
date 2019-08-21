from ibm_watson import VisualRecognitionV3
from PIL import Image
from picamera import PiCamera


visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='hgkvHWd0-DONvE2iStjGODSek8A9g9P7bdeQBkllA3GV')


def face_crop(id, face_location):
    left = face_location['left']
    top = face_location['top']
    img = Image.open('smartaccess/media/tmp.jpg')
    if face_location['width'] >= face_location['height']:
        width = face_location['width']
        height = face_location['width']
    else:
        width = face_location['height']
        height = face_location['height']
    img = img.crop((left, top, left + width, top + height)).resize((300, 300), Image.ANTIALIAS)
    img.save('smartaccess/media/face_crops/{}.jpg'.format(id), "JPEG")
    return 'smartaccess/media/face_crops/{}.jpg'.format(id)


def get_photo_data(id):
    # tmp.jpg is the last shot, it will be overwritten every successful access
    camera = PiCamera()
    camera.capture('smartaccess/media/tmp.jpg')
    camera.close()
    with open('smartaccess/media/tmp.jpg', 'rb') as images_file:
        result = visual_recognition.detect_faces(images_file).get_result()
        try:
            # select the first (and hopefully only) face
            face = result['images'][0]['faces'][0]
            # average the age, pick 'M' or 'F' and extract the crop using face_crop()
            data = {'age': (face['age']['min'] + face['age']['max']) / 2,
                    'sex': face['gender']['gender'][0],
                    'photo': face_crop(id, face['face_location'])}
        except:
            print('Face not detected')
            data = {'age': None,
                    'sex': None,
                    'photo': None}
        return data

