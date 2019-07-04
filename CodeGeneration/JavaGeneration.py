import sys
sys.path.append('../')
import os
import Constants


def printActionBar(appName):
    return "\t\tthis.getSupportActionBar().setDisplayOptions(ActionBar.DISPLAY_SHOW_CUSTOM);\n"+\
"\t\tgetSupportActionBar().setDisplayShowCustomEnabled(true);\n"+\
"\t\tLayoutInflater inflator=   (LayoutInflater)this.getSystemService(Context.LAYOUT_INFLATER_SERVICE);\n"+\
"\t\tView v=inflator.inflate(R.layout.action_bar_"+appName+", null);\n"+\
"\t\tActionBar.LayoutParams layoutParams = new ActionBar.LayoutParams(ActionBar.LayoutParams.MATCH_PARENT,ActionBar.LayoutParams.MATCH_PARENT);\n"+\
"\t\tgetSupportActionBar().setCustomView(v, layoutParams);\n"+\
"\t\tToolbar parent = (Toolbar) v.getParent();\n"+\
"\t\tparent.setContentInsetsAbsolute(0, 0);\n"



def findListViewAndRadioGroup(rootNode,listViews,radioGroups):
    if rootNode.nodeType == 'android.widget.ListView':
        listViews.append(rootNode)
        return
    if rootNode.nodeType == 'android.widget.RadioGroup':
        radioGroups.append(rootNode)
        return 
    for childNode in rootNode.childNodes:
        findListViewAndRadioGroup(childNode,listViews,radioGroups)

def printArrayList(noOfListViews,appName):
    arrayList = ""
    for i in range(noOfListViews):
        arrayList += "\tListView lv"+str(i)+";\n"+\
        "\t"+appName.capitalize()+"ListViewBaseAdapter"+str(i)+" adapter"+str(i)+";\n"+\
        "\tArrayList<"+appName.capitalize()+"ListViewBean"+str(i)+"> arr_bean"+str(i)+";\n"
    return arrayList


def getItemsfromLeafNodes(listIdx,layoutIdx,node,leafIdx,varType,varName,selectedNames,selectedTypes,selectedIds):
    leaves = ""
    if len(node.childNodes) == 0:
        if node.nodeType in varType:
            if layoutIdx == 0:
                selectedNames.append(varName[node.nodeType])
                selectedTypes.append(node.nodeType)
                selectedIds.append(node.id)
            if node.nodeType == 'android.widget.TextView' or node.nodeType == 'android.widget.Button':
                leaves += '"' + node.text + '"'
            if node.nodeType == 'android.widget.ImageView' or node.nodeType == 'android.widget.ImageButton':
                leaves += "R.drawable." + node.imagePath
            leaves += ", "
            leafIdx+=1
        return leaves
    for child in node.childNodes:
         leaves += getItemsfromLeafNodes(listIdx,layoutIdx,child,leafIdx,varType,varName,selectedNames,selectedTypes,selectedIds)
    return leaves


def printAddingItems(listView,idx,appName):
    varType = {'android.widget.ImageButton': 'int', 'android.widget.ImageView': 'int', \
               'android.widget.TextView': 'String', 'android.widget.Button': 'String','android.widget.CheckedTextView': 'String'}
    varName = {'android.widget.ImageButton': 'icons', 'android.widget.ImageView': 'images', \
               'android.widget.TextView': 'texts', 'android.widget.Button': 'buttonTexts','android.widget.CheckedTextView': 'checkedTexts'}
    selectedNames = []
    selectedTypes = []
    selectedIds = []
    leafIdx = 0
    items = ""
    items+= "\t\tlv"+str(idx)+" = (ListView) findViewById(R.id.ListView"+str(listView.id)+");\n"\
    "\t\tarr_bean"+str(idx)+"=new ArrayList<>();\n"

    for i in range(len(listView.childNodes)):
        items += "\t\tarr_bean"+str(idx)+".add(new "+appName.capitalize()+"ListViewBean"+str(idx)+"("
        items += getItemsfromLeafNodes(idx,i, listView.childNodes[i],leafIdx, varType, varName, selectedNames, selectedTypes,selectedIds)
        items = items[:-2]
        items += "));\n"
    items+="\t\tadapter"+str(idx)+"=new "+appName.capitalize()+"ListViewBaseAdapter"+str(idx)+"(arr_bean"+str(idx)+",this);\n"+\
    "\t\tlv"+str(idx)+".setAdapter(adapter"+str(idx)+");\n"
    
    return items,selectedTypes,selectedIds,selectedNames
    
