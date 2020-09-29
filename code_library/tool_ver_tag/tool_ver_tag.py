import re, nuke


def tool_ver_tag() :
	toolNodes = []
	for node in nuke.selectedNodes() :
		toolNodes.append( node )

	k_dict = {}

	from datetime import date
	k_dict['l_DATE'] = date.today()

	try :
		k_dict['l_VERSION'] = toolNodes[0]['l_VERSION'].value()
		k_dict['btn_CHANGELOG'] = re.split('log = "|"' , toolNodes[0]['btn_CHANGELOG'].value() )[1].replace( '<br>' , '\n' ).replace( '&nbsp;' , ' ' )
		k_dict['l_DEV'] = toolNodes[0]['l_DEV'].value()
	except NameError :
		k_dict['l_VERSION'] = ''
		k_dict['btn_CHANGELOG'] = ''
		k_dict['l_DEV'] = ''

	p = nuke.Panel('Version Tag')
	p.addSingleLineInput('Version', k_dict['l_VERSION'])
	p.addSingleLineInput('Date Modified', k_dict['l_DATE'])
	p.addMultilineTextInput('Changelog', k_dict['btn_CHANGELOG'])
	p.addSingleLineInput('Developed by', k_dict['l_DEV'])
	p.setWidth( 700 )


	if p.show() == 1 :
		new_ver = p.value('Version')
		new_date = p.value('Date Modified')
		new_clog = p.value('Changelog')
		new_dev = p.value('Developed by')

		if new_clog.find('\n') > 0 :
			new_clog = new_clog.replace(' ' , '&nbsp;')
		new_clog = new_clog.replace('\n' , '<br>').replace('\"' , '\'')

		for toolNode in toolNodes :
			try :
				toolNode['l_VERSION'].setValue(new_ver)
				toolNode['l_DATE'].setValue(new_date)
				toolNode['btn_CHANGELOG'].setValue( 'log = "{0}"\nnuke.message( log )'.format( new_clog ) )
				toolNode['l_DEV'].setValue(new_dev)
			except NameError :
				make_tag = nuke.Tab_Knob('t_VERSION', 'Version')
				make_ver = nuke.Text_Knob('l_VERSION', 'Version', new_ver)
				make_date = nuke.Text_Knob('l_DATE', 'Date Modified', new_date)
				make_clog = nuke.PyScript_Knob('btn_CHANGELOG', 'Changelog', 'log = "{0}"\nnuke.message( log )'.format( new_clog ) )
				make_dev = nuke.Text_Knob('l_DEV', 'Developed by', new_dev)
				toolNode.addKnob(make_tag)
				toolNode.addKnob(make_ver)
				toolNode.addKnob(make_date)
				toolNode.addKnob(make_clog)
				toolNode.addKnob(make_dev)
				toolNode['btn_CHANGELOG'].setFlag( 0x0000000000001000 )