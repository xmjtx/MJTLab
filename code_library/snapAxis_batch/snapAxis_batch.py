import nuke
import nukescripts

def snapAxis_batch() :
	def vtxcheck() :
		vcount = 0
		for i in nukescripts.snap3d.selectedVertexInfos() :
			vcount += 1
		return vcount

	def generateAX(frameST, frameED, mode) :
		root = nuke.root()

		root.begin()

		bksel = []
		for node in nuke.allNodes() :
			if node['selected'].getValue(True) :
				bksel.append( node )
				node['selected'].setValue(False)

		ct_hack = nuke.nodes.CurveTool()
		vtx = {}
		axnode_ls = []

		progBar = nuke.ProgressTask('Sampling vertex')
		jobCount = 0
		jobTotal = frameED-frameST

		for ctime in xrange( frameST, frameED, 1 ) :

			nuke.execute(ct_hack, ctime, ctime)

			### progress bar
			jobCount += 1
			progShow = int(jobCount/jobTotal * 100)
			if progBar.isCancelled() :
				break;
			progBar.setProgress(progShow)
			#################

			for i in nukescripts.snap3d.selectedVertexInfos() :
				vtx[ str(i.objnum) + '_' + str(i.index) ] = i.position

			if ctime == frameST :
				for key,value in vtx.items() :
					ax = nuke.nodes.Axis()
					if mode == 1 :
						ax['translate'].setAnimated()
					for i in range(3) :
						ax['translate'].setValue( value[i], i)

					axid = nuke.Text_Knob('axid','axid',key)
					ax.addKnob(axid)

					axnode_ls.append( ax )
			else :
				for key,value in vtx.items() :
					for ax in axnode_ls :
						if ax['axid'].value() == key :
							for i in range(3) :
								ax['translate'].setValue( value[i], i)

		nuke.delete( ct_hack )
		del progBar
		del ctime

		for ctime in xrange ( frameST, frameED, 1) :
			for ax in axnode_ls :
				tr = ax['translate'].getValueAt(ctime)
				ax['translate'].setValueAt(tr[0], ctime, 0)
				ax['translate'].setValueAt(tr[1], ctime, 1)
				ax['translate'].setValueAt(tr[2], ctime, 2)
		
		scene = nuke.nodes.Scene()
		for i in range( len(axnode_ls) ) :
			axnode_ls[i]['selected'].setValue(True)
			scene.setInput(i, axnode_ls[i])
			if i == 0 :
				scene.setXYpos( int( axnode_ls[i].xpos() ), int( axnode_ls[i].ypos() + nuke.toNode('preferences')['GridWidth'].getValue() ) )

		nukescripts.autoBackdrop()

		for ax in axnode_ls :
			ax['selected'].setValue(False)

		for revertsel in bksel :
			revertsel['selected'].setValue(True)

		root.end()

	#######################################

	if vtxcheck() == 0 :
		nuke.message('Please select vertex first.')
	else :
		p = nuke.Panel('Snap vertex(s)')
		p.addEnumerationPulldown('select mode : ', '"non-animated" "animated"')

		if p.show() == 1 :
			if p.value('select mode : ') == 'animated' :
				projRange = str( int( nuke.root()['first_frame'].getValue() ) ) + '-' + str( int( nuke.root()['last_frame'].getValue() ) )

				subp = nuke.Panel('frame range')
				subp.addSingleLineInput('set frame range', projRange)

				if subp.show() == 1 :
					crange = subp.value('set frame range').replace(' ', '')


					if '-' in crange :
						frameST = int( crange.split('-')[0] )
						frameED = int( crange.split('-')[1] ) + 1
					else :
						frameST = int( crange )
						frameED = int( crange ) + 1

					generateAX(frameST, frameED, 1)

			if p.value('select mode : ') == 'non-animated' :
				frameST = int( nuke.frame() )
				frameED = int( nuke.frame() ) + 1

				generateAX(frameST, frameED, 0)