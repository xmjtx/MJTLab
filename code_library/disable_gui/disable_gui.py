import nuke

def disable_gui() :
	for node in nuke.selectedNodes() :
		try :
			if node['disable'].getValue() :
				node['disable'].clearAnimated()
				node['disable'].setValue(0)
				node['label'].fromScript( '\n'.join( [i for i in node['label'].toScript().split('\n') if i != 'Disabled by GUI'] ) )
			else :
				node['disable'].setExpression('$gui')
				node['label'].fromScript( '\n'.join( [node['label'].toScript() , 'Disabled by GUI'] ) )
		except :
			pass