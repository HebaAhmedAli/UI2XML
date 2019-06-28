import sys
sys.path.append('../')
import Constants
import os
def addIntentToJava(buttonsToActivities):
    
    return
    
def addIntentToMainifest(buttonsToActivities):
    if not os.path.exists('../'+Constants.DIRECTORY+'/res'):
            os.makedirs('../'+Constants.DIRECTORY+'/res') 
    fTo=open('../'+Constants.DIRECTORY+'/res/'+'AndroidManifest.xml', 'w+')
    newActivities = ""
    for i in range(len(buttonsToActivities)):
        newActivities += '\t'+'\t'+'<activity android:name=".'+buttonsToActivities[i][2][:-6].capitalize()+'Activity"'+ '>\n'+\
        '\t'+'\t'+'</activity>'+'\n'
    
    fTo.write('<?xml version="1.0" encoding="utf-8"?>'+'\n'+
              '<manifest xmlns:android="http://schemas.android.com/apk/res/android"'+'\n'
              +'\t'+'package="com.example.gp">'
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
    return

def switchActivities(buttonsToActivities):
    addIntentToJava(buttonsToActivities)
    addIntentToMainifest(buttonsToActivities)
    
imagesPath='data/ScreenShots/ourTest'
Constants.DIRECTORY = imagesPath+'/output/'+'main'
switchActivities([['Button_0_4_0','mainAD.jpg','switchAS.png'],['Button_0_5_0','mainAD.jpg','radio1AS.png']])