#from numarray import *
#from numpy import *

import random

class Puzzle():
	width = 0
	height = 0
	karta = None
	
	def __init__ (self,w,h):
		self.width = w
		self.height = h
		
		self.karta = []
		for i in range(0,h):
			init = 0
			add = []
			for j in range(0,w):
				add.append(init)
			self.karta.append(add)
		self.init()
	
	# fill with ones and zeroes,
	# make sure that everything fits (all constraints are satisfied)
	def init(self):
		def nextline(prevline):
			def genline(size):
				for i in range(0,size):
					r = int(round(random.random()))
					
			nextline = []
			for i in range(0,len(prevline)):
				r = int(round(random.random()))
				
		def all_connected(karta):
			#try:
			out = ""
			for i in range(0,self.height):
				for j in range(0,self.width):
					if self.karta[i][j] == 1:
						neighbours = self.get_neighbours(i,j)
						out = "%s\n(%d,%d) : %s " % (out,i,j,neighbours) 
						if 1 not in neighbours:
							return False

			#except:
			#	pass
			print out
			return True
		
		# {zero} maps often generated randomly, so we need some ones at least
		def enough_ones(karta,minimum_ones):
			anzahl = 0
			for i in range(0,self.height):
				for j in range(0,self.width):
					if self.karta[i][j] == 1:
						anzahl = anzahl + 1
			return anzahl >= minimum_ones
						
		def valid_karta(karta):
			return all_connected(karta) and enough_ones(karta,1)
		# generate the map randomly
		attempt = 0
		while not valid_karta(self.karta):
			for i in range(0,self.height):
				for j in range(0,self.width):
					self.karta[i][j] = int(round(random.random()))
			attempt = attempt + 1
		print "Attempt #%s" % attempt
			
	# array of 2-4 neighbour values sorrunging the tile
	def get_neighbours(self,i,j):
		neighbours = []
		try:
			if i > 0:
				neighbours.append(self.karta[i-1][j])
			if i < self.width-1:
				neighbours.append(self.karta[i+1][j])
			if j > 0:
				neighbours.append(self.karta[i][j-1])
			if j < self.height-1:
				neighbours.append(self.karta[i][j+1])
		except IndexError:
			raise
		return neighbours
	
	def get_all_connected(self,i,j):
		neighbours = self.get_neighbours(i,j)
		
		
		
		
	
	# prints the map as a square. if debug is true, prints coordinates too
	def pprint(self,debug=False):
		result = ""
		for i in range(0,self.height):
			line = ""
			for j in range(0,self.width):
				e = self.karta[i][j]
				if not debug:
					line = "%s %s" % (line , e)
				else:
					line = "%s %s (%d,%d)" % (line , e, i , j)
			result = "%s%s\n" % (result, line)
		return result.rstrip("\n")

def main():
	import sys
	try:
		# command line
		n = int(sys.argv[1])
	except:
		n = 6 # default
	p = Puzzle(n,n)
	debug = False
	print p.pprint(debug)

main()
