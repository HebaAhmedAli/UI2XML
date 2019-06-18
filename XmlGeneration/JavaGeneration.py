import sys
sys.path.append('../')
import os
import Constants


def printActionBar(appName):
    return "\t\tthis.getSupportActionBar().setDisplayOptions(ActionBar.DISPLAY_SHOW_CUSTOM);\n"+\
"\t\tgetSupportActionBar().setDisplayShowCustomEnabled(true);\n"+\
"\t\tgetSupportActionBar().setCustomView(R.layout.action_bar_"+appName+");\n"+\
"\t\tView view = getSupportActionBar().getCustomView();\n"

def findListView(rootNode,listViews):
    if rootNode.nodeType == 'android.widget.ListView':
        listViews.append(rootNode)
        return
    for childNode in rootNode.childNodes:
        findListView(childNode,listViews)

def printArrayList(noOfListViews,appName):
    arrayList = ""
    for i in range(noOfListViews):
        arrayList += "\tListView lv"+str(i)+";\n"+\
        "\t"+appName.capitalize()+"ListViewBaseAdapter"+str(i)+" adapter"+str(i)+";\n"+\
        "\tArrayList<"+appName.capitalize()+"ListViewBean"+str(i)+"> arr_bean"+str(i)+";\n"
    return arrayList

def  printListItems(listView,idx):
    varType = {'android.widget.ImageButton': 'int' ,'android.widget.ImageView': 'int',\
              'android.widget.TextView': 'String', 'android.widget.Button': 'String'}
    varName = {'android.widget.ImageButton': 'icons' ,'android.widget.ImageView': 'images',\
              'android.widget.TextView': 'texts', 'android.widget.Button': 'buttonTexts'}
    selectedNames = []
    selectedTypes = []
    items=""
    leafIdx = 0
    leafCount = 0
    while leafCount < len(listView.childNodes[0].childNodes):
        layoutIdx = 0
        if listView.childNodes[0].childNodes[leafCount].nodeType in varType:
            items+="\t"+varType[listView.childNodes[0].childNodes[leafCount].nodeType]+" "\
            +varName[listView.childNodes[0].childNodes[leafCount].nodeType]+str(idx)+str(leafIdx)+" [] = { "  
            selectedNames.append(varName[listView.childNodes[0].childNodes[leafCount].nodeType])
            selectedTypes.append(listView.childNodes[0].childNodes[leafCount].nodeType)
            while layoutIdx < len(listView.childNodes):
                if listView.childNodes[0].childNodes[leafCount].nodeType == 'android.widget.TextView' or \
                listView.childNodes[0].childNodes[leafCount].nodeType == 'android.widget.Button':
                    items+='"'+listView.childNodes[layoutIdx].childNodes[leafCount].text+'"'
                    
                if listView.childNodes[0].childNodes[leafCount].nodeType == 'android.widget.ImageView' or \
                listView.childNodes[0].childNodes[leafCount].nodeType == 'android.widget.ImageButton':
                    items+="R.drawable."+listView.childNodes[layoutIdx].childNodes[leafCount].imagePath 
                    
                if layoutIdx < len(listView.childNodes) -1:
                        items+=", "
                        
                layoutIdx+=1
            items+="};\n"
            leafIdx+=1
        leafCount+=1            
    return items,selectedTypes,selectedNames
def printAddingItems(listViewId,selectedVarNames,idx,appName):
    items = ""
    items+= "\t\tlv"+str(idx)+" = (ListView) findViewById(R.id.ListView"+str(listViewId)+");\n"\
    "\t\tarr_bean"+str(idx)+"=new ArrayList<>();\n"+\
    "\t\tfor(int i = 0; i<"+selectedVarNames[0]+str(idx)+"0.length;i++){\n"+\
    "\t\t\tarr_bean"+str(idx)+".add(new "+appName.capitalize()+"ListViewBean"+str(idx)+"("
    for i in range (len(selectedVarNames)):
        items+= selectedVarNames[i]+str(idx)+str(i)+"[i]"
        if i < len(selectedVarNames)-1 :
            items+=","        
    items+= "));\n"+\
    "\t\t}\n"+\
    "\t\tadapter"+str(idx)+"=new "+appName.capitalize()+"ListViewBaseAdapter"+str(idx)+"(arr_bean"+str(idx)+",this);\n"+\
    "\t\tlv"+str(idx)+".setAdapter(adapter"+str(idx)+");\n"
    
    return items
    
