from House import House
#randint is inclusive,inclusive
from random import randint,random
import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from pylab import get_cmap
from datetime import datetime
import os


class Network:

	def __init__(self,N=10,N_types=2,threshold=0.5,empty_percent=.2):

		#self.grid = np.array([])
		self.grid = np.empty((N,N),dtype=House)
		self.N = N
		self.N_types = N_types

		self.threshold = threshold
		self.empty_proportion = empty_percent
		self.empty_set = set([])

		#So the types will start at 1. 0 will be reserved for an empty spot.
		for i in range(N):
			for j in range(N):
				self.grid[i,j] = House(randint(1,N_types),(i,j))

				if random()<self.empty_proportion:
					self.grid[i,j].type = 0
					self.empty_set.add((i,j))

		self.sim_avg = []
		self.movement = []
		#print(self.grid)

	def moveStep(self):

		sim_avg = []
		#If it's not above the threshold, so it wants to move, does it have to choose an empty spot that is above?
		moves = 0
		for (i,j), house in np.ndenumerate(self.grid):
			#print('i,j',i,j)
			if house.type!=0:

				sim = self.percentSimilar((i,j))
				sim_avg.append(sim)
				#print('house at {} is {} perc sim'.format((i,j),sim))

				if not self.aboveThresh(sim):
					empty = list(self.empty_set)[randint(0,len(self.empty_set)-1)]
					self.empty_set.remove(empty)
					temp = self.grid[empty]
					self.grid[empty] = self.grid[(i,j)]
					self.grid[(i,j)] = temp
					self.empty_set.add((i,j))

					moves += 1
					#print('moved from {} to {}'.format((i,j),empty))

		self.sim_avg.append(sum(sim_avg)/(self.N**2 - len(self.empty_set)))
		self.movement.append(moves)




	def aboveThresh(self,perc_sim):
		return(perc_sim>=self.threshold)

	def percentSimilar(self,loc):
		type = self.grid[tuple(loc)].type
		assert (type!=0), 'type is 0, dont pass it this'

		ns = self.getNeighborLocations(loc)

		typed_neighbors = sum([1.0 for n in ns if self.grid[n].type!=0])

		perc_sim = sum([1.0 for n in ns if self.grid[n].type==type])/max(1,typed_neighbors)
		#print('house at {} has this perc of neighbors similar: {}'.format(loc,perc_sim))
		return(perc_sim)



	def getNeighborLocations(self,loc):
		x = loc[0]
		y = loc[1]
		locs = set([(x+i,y+j) for i in range(-1,2) for j in range(-1,2) if (i,j)!=(0,0)])
		if x<=0:
			[locs.discard((-1,y+i)) for i in range(-1,2)]
		if x>=self.N-1:
			[locs.discard((self.N,y+i)) for i in range(-1,2)]
		if y<=0:
			[locs.discard((x+i,-1)) for i in range(-1,2)]
		if y>=self.N-1:
			[locs.discard((x+i,self.N)) for i in range(-1,2)]

		return(list(locs))



	def plotState(self,plot_axis=None):

		if plot_axis is None:
			fig, axes = plt.subplots(2,1,figsize=(6,10))
			state_ax = axes[1]
		else:
			state_ax = plot_axis

		width = 1.0
		height = 1.0

		block_width = width/self.N
		margin = block_width/10.0

		#cm = get_cmap('Paired')
		cm = get_cmap('inferno')

		box_margin = 0.008
		state_ax.clear()
		state_ax.add_patch(patches.Rectangle((-box_margin*width,-box_margin*width),(1+2*box_margin)*width,(1+2*box_margin)*height,linewidth=4,edgecolor='black',facecolor='black'))

		state_ax.set_xlim(-box_margin*width,(1+box_margin)*width)
		state_ax.set_ylim(-box_margin*width,(1+box_margin)*width)

		for i in range(self.N):
			for j in range(self.N):

				(x0,y0) = (i*block_width+margin,j*block_width+margin)
				rect_width = block_width - 2*margin

				color = cm(1.*self.grid[i,j].type/self.N_types)
				rect = patches.Rectangle((x0,y0),rect_width,rect_width,linewidth=2,edgecolor=color,facecolor=color)
				state_ax.add_patch(rect)

		state_ax.set_aspect('equal')
		state_ax.axis('off')
		#plt.tight_layout()
		#plt.show()



	def drawGrid(self,gen=200,state_plot_obj=None):


		fig, axes = plt.subplots(2,1,figsize=(6,12))
		graph_ax = axes[0]
		state_ax = axes[1]
		graph_ax_2 = graph_ax.twinx()
		fig.show()


		for i in range(gen):


			#graph_ax.plot(gen,best,label='best')

			graph_ax.clear()
			graph_ax_2.clear()
			graph_ax.plot(self.sim_avg,label='avg sim')
			graph_ax_2.plot(self.movement,label='moves',color='r')
			graph_ax.set_xlabel('# generations')
			graph_ax.set_ylabel('avg similarity')
			graph_ax_2.set_ylabel('moves taken')
			'''graph_ax.legend()
			graph_ax_2.legend()'''

			'''
			graph_ax.set_ylabel('fitness function')
			#graph_ax.plot(gen,mean,label='mean')
			'''

			#graph_ax.text(.6*i,.8*max(best),'best: {:.3f}\nmean: {:.3f}'.format(cur_best,cur_mean))

			'''if state_plot_obj is not None:
				state_plot_obj.copyState(self.sorted_population[0][0])
				state_plot_obj.plotState(plot_axis=axes[1])'''


			self.plotState(plot_axis=state_ax)

			fig.canvas.draw()

			self.moveStep()


		date_string = datetime.now().strftime("%H-%M-%S")
		plt.savefig('neighborhoods_' + date_string + '.png')
		#plt.savefig('neighborhoods_' + self.class_name + '__pop=' + str(self.popsize) + '__gen=' + str(generations) + '__' + self.kwargs_str + '__' + date_string + '.png')

		return(0)


	def makeGif(self):
		os.system('convert @image_list.txt {}/{}.gif'.format(picPath,gif_name)) # On windows convert is 'magick'
















#