def printListViewBean(leavesType,idx,appName,package):
    listViewBean = ""
    if Constants.PACKAGE != '':
        fTo=open(Constants.DIRECTORY+'/java/com/example/'+Constants.PACKAGE+"/"+Constants.PROJECT_NAME+"/"+appName.capitalize()+"ListViewBean"+str(idx)+'.java', 'w+')
    else:
        fTo=open(Constants.DIRECTORY+'/java/com/example/'+Constants.PROJECT_NAME+"/"+appName.capitalize()+"ListViewBean"+str(idx)+'.java', 'w+')

    varType = {'android.widget.ImageButton': 'int' ,'android.widget.ImageView': 'int',\
              'android.widget.TextView': 'String', 'android.widget.Button': 'String','android.widget.CheckedTextView': 'String'}
    varName = {'android.widget.ImageButton': 'icon' ,'android.widget.ImageView': 'image',\
              'android.widget.TextView': 'text', 'android.widget.Button': 'buttonText','android.widget.CheckedTextView': 'checkedTexts'}
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
        
    fTo.write("package "+package+";\n"+listViewBean)    
    
    return
    
    
def printListViewBaseAdapter(listView,leavesType,selectedIds,idx,appName,package):
    listViewBean = ""
    if Constants.PACKAGE != '':
        fTo=open(Constants.DIRECTORY+'/java/com/example/'+Constants.PACKAGE+"/"+Constants.PROJECT_NAME+"/"+appName.capitalize()+"ListViewBaseAdapter"+str(idx)+'.java', 'w+')
    else:
        fTo=open(Constants.DIRECTORY+'/java/com/example/'+Constants.PROJECT_NAME+"/"+appName.capitalize()+"ListViewBaseAdapter"+str(idx)+'.java', 'w+')

    imports = "import android.content.Context;\nimport android.view.LayoutInflater;\nimport android.view.View;\n"+\
    "import android.view.ViewGroup;\nimport android.widget.BaseAdapter;\nimport java.util.ArrayList;\nimport java.util.List;\n"
    
    listViewBean += "public class "+appName.capitalize()+"ListViewBaseAdapter"+str(idx)+" extends BaseAdapter {\n"+\
    "\tpublic ArrayList<"+appName.capitalize()+"ListViewBean"+str(idx)+"> arrayListListener;\n"+\
    "\tprivate List<"+appName.capitalize()+"ListViewBean"+str(idx)+"> mListenerList;\n\tContext mContext;\n"+\
    "\tpublic "+appName.capitalize()+"ListViewBaseAdapter"+str(idx)+"(List<"+appName.capitalize()+"ListViewBean"+str(idx)+"> mListenerList, Context context) {\n"+\
    "\t\tmContext = context;\n\t\tthis.mListenerList = mListenerList;\n\t\tthis.arrayListListener = new ArrayList<"+appName.capitalize()+"ListViewBean"+str(idx)+">();\n"+\
    "\t\tthis.arrayListListener.addAll(mListenerList);\n\t}\n\tpublic class ViewHolder {\n"

    varName = {'android.widget.ImageButton': 'iconView' ,'android.widget.ImageView': 'imageView',\
              'android.widget.TextView': 'textView', 'android.widget.Button': 'buttonView','android.widget.CheckedTextView':'checkedTextView'}
    viewType = {'android.widget.ImageButton': 'ImageButton' ,'android.widget.ImageView': 'ImageView',\
              'android.widget.TextView': 'TextView', 'android.widget.Button': 'Button','android.widget.CheckedTextView':'CheckedTextView'}
    setter = {'android.widget.ImageButton': 'setImageResource' ,'android.widget.ImageView': 'setImageResource',\
              'android.widget.TextView': 'setText', 'android.widget.Button': 'setText','android.widget.CheckedTextView':'CheckedTextView'}
    getter = {'android.widget.ImageButton': 'getIcon' ,'android.widget.ImageView': 'getImage',\
              'android.widget.TextView': 'getText', 'android.widget.Button': 'getButtonText','android.widget.CheckedTextView':'getCheckedText'}
    
    holderItems=""
    setHolderItems=""
    for i in range(len(leavesType)):
        imports+= "import "+leavesType[i]+";\n"
        listViewBean += "\t\t"+viewType[leavesType[i]]+" "+ varName[leavesType[i]]+str(i)+";\n"
        holderItems+= "\t\t\tholder."+varName[leavesType[i]]+str(i)+" = ("+viewType[leavesType[i]]+") view.findViewById(R.id."+viewType[leavesType[i]]+'_'+str(selectedIds[i])+");\n"
        setHolderItems += "\t\t\tholder."+varName[leavesType[i]]+str(i)+"."+setter[leavesType[i]]+"(mListenerList.get(position)."+getter[leavesType[i]]+str(i)+"());\n"
        #if leavesType[i] == 'android.widget.ImageButton' or leavesType[i] == 'android.widget.Button':
        #    setHolderItems += "\t\t\tholder."+varName[leavesType[i]]+str(i)+".setOnClickListener(new View.OnClickListener() {\n"+\
        #   "\t\t\t\t@Override\n\t\t\t\tpublic void onClick(View v) {\n\t\t\t\t\t// onClick logic \t\t\t\t}\n\t\t\t});\n"
    
    listViewBean+= "\t}\n\t@Override\n\tpublic int getCount() {\n\t\treturn mListenerList.size();\n\t}\n"+\
        "\t@Override\n\tpublic Object getItem(int position) {\n\t\treturn mListenerList.get(position);\n\t}\n"+\
        "\t@Override\n\tpublic long getItemId(int position) {\n\t\treturn position;\n\t}\n\t@Override\n"+\
        "\tpublic View getView(final int position, View view, ViewGroup parent) {\n\t\tfinal ViewHolder holder;\n"+\
        "\t\tif (view == null) {\n"+\
        "\t\t\tview = LayoutInflater.from(mContext).inflate(R.layout.list_view"+str(listView.id)+", null);\n"+\
        "\t\t\tholder = new ViewHolder();\n"+holderItems+"\t\t\tview.setTag(holder);\n\t\t}\n"+\
        "\t\telse {\n\t\t\tholder = (ViewHolder) view.getTag();\n\t\t}\n\t\ttry {\n"+\
        setHolderItems+"\t\t} catch (Exception ex){\n\t\t}\n\t\treturn view;\n\t}\n}"
    
    fTo.write("package "+package+";\n"+imports+listViewBean)
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
        onClick += "\tpublic void clickMe"+str(buttonId)+"(View view){\n\t// onClick logic_"+buttonId+"\n"+\
        "\t\tToast.makeText(getApplicationContext(),"+'"'+"Clicked on Button"+'"'+",Toast.LENGTH_SHORT).show();\n"+\
        "\t}\n"
    return onClick

