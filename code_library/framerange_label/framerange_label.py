import nuke

def framerange_label() :
	for node in nuke.allNodes() :
		if node.Class() == 'Read' :
			node['label'].setValue('[value first] - [value last]')