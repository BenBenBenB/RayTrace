# Optics Ray Tracer Program 1
# Made by Ben Burton for Dr. Eric Klumpe for PHYS 3520


import matplotlib.pyplot as plt
from math import pi

# A simple class to keep track of points along the ray.
# x is height from center of lens
# z is in the direction of propagation direction
# alpha is angle from z-axis

class Ray:
	# Input initial values and lenses.
	# lenses must have at least 1 lens and be ordered by position along z-axis
	# Input angle is in radians
	# x is distance from center of lens, z is in direction of propagation
	def __init__(self, lenses, alpha_incident, z_init, x_init):
		# Populate initial values (these are left of 1st lens)
		self.z = [z_init]
		self.x = [x_init]
		self.alpha = [alpha_incident]

		# Calculate x and z at first lens
		d = lenses[0].pos - z_init
		self.x.append(d*alpha_incident+x_init)
		self.z.append(lenses[0].pos)

		# Calculate positions and angles iteratively for each lens.
		for i in range(len(lenses)-1):
			d = lenses[i+1].pos - lenses[i].pos
			x1 = self.x[-1]
			a1 = self.alpha[-1]
			self.z.append(lenses[i+1].pos)
			# lens: a2 = a1 - x1/f
			self.alpha.append(a1 - x1/lenses[i].f)
			# slab: x2 = d*a1 + x1
			self.x.append(d * self.alpha[-1] + x1)

		# For final lens, base d on focal length
		# Maybe change this later for pupil purposes
		if len(lenses) >= 2:
			d = 1/(1/lenses[-1].f-1/(lenses[-1].f+lenses[-2].f))
		else:
			d = abs(lenses[-1].f)*1.5
			#print("Eye relief is %2.2d" % d)
		self.alpha.append(self.alpha[-1] - self.x[-1]/lenses[-1].f)
		self.z.append(self.z[-1] + d)
		self.x.append(d * self.alpha[-1] + self.x[-1])

		# Calculate final ray out to distance based on focal length

# Holds info on a lens
# Inputs: position, diameter, index, r_left, r_right
class Lens:
	def __init__(self, position, diameter, index, r_left, r_right):
		self.pos = position # not used but maybe later for multiple lenses
		self.diameter = diameter # diameter of lens
		self.index = index
		self.r_left = r_left
		self.r_right= r_right
		self.f = 1/((index - 1)*(1/r_left - 1/r_right))

	def plot(self):
			plt.plot([self.pos,self.pos],[self.diameter/2,-self.diameter/2],linewidth=4, color='b',alpha=0.5)

# A glorified list of lenses
class OpticalBench:
	def __init__(self):
		self.lenses = []

	# add a lens in the correct list position
	def add(self, new_lens):
		i=0
		while (i < len(self.lenses) and self.lenses[i].pos < new_lens.pos):
			i+=1
		self.lenses.insert(i, new_lens)

	# Remove lens at specified position
	def remove(self, position):
		for i in range(len(self.lenses)):
			if (self.lenses[i].pos == position):
				self.lenses.pop(i)
				return True
		return False

	# Return True if a lens is at specified position
	def has(self, position):
		for i in range(len(self.lenses)):
			if (self.lenses[i].pos == position):
				return True
		return False

	# used for debug purposes,
	def display(self):
		for i in range(len(self.lenses)):
			print(self.lenses[i].pos)
		if len(self.lenses) == 0:
			print('empty')


# This class will create a graph of the rays using pyplot
class RayTrace:
	# Generate each ray object from top to bottom, adding each to the plot
	def __init__(self, num_rays, lenses, z_init = None, x_init = None, alpha = None):
		# First, plot the lenses
		self.lenses = lenses
		self.num_rays = num_rays
		self.rays = []

		for lens in self.lenses:
			lens.plot()
		# Now Plot all rays
		if (alpha == None):
			plt.title("Ray Trace for Point Source")
			self.plot_point_source(num_rays, lenses, z_init, x_init)
		else:
			plt.title("Ray Trace for Collimated Source")
			alpha *= alpha*pi/180
			self.plot_collimated(num_rays, lenses, alpha)

		# Add in pretty plot options here.
		plt.axhline(color='k',linewidth=0.5,alpha=0.5)

		# Get some numbers:
		#Transverse magnification:
		#d1 = self.rays[0]

	# These are necessary since we want the top and bottom rays 
	# to hit the top and bottom of first lens
	def plot_collimated(self, num_rays, lenses, alpha):
		# plot rays from top to bottom position at first lens
		d = abs(lenses[0].f)
		x_init = lenses[0].diameter/2-d*alpha
		z_init = lenses[0].pos - d
		for i in range(self.num_rays):
			ray = Ray(lenses,alpha,z_init, x_init)
			self.rays.append(ray)
			plt.plot(ray.z, ray.x)
			x_init -= lenses[0].diameter/(num_rays-1)


	def plot_point_source(self, num_rays, lenses, z_init, x_init):
		# first, get initial angle to hit top of lens
		d = lenses[0].pos - z_init
		x2 = lenses[0].diameter/2
		alpha = (x2 - x_init)/d
		# Now plot every ray for every angle
		for i in range(self.num_rays):
			ray = Ray(lenses,alpha,z_init, x_init)
			plt.plot(ray.z, ray.x)
			alpha -= lenses[0].diameter/(num_rays-1)/d