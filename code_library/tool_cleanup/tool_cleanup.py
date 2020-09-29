import os
import nuke

def tool_cleanup() :
	p = nuke.Panel('select types :')
	p.addEnumerationPulldown('cleanup type :', 'copy&paste file ')

	if p.show() :
		if p.value('cleanup type :') == 'file' :
			subp = nuke.Panel('select file :')
			subp.addFilenameSearch('file :', '')
			subp.setWidth( 500 )
			
			if subp.show() :
				workfile = subp.value('file :')
				
				if len( workfile ) > 0 :
					file = open( workfile , 'r' )
					context = file.readlines()
					file.close()
					
					if workfile.split('.')[-1:][0].lower() == 'nk' or workfile.split('.')[-1:][0].lower() == 'gizmo' :

						###
						linenotes = []
						scanrange = 0
						rootscan = 0

						for key,value in enumerate(context) :
							if value[0:3] == '#! ' or value[0:8] == 'version ' or scanrange != 0 :
								linenotes.append( key )
						
							if value[0:24] == 'define_window_layout_xml' or value[0:17] == ' colorManagement ' :
								linenotes.append( key )
								scanrange = 1

							if value[0:6] == 'Root {' :
								rootscan = 1

							if rootscan == 1 and value[0:6] == ' name ' :
								linenotes.append( key )

							if value[0:10] == ' floatLut ' :
								scanrange = 0
								rootscan = 0

							if value[0:1] == '}' :
								scanrange = 0
						
						linenotes.sort()
						linenotes.reverse()

						for i in linenotes :
							context.pop(i)

						newfile = workfile.split( os.sep )[-1:][0].split('.')[0] + '_clean.' + workfile.split( os.sep )[-1:][0].split('.')[1]
						filepath = workfile.split( os.sep )[:-1]
						filepath.append(newfile)

						file = open( os.sep.join( filepath ) , 'w' )
						file.write( ''.join( context ) )
						file.close()

						nuke.message('clean file saved here : <br>' + os.sep.join( filepath ) )
						###
						
					else :
						nuke.message('Only support <font color=orange>*.nk</font> & <font color=orange>*.gizmo</font> .<br><br>Process denied.')
				else :
					nuke.message('file path is empty.<br><br>Process denied.')
		else :
			subp = nuke.Panel('paste code :')
			subp.addFilenameSearch('save file :', '')
			subp.addBooleanCheckBox('also save as gizmo', True)
			subp.addMultilineTextInput('paste code here :', '')
			subp.setWidth( 500 )
			
			if subp.show() :
				newfile = subp.value('save file :')
				pastecode = subp.value('paste code here :').split('\n')

				if len( newfile ) == 0 :
					nuke.message('file path is empty.<br><br>Process denied.')
				elif len(pastecode) <= 1 :
					nuke.message('No code pasted.<br><br>Process denied.')
				else :
					if newfile.split('.')[-1:][0].lower() != 'nk' :
						newfile = newfile + '.nk'
					###
					newcontext = []
					
					for i in pastecode :
						if i[:19] == 'set cut_paste_input' or i[:8] == 'version ' or i[:21] == 'push $cut_paste_input' or i[:10] == ' selected ' or i[:6] == ' xpos ' or i[:6] == ' ypos ' :
							pass
						else :
							newcontext.append(i)
					
					file = open( newfile , 'w' )
					file.write( '\n'.join(newcontext) )
					file.close()

					if subp.value('also save as gizmo') :
						if newcontext[0] == 'Group {' :
							newcontext[0] = 'Gizmo {'

						newGizmo = newfile.split('.')[:-1][0] + '.gizmo'

						file = open( newGizmo , 'w' )
						file.write( '\n'.join(newcontext) )
						file.close()

						nuke.message('New nk file save here : <br>nk : {0}<br>gizmo : {1}'.format( newfile, newGizmo ) )
					else :
						nuke.message('New nk file save here : <br>nk : {0}'.format( newfile ) )