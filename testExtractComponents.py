import ComponentsExtraction.ComponentsExtraction as ComponentsExtraction


imagesPath='data/ScreenShots'


def processSave(imageDir, subdir, i):
    img=cv2.imread(imageDir)
    imageDir = imageDir.replace('.jpeg','')
    imageDir = imageDir.replace('.png','')
    # TODO: Loop on the wanted images and call this function on.
    # Take the loop that loops on the folders.
    image=[] # TODO: Contains the image.
    ComponentsExtraction.extractComponents(image, imageDir)
    cv2.imwrite(subdir+"/output"+str(i)+".jpg",img)





for subdir, dirs, files in os.walk(imagesPath):
    i=0
    for file in files:
        imgPath = os.path.join(subdir, file)
        #print string
        if ".png" in imgPath or ".jpeg" in imgPath:
            processSave(imgPath, subdir, i)
            i=i+1