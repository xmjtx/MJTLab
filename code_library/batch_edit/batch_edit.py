import nuke

def batch_edit() :
	knob_error = 'Knob does not exist.'
	value_error = 'Sat value need to be a number.'

	p = nuke.Panel('select edit mode')
	p.addEnumerationPulldown('select edit mode', '"selected nodes" "node class"')
	if p.show() == 1 :
		editmode = p.value('select edit mode')

		if editmode == 'selected nodes' :
			snc = []
			for i in nuke.selectedNodes() :
				snc.append( i.name() )

			if len(snc) == 0 :
				nuke.message('No node selected.')
			else :
				subp = nuke.Panel('batch edit - selected nodes')
				subp.addSingleLineInput('selected nodes', ','.join(snc))
				subp.addSingleLineInput('edit knob', '')
				subp.addEnumerationPulldown('set value type', '"Number" "Text" "Expression"')
				subp.addSingleLineInput('value', '')

				if subp.show() == 1 :
					nc = subp.value('selected nodes').split(',')
					ek = subp.value('edit knob')
					vt = subp.value('set value type')
					sv = subp.value('value')

					try :
						for node in nc :
							if nuke.toNode(node)[ek].isAnimated() :
								nuke.toNode(node)[ek].clearAnimated()
							if vt == 'Number' :
								try :
									nuke.toNode(node)[ek].setValue( float(sv) )
								except TypeError :
									nuke.toNode(node)[ek].setValue( int(sv) )
							elif vt == 'Text' :
								nuke.toNode(node)[ek].setValue( str(sv) )
							elif vt == 'Expression' :
								nuke.toNode(node)[ek].setExpression( str(sv) )
						nuke.message('Edit succeed.')
					except NameError :
						nuke.message(knob_error)
					except ValueError :
						nuke.message(value_error)

		if editmode == 'node class' :
			try :
				snc = nuke.selectedNode().Class()
			except :
				snc = ''

			subp = nuke.Panel('batch edit - node class')
			subp.addSingleLineInput('node class', snc)
			subp.addSingleLineInput('edit knob', '')
			subp.addEnumerationPulldown('set value type', '"Number" "Text" "Expression"')
			subp.addSingleLineInput('value', '')

			if subp.show() == 1 :
				nc = subp.value('node class')
				ek = subp.value('edit knob')
				vt = subp.value('set value type')
				sv = subp.value('value')

				try :
					for node in nuke.allNodes() :
						if node.Class() == nc  :
							if nuke.toNode(node.name())[ek].isAnimated() :
								nuke.toNode(node.name())[ek].clearAnimated()
							if vt == 'Number' :
								try :
									nuke.toNode(node.name())[ek].setValue( float(sv) )
								except TypeError :
									nuke.toNode(node.name())[ek].setValue( int(sv) )
							elif vt == 'Text' :
								nuke.toNode(node.name())[ek].setValue( str(sv) )
							elif vt == 'Expression' :
								nuke.toNode(node.name())[ek].setExpression( str(sv) )
					nuke.message('Edit succeed.')
				except NameError :
					nuke.message(knob_error)
				except ValueError :
					nuke.message(value_error)