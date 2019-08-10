from ibm_watson import VisualRecognitionV3


visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='hgkvHWd0-DONvE2iStjGODSek8A9g9P7bdeQBkllA3GV')


def face_crop(face_location):
    # TODO implement
    pass


def get_photo_data(id):
    with open('smartaccess/media/tmp.jpg', 'rb') as images_file:
        result = visual_recognition.detect_faces(images_file).get_result()
        # select the first (and hopefully only) face
        face = result['images'][0]['faces'][0]
        # average the age, pick 'M' or 'F' and extract the crop using face_crop()
        data = {'age': (face['age']['min'] + face['age']['max']) / 2,
                'sex': face['gender']['gender'][0],
                'photo': face_crop(face['face_location'])}
        return data

