from keras.preprocessing import image
import Constants


def preprocessing(imgPath):
        img = image.load_img(imgPath, target_size = (Constants.IMAGE_SIZE,Constants.IMAGE_SIZE))
        img = img.astype('float32')
        img /= 255
        return img