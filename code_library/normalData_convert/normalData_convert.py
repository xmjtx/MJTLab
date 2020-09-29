import nuke

def normalData_convert() :
	errormsg = 'Please select a camera first.'
	try :
		n =nuke.selectedNode()
		morder =['0','1','2','4','5','6','8','9','10']
		if n.Class()[:6] == 'Camera' :
			connect = nuke.nodes.Dot()
			connect.setXYpos( int(n.xpos()+(nuke.toNode('preferences')['GridWidth'].getValue()*2)) , int(n.ypos()) )
			connect['label'].setValue('normal world input')
			cmatrix = nuke.nodes.ColorMatrix()
			for i in range(9) :
				cmatrix['matrix'].setExpression( '{0}.world_matrix.{1}'.format(n.name(),morder[i]), i )
			cmatrix['invert'].setValue(1)
			cmatrix.setInput(0, connect)
		else :
			nuke.message(errormsg)
	except :
		nuke.message(errormsg)