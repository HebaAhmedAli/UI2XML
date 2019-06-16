import sys
sys.path.append('../')
import os
import Constants


def printActionBar(appName):
    return "\t\tthis.getSupportActionBar().setDisplayOptions(ActionBar.DISPLAY_SHOW_CUSTOM);\n"+\
"\t\tgetSupportActionBar().setDisplayShowCustomEnabled(true);\n"+\
"\t\tgetSupportActionBar().setCustomView(R.layout.action_bar_"+appName+");\n"+\
"\t\tView view = getSupportActionBar().getCustomView();\n"

def findListView(rootNode,listViewIds):
    if len(rootNode.childNodes) == 0:
        if rootNode.nodeType == 'android.widget.ListView':
           listViewIds.append(rootNode)
        return
    for childNode in rootNode.childNodes:
        findButtons(childNode,listViewIds)

def printArrayList(noOfListViews):
    arrayList = ""
    for i in range(noOfListViews):
        arrayList += "\tListView lv;\n"+\
        "\tListViewBaseAdapter adapter;\n"+\
        "\tArrayList<ListViewBean> arr_bean;\n"
    return arrayList
    
def printAddingItems(listView):
    items = ""
    
    return items
    
def printListViewBean(listView):
    listViewBean = ""
    
    return listViewBean
    
    
def printListViewBaseAdapter(listView):
    listViewBean = ""
    
    return listViewBean
       
  
def findButtons(rootNode,buttonsIds):
    if len(rootNode.childNodes) == 0:
        if(rootNode.nodeType == 'android.widget.ImageButton' or rootNode.nodeType == 'android.widget.Button'):
           buttonsIds.append(rootNode.id)
        return
    for childNode in rootNode.childNodes:
        findButtons(childNode,buttonsIds)
            
def printButtons(buttonsId):
    onClick = ""
    for buttonId in  buttonsId:
        onClick += "\tpublic void clickMe"+str(buttonId)+"(View view){\n\n\t}\n"
    return onClick
    
def generateJava(rootNode,appName,actionBarOp):
    if not os.path.exists(Constants.DIRECTORY+'/java'):
            os.makedirs(Constants.DIRECTORY+'/java') 
    fTo=open(Constants.DIRECTORY+'/java/'+appName.capitalize()+"Activity"+'.java', 'w+')
    
    package = "com.example."+Constants.PACKAGE+"."+appName
    imports = "import android.os.Bundle;\n"+\
    "import android.support.v7.app.AppCompatActivity;\n"+\
    "import android.view.View;\n"
    
    classBody =""
    
    listViews = []    
    findListView(rootNode,listViews)
    #classBody+= printArrayList(len(listViews))
    #for listView in listViews:
     #   listItems = printAddingItems(listView)
      #  printListViewBean(listView)
       # printListViewBaseAdapter(listView)
        
        
    classBody += "\npublic class "+appName.capitalize()+"Activity"+" extends AppCompatActivity {\n\n"+\
    "\t@Override\n"+\
    "\tprotected void onCreate(Bundle savedInstanceState) {\n"
    
    onCreateBody ="\t\tsuper.onCreate(savedInstanceState);\n"+\
    "\t\tsetContentView(R.layout.activity_"+appName+");\n"
    
    if(actionBarOp == 'A'):
        imports+= "import android.support.v7.app.ActionBar;\n"
        onCreateBody+= printActionBar(appName)
    
    
    
    onCreateClose="\t}\n"
        
    buttonsId = []
    findButtons(rootNode,buttonsId) 
    onClickFunctions= printButtons(buttonsId)
    
    
    classClose= "}"
        
        
    fTo.write(package+imports+classBody+onCreateBody+onCreateClose+onClickFunctions+classClose)    
    
    