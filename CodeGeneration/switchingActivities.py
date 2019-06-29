import Constants
import fileinput
import sys
sys.path.append('../')


def addIntentToJava(buttonsToActivities):
    for buttonId,fromActivity,toActivity in buttonsToActivities:
        fromActivity = fromActivity[:-6]
        fromActivityFile = "../"+Constants.DIRECTORY+'/java/com/example/'+Constants.PROJECT_NAME+"/"+fromActivity.capitalize()+"Activity.java"
        toActivity = toActivity[:-6]
        intent = "Intent intent = new Intent("+fromActivity+"Activity.this, "+toActivity+"Activity.class)\n;"+"\tstartActivity(intent);"
        with open(fromActivityFile, 'r') as file:
            filedata = file.read()
        filedata = filedata.replace("// onClick logic"+buttonId, intent)
        print(filedata)
        with open(fromActivityFile, 'w') as file:
            file.write(filedata)
def addIntentToMainifest(buttonsToActivities):
    fTo=open(Constants.DIRECTORY+'/res/layout/'+'AndroidManifest.xml', 'w+')

    return

def switchActivities(buttonsToActivities):
    addIntentToJava(buttonsToActivities)
    #addIntentToMainifest(buttonsToActivities)

switchActivities([['0_5_0',"face1AD.jpg","face2AD.jpg"]])