import screenshotProcessing.ComponentsExtraction as ComponentsExtraction


imagesPath='data/ScreenShots'


def processSave(imageDir, subdir, i):
    img=cv2.imread(imageDir)
    imageDir = imageDir.replace('.jpeg','')
    imageDir = imageDir.replace('.png','')
    # TODO: Loop on the wanted images and call this function on.
    # Take the loop that loops on the folders.
    image=[] # TODO: Contains the image.
    boxes, texts = ComponentsExtraction.extractComponents(image)
    margin = 5
    if not os.path.exists(imageDir):
        os.makedirs(imageDir)
    for x,y,w,h in boxes:
        # testing: print the cropped in folder
        crop_img = img[y - margin:y + h + margin, x - margin:x + w + margin]
        cv2.imwrite(imageDir + "/comp"+str(j) + ".jpg",crop_img)
    cv2.imwrite(subdir+"/output"+str(i)+".jpg",img)


for subdir, dirs, files in os.walk(imagesPath):
    i=0
    for file in files:
        imgPath = os.path.join(subdir, file)
        #print string
        if ".png" in imgPath or ".jpeg" in imgPath:
            processSave(imgPath, subdir, i)
            i=i+1