def printListViewBean(leavesType,idx,appName):
    listViewBean = ""
    fTo=open(Constants.DIRECTORY+'/java/'+appName.capitalize()+"ListViewBean"+str(idx)+'.java', 'w+')
    
    varType = {'android.widget.ImageButton': 'int' ,'android.widget.ImageView': 'int',\
              'android.widget.TextView': 'String', 'android.widget.Button': 'String'}
    varName = {'android.widget.ImageButton': 'icon' ,'android.widget.ImageView': 'image',\
              'android.widget.TextView': 'text', 'android.widget.Button': 'buttonText'}
    listViewBean+= "public class "+appName.capitalize()+"ListViewBean"+str(idx)+" {\n"
    constructor = ""
    getterAndSetter = ""
    params = ""
    for i in range (len(leavesType)):
        listViewBean+= "\t"+varType[leavesType[i]]+" "+varName[leavesType[i]]+str(i)+ ";\n"
        params +=varType[leavesType[i]]+" "+varName[leavesType[i]]+str(i)
        if i < len(leavesType)-1:
            params+=","
        constructor += "\t\tthis."+varName[leavesType[i]]+str(i)+" = "+varName[leavesType[i]]+str(i)+";\n"
        getterAndSetter += "\tpublic "+varType[leavesType[i]]+" get"+varName[leavesType[i]].capitalize()+str(i)+"() {\n"+\
        "\t\treturn "+varName[leavesType[i]]+str(i)+";\n\t}\n"+\
        "\tpublic void set"+varName[leavesType[i]].capitalize()+str(i)+"("+varType[leavesType[i]] +" "+varName[leavesType[i]]+str(i)+") {\n"+\
        "\t\tthis."+varName[leavesType[i]]+str(i)+" = "+varName[leavesType[i]]+str(i)+";\n\t}\n"
                
    listViewBean+= "\tpublic "+appName.capitalize()+"ListViewBean"+str(idx)+"() {\n\t}\n"+\
    "\tpublic "+appName.capitalize()+"ListViewBean"+str(idx)+"("+params+") {\n"+\
    "\t\tsuper();\n"+constructor + "\t}\n" +  getterAndSetter+"}\n"
        
    fTo.write("package com.example."+Constants.PACKAGE+"."+appName+";\n"+listViewBean)    
    
    return
    
    
