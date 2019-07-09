import sys
sys.path.append('../')
import Constants
import os

def addIntentToJava(buttonsToActivities):
    for buttonId,fromActivity,toActivity in buttonsToActivities:
        if "Image" in buttonId:
            buttonId = buttonId[12:]
        else:
            buttonId = buttonId[7:]
        fromActivity = fromActivity[:-6]
        fromActivityFile = Constants.DIRECTORY+'/java/com/example/'+Constants.PROJECT_NAME+"/"+fromActivity.capitalize()+"Activity.java"
        toActivity = toActivity[:-6]
        intent = "\n\t\tIntent intent = new Intent("+fromActivity.capitalize()+"Activity.this, "+toActivity.capitalize()+"Activity.class);\n"+"\t\tstartActivity(intent);\n\t\t"
        with open(fromActivityFile, 'r') as file:
            filedata = file.read()
        file.close()
        filedata = filedata.replace("\n\t// onClick logic_"+buttonId+"\n\t\t", intent)
        with open(fromActivityFile, 'w') as file:
            file.write(filedata)

def addIntentToMainifest(buttonsToActivities):
    if not os.path.exists(Constants.DIRECTORY):
            os.makedirs(Constants.DIRECTORY) 
    fTo=open(Constants.DIRECTORY+'/'+'AndroidManifest.xml', 'w+')
    newActivities = ""
    for i in range(len(buttonsToActivities)):
        if buttonsToActivities[i][2][:-6].capitalize()!= "Main":
            newActivities += '\t'+'\t'+'<activity android:name=".'+buttonsToActivities[i][2][:-6].capitalize()+'Activity"'+ '>\n'+\
            '\t'+'\t'+'</activity>'+'\n'
    
    fTo.write('<?xml version="1.0" encoding="utf-8"?>'+'\n'+
              '<manifest xmlns:android="http://schemas.android.com/apk/res/android"'+'\n'
              +'\t'+'package="com.example.'+Constants.PROJECT_NAME.lower()+'">\n'
              +'\t'+'<application'+'\n'
              +'\t'+'\t'+'android:allowBackup="true"'+'\n'
              +'\t'+'\t'+'android:icon="@mipmap/ic_launcher"'+'\n'
              +'\t'+'\t'+'android:label="@string/app_name"'+'\n'
              +'\t'+'\t'+'android:roundIcon="@mipmap/ic_launcher_round"'+'\n'
              +'\t'+'\t'+'android:supportsRtl="true"'+'\n'
              +'\t'+'\t'+'android:theme="@style/AppTheme">'+'\n'
              +'\t'+'\t'+'<activity android:name=".MainActivity">'+'\n'
              +'\t'+'\t'+'\t'+'<intent-filter>'+'\n'
              +'\t'+'\t'+'\t'+'\t'+'<action android:name="android.intent.action.MAIN"/>'+'\n'
              +'\t'+'\t'+'\t'+'\t'+'<category android:name="android.intent.category.LAUNCHER"/>'+'\n'
              +'\t'+'\t'+'\t'+'</intent-filter>'+'\n'
              +'\t'+'\t'+'</activity>'+'\n'
              +newActivities
              +'\t'+'</application>'+'\n'
              +'</manifest>')
    fTo.close()
    return

def switchActivities(buttonsToActivities):
    addIntentToJava(buttonsToActivities)
    addIntentToMainifest(buttonsToActivities)

'''
imagesPath='data/ScreenShots/ourTest'
Constants.DIRECTORY = imagesPath+'/'+'main'
switchActivities([['Button_0_4_0','mainAD.jpg','drAD.png'],['Button_0_5_0','mainAD.jpg','radio1AS.png'],['Button_0_6_0','mainAD.jpg','switchAS.png']])
'''