def setCheckedHorizontal(radioGroup,radioGroupIdx,radioIdx):
    checkedString = "\t\t\t\tradioButton"+str(radioGroupIdx)+str(radioIdx)+".setChecked(true);\n"
    radioCount = 0
    for i in range(len(radioGroup.childNodes)):
        if radioGroup.childNodes[i].nodeType == 'android.widget.RadioButton':
            if radioCount != radioIdx:
                checkedString+=  "\t\t\t\tradioButton"+str(radioGroupIdx)+str(radioCount)+".setChecked(false);\n"
            radioCount+=1
    return checkedString


def setCheckedVertical(radioGroup,radioGroupIdx,radioIdx):
    checkedString = "\t\t\t\tradioButton" + str(radioGroupIdx) + str(radioIdx) + ".setChecked(true);\n"
    for i in range(len(radioGroup.childNodes)):
        if i != radioIdx:
            checkedString += "\t\t\t\tradioButton" + str(radioGroupIdx) + str(i) + ".setChecked(false);\n"
    return checkedString

def printRadiosAndOnClicks(radioGroup,radioGroupIdx):
    radioButtons = "\tRadioButton "
    findViews = ""
    onClicks = ""
    radioId = ""
    if len(radioGroup.childNodes) > 1 : # VerticalRadioGroup
        for i in range(len(radioGroup.childNodes)):
            for child in radioGroup.childNodes[i].childNodes: 
                if child.nodeType == "android.widget.RadioButton":
                    radioId = child.id
                    break
            radioButtons+= "radioButton"+str(radioGroupIdx)+str(i)
            if i < len(radioGroup.childNodes)-1 :
                radioButtons+= ", "
            findViews += "\t\tradioButton"+str(radioGroupIdx)+str(i)+" = "+"(RadioButton)findViewById(R.id.RadioButton_"+radioId+");\n"
            onClicks+= "\t\tradioButton"+str(radioGroupIdx)+str(i)+".setOnClickListener(new View.OnClickListener() {\n"+\
            "\t\t\tpublic void onClick(View v) {\n"
            onClicks+= setCheckedVertical(radioGroup,radioGroupIdx,i)
            onClicks+="\t\t\t}\n\t\t});"
        radioButtons+= ";\n"
        
    else: # HorizontalRadioGroup containing only one horizontal Linearlayout
       radioButtonCount = 0
       for i in range(len(radioGroup.childNodes[0].childNodes)):
           if radioGroup.childNodes[0].childNodes[i].nodeType == "android.widget.RadioButton":
                radioId = radioGroup.childNodes[0].childNodes[i].id
                radioButtons+= "radioButton"+str(radioGroupIdx)+str(radioButtonCount)+", "
                findViews += "\t\tradioButton"+str(radioGroupIdx)+str(radioButtonCount)+" = "+"(RadioButton)findViewById(R.id.RadioButton_"+radioId+");\n"
                onClicks+= "\t\tradioButton"+str(radioGroupIdx)+str(radioButtonCount)+".setOnClickListener(new View.OnClickListener() {\n"+\
                "\t\t\tpublic void onClick(View v) {\n"
                onClicks+= setCheckedHorizontal(radioGroup.childNodes[0],radioGroupIdx,radioButtonCount)
                onClicks+="\t\t\t}\n\t\t});\n"
                radioButtonCount += 1
       radioButtons = radioButtons[:-2]         
       radioButtons+= ";\n"
       
    return radioButtons, findViews+onClicks

def generateJava(rootNode,appName,actionBarOp):
    if Constants.PACKAGE != '':
        if not os.path.exists(Constants.DIRECTORY+'/java/com/example/'+Constants.PACKAGE+"/"+Constants.PROJECT_NAME+"/"):
                os.makedirs(Constants.DIRECTORY+'/java/com/example/'+Constants.PACKAGE+"/"+Constants.PROJECT_NAME+"/") 
        fTo=open(Constants.DIRECTORY+'/java/com/example/'+Constants.PACKAGE+"/"+Constants.PROJECT_NAME+"/"+appName.capitalize()+"Activity"+'.java', 'w+')
    else:
        if not os.path.exists(Constants.DIRECTORY+'/java/com/example/'+Constants.PROJECT_NAME+"/"):
                os.makedirs(Constants.DIRECTORY+'/java/com/example/'+Constants.PROJECT_NAME+"/") 
        fTo=open(Constants.DIRECTORY+'/java/com/example/'+Constants.PROJECT_NAME+"/"+appName.capitalize()+"Activity"+'.java', 'w+')
   
    package = "com.example."+Constants.PACKAGE+"."+Constants.PROJECT_NAME
    if Constants.PACKAGE == '':
        package = "com.example."+Constants.PROJECT_NAME
    imports = "import android.os.Bundle;\n"+\
    "import android.view.View;\n"+\
    "import android.widget.Toast;\n" +\
    "import android.content.Intent;\n" +\
    "import android.content.Context;\n" 

    if Constants.PACKAGE == '':
        imports+= "import androidx.appcompat.app.AppCompatActivity;\n"
    else:
        imports+="import android.support.v7.app.AppCompatActivity;\n"
    
    classBody =""
    classBody += "\npublic class "+appName.capitalize()+"Activity"+" extends AppCompatActivity {\n\n"
    listViews = []  
    radioGroups = []
    findListViewAndRadioGroup(rootNode,listViews,radioGroups)
    if len(listViews) >0:
        imports+= "import android.widget.ListView;\nimport java.util.ArrayList;\n"
    classBody+= printArrayList(len(listViews),appName)
    addedListItems = ""
    allListItems = ""

    for i in range(len(listViews)):
        #listItems,leavesType,selectedVarNames= printListItems(listViews[i],i)
        #classBody+=listItems
        addedListItems,leavesType,selectedIds,selectedVarNames = printAddingItems(listViews[i],i,appName)
        printListViewBean(leavesType,i,appName,package)
        printListViewBaseAdapter(listViews[i],leavesType,selectedIds,i,appName,package)
        allListItems+= addedListItems
    groupsRadiosDef = ""
    groupsRadiosOnClick = ""
    radiosDef = "" 
    radiosOnClick = ""
    if len(radioGroups)>0:
        imports += "import android.widget.RadioButton;\n"
    for i in range(len(radioGroups)):
        radiosDef,radiosOnClick = printRadiosAndOnClicks(radioGroups[i],i)
        groupsRadiosDef+=radiosDef
        groupsRadiosOnClick+=radiosOnClick
    
    classBody += groupsRadiosDef
    
    classBody+= "\t@Override\n"+\
    "\tprotected void onCreate(Bundle savedInstanceState) {\n"
    
    onCreateBody ="\t\tsuper.onCreate(savedInstanceState);\n"+\
    "\t\tsetContentView(R.layout.activity_"+appName+");\n"
    if(actionBarOp == 'A'):
        if Constants.PACKAGE == '':
            imports+= "import androidx.appcompat.app.ActionBar;\n"
            imports+= 'import android.view.LayoutInflater;\n'
            imports+= 'import androidx.appcompat.widget.Toolbar;\n'
        else:    
            imports+= "import android.support.v7.app.ActionBar;\n"
            imports+= 'import android.view.LayoutInflater;\n'
            imports+= 'import androidx.appcompat.widget.Toolbar;\n'
        onCreateBody+= printActionBar(appName)   
    
    onCreateBody+= allListItems
    onCreateBody+= groupsRadiosOnClick
    onCreateClose="\t}\n"
        
    buttonsId = []
    findButtons(rootNode,buttonsId) 
    onClickFunctions= printButtons(buttonsId)
    
    
    classClose= "}"

        
    fTo.write("package "+package+';\n'+imports+classBody+onCreateBody+onCreateClose+onClickFunctions+classClose)    
    
    