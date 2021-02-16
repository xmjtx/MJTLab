============================================
Easy installation :
============================================
http://www.nukepedia.com/gizmos/other/menupy
https://github.com/xmjtx/MJTLab/tree/main/gizmo_library/Misc/MenuPy_v26

#Drag'n Drop this "MenuPy" gizmo into Nuke for easy installation.


============================================
Advanced installation (gizmo user) :
============================================

### Gizmo User - Add this to your menu.py ###
import nuke
### MJTLab - Deep2VP v4.0 ###
DVPFam = {"general" : ["Deep2VP","DVPToImage","DVPortal","DVPColorCorrect"] , 
		"matte" : ["DVPmatte","DVPattern","DVProjection"] , 
		"lighting" : ["DVPsetLight","DVPscene","DVPrelight","DVPrelightPT","DVPfresnel"] , 
		"shader" : ["DVP_Shader","DVP_ToonShader"]
		}
### hard code. Don't change it ###
toolbar = nuke.toolbar("Nodes")
DVP = toolbar.addMenu("Deep2VP", icon="Deep2VP.png")
for key,value in DVPFam.items() :
	for item in value :
		if key == "general" :
			DVP.addCommand( "{0}".format(item), "nuke.createNode(\"{0}\")".format(item), icon="{0}.png".format(item) )
		else :
			DVP.addCommand( "{0}/{1}".format(key,item), "nuke.createNode(\"{0}\")".format(item), icon="{0}.png".format(item) )
### end here ###


============================================
Advanced installation (.nk group user) :
============================================

### .nk group User - Add this to your menu.py ###
import nuke
### edit folder path here ###
DVPath = "C:/MenuPy/Deep2VP/"

### MJTLab - Deep2VP v4.0 ###
DVPFam = {"general" : ["Deep2VP","DVPToImage","DVPortal","DVPColorCorrect"] , 
		"matte" : ["DVPmatte","DVPattern","DVProjection"] , 
		"lighting" : ["DVPsetLight","DVPscene","DVPrelight","DVPrelightPT","DVPfresnel"] , 
		"shader" : ["DVP_Shader","DVP_ToonShader"]
		}
### hard code. Don't change it ###
toolbar = nuke.toolbar("Nodes")
DVP = toolbar.addMenu("Deep2VP", icon="Deep2VP.png")
for key,value in DVPFam.items() :
	for item in value :
		if key == "general" :
			DVP.addCommand( "{0}".format(item), "nuke.nodePaste(\"{0}{1}.nk\")".format(DVPath,item), icon="{0}.png".format(item) )
		else :
			DVP.addCommand( "{0}/{1}".format(key,item), "nuke.nodePaste(\"{0}{1}/{2}.nk\")".format(DVPath,key,item), icon="{0}.png".format(item) )
### end here ###