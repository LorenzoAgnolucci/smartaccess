from ibm_watson import VisualRecognitionV3
import PIL


visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='hgkvHWd0-DONvE2iStjGODSek8A9g9P7bdeQBkllA3GV')


def face_crop(id, face_location):
    # TODO implement with PILLOW
    #  the method should save a fixed dimension squared image in the dir /smartaccess/media/face_crops
    #  named <id>.jpg where id is the id log passed through get_photo_data()
    pass


def get_photo_data(id):
    # tmp.jpg is the last shot, it will be overwritten every successful access
    with open('smartaccess/media/tmp.jpg', 'rb') as images_file:
        result = visual_recognition.detect_faces(images_file).get_result()
        # select the first (and hopefully only) face
        face = result['images'][0]['faces'][0]
        # average the age, pick 'M' or 'F' and extract the crop using face_crop()
        data = {'age': (face['age']['min'] + face['age']['max']) / 2,
                'sex': face['gender']['gender'][0],
                'photo': face_crop(id, face['face_location'])}
        return data