def printListViewBaseAdapter(listView,leavesType,idx,appName):
    listViewBean = ""
    fTo=open(Constants.DIRECTORY+'/java/'+appName.capitalize()+"ListViewBaseAdapter"+str(idx)+'.java', 'w+')
    imports = "import android.content.Context;\nimport android.view.LayoutInflater;\nimport android.view.View;\n"+\
    "import android.view.ViewGroup;\nimport android.widget.BaseAdapter;\nimport java.util.ArrayList;\nimport java.util.List;\n"
    
    listViewBean += "public class "+appName.capitalize()+"ListViewBaseAdapter"+str(idx)+" extends BaseAdapter {\n"+\
    "\tpublic ArrayList<"+appName.capitalize()+"ListViewBean"+str(idx)+"> arrayListListener;\n"+\
    "\tprivate List<"+appName.capitalize()+"ListViewBean"+str(idx)+"> mListenerList;\n\tContext mContext;\n"+\
    "\tpublic "+appName.capitalize()+"ListViewBaseAdapter"+str(idx)+"(List<"+appName.capitalize()+"ListViewBean"+str(idx)+"> mListenerList, Context context) {\n"+\
    "\t\tmContext = context;\n\t\tthis.mListenerList = mListenerList;\n\t\tthis.arrayListListener = new ArrayList<"+appName.capitalize()+"ListViewBean"+str(idx)+">();\n"+\
    "\t\tthis.arrayListListener.addAll(mListenerList);\n\t}\n\tpublic class ViewHolder {\n"
    
    varName = {'android.widget.ImageButton': 'iconView' ,'android.widget.ImageView': 'imageView',\
              'android.widget.TextView': 'textView', 'android.widget.Button': 'buttonView'}
    viewType = {'android.widget.ImageButton': 'ImageButton' ,'android.widget.ImageView': 'ImageView',\
              'android.widget.TextView': 'TextView', 'android.widget.Button': 'Button'}
    setter = {'android.widget.ImageButton': 'setImageResource' ,'android.widget.ImageView': 'setImageResource',\
              'android.widget.TextView': 'setText', 'android.widget.Button': 'setText'}
    getter = {'android.widget.ImageButton': 'getIcon' ,'android.widget.ImageView': 'getImage',\
              'android.widget.TextView': 'getText', 'android.widget.Button': 'getButtonText'}
    
    holderItems=""
    setHolderItems=""
    for i in range(len(leavesType)):
        imports+= "import "+leavesType[i]+";\n"
        listViewBean += "\t\t"+viewType[leavesType[i]]+" "+ varName[leavesType[i]]+str(i)+";\n"
        holderItems+= "\t\t\tholder."+varName[leavesType[i]]+str(i)+" = ("+viewType[leavesType[i]]+") view.findViewById(R.id."+viewType[leavesType[i]]+str(listView.childNodes[0].childNodes[i].id)+");\n"
        setHolderItems += "\t\t\tholder."+varName[leavesType[i]]+str(i)+"."+setter[leavesType[i]]+"(mListenerList.get(position)."+getter[leavesType[i]]+str(i)+"());\n"
        #if leavesType[i] == 'android.widget.ImageButton' or leavesType[i] == 'android.widget.Button':
        #    setHolderItems += "\t\t\tholder."+varName[leavesType[i]]+str(i)+".setOnClickListener(new View.OnClickListener() {\n"+\
        #   "\t\t\t\t@Override\n\t\t\t\tpublic void onClick(View v) {\n\t\t\t\t\t// onClick logic \t\t\t\t}\n\t\t\t});\n"
    
    listViewBean+= "\t}\n\t@Override\n\tpublic int getCount() {\n\t\treturn mListenerList.size();\n\t}\n"+\
        "\t@Override\n\tpublic Object getItem(int position) {\n\t\treturn mListenerList.get(position);\n\t}\n"+\
        "\t@Override\n\tpublic long getItemId(int position) {\n\t\treturn position;\n\t}\n\t@Override\n"+\
        "\tpublic View getView(final int position, View view, ViewGroup parent) {\n\t\tfinal ViewHolder holder;\n"+\
        "\t\tif (view == null) {\n"+\
        "\t\t\tview = LayoutInflater.from(mContext).inflate(R.layout.list_view_"+str(listView.id)+", null);\n"+\
        "\t\t\tholder = new ViewHolder();\n"+holderItems+"\t\t\tview.setTag(holder);\n\t\t}\n"+\
        "\t\telse {\n\t\t\tholder = (ViewHolder) view.getTag();\n\t\t}\n\t\ttry {\n"+\
        setHolderItems+"\t\t} catch (Exception ex){\n\t\t}\n\t\treturn view;\n\t}\n}"
    
    fTo.write("package com.example."+Constants.PACKAGE+"."+appName+";\n"+imports+listViewBean)
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
        onClick += "\tpublic void clickMe"+str(buttonId)+"(View view){\n\t// onClick logic\n\t}\n"
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
    classBody += "\npublic class "+appName.capitalize()+"Activity"+" extends AppCompatActivity {\n\n"
    listViews = []    
    findListView(rootNode,listViews)
    if len(listViews) >0:
        imports+= "import android.widget.ListView;\nimport java.util.ArrayList;\n"
    classBody+= printArrayList(len(listViews),appName)
    addedListItems=""
    for i in range(len(listViews)):
        imports += "import "+package+"."+"ListViewBean"+str(i)+';\n'
        listItems,leavesType,selectedVarNames= printListItems(listViews[i],i)
        classBody+=listItems
        addedListItems = printAddingItems(listViews[i].id,selectedVarNames,i,appName)
        printListViewBean(leavesType,i,appName)
        printListViewBaseAdapter(listViews[i],leavesType,i,appName)        
        
    
    classBody+= "\t@Override\n"+\
    "\tprotected void onCreate(Bundle savedInstanceState) {\n"
    
    onCreateBody ="\t\tsuper.onCreate(savedInstanceState);\n"+\
    "\t\tsetContentView(R.layout.activity_"+appName+");\n"
    
    if(actionBarOp == 'A'):
        imports+= "import android.support.v7.app.ActionBar;\n"
        onCreateBody+= printActionBar(appName)   
    
    onCreateBody+= addedListItems
    onCreateClose="\t}\n"
        
    buttonsId = []
    findButtons(rootNode,buttonsId) 
    onClickFunctions= printButtons(buttonsId)
    
    
    classClose= "}"
        
        
    fTo.write("package "+package+';\n'+imports+classBody+onCreateBody+onCreateClose+onClickFunctions+classClose)    
    
    