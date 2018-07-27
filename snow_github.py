import random
import time
from math import sqrt, ceil
import numpy as np
import matplotlib.pyplot as plt


class triangular_mesh():

	def __init__(self, mesh_length, nucleus_upper_limit):
		self.mesh_length = mesh_length 
		self.nucleus = set(((0, 0))) 
		self.nucleus_upper_limit = nucleus_upper_limit 
		self.nucleus_num = 1 

	def nearby_six_position(self, snow_coordinate):
	
		nearby_vector = {
		1 : [1, 0],
		2 : [0, 1],
		3 : [-1, 1],
		4 : [1 , -1],
		5 : [-1, 0],
		6 : [0, -1]
		}		
		for key in nearby_vector:
			nearby_vector[key][0] += snow_coordinate[0]
			nearby_vector[key][1] += snow_coordinate[1]
		#print (nearby_vector)
		return nearby_vector


	def check_nucleus(self, snow_coordinate):

		if tuple(snow_coordinate) == (0, 0):
			return 1
		if tuple(snow_coordinate) in self.nucleus:
			return 1

		nearby_vector = self.nearby_six_position(snow_coordinate)
		for key in nearby_vector:
			if nearby_vector[key] == [0, 0]:
				return 2
			if tuple(nearby_vector[key]) in self.nucleus:
				return 2

		return 0

	def add_nucleus(self, snow_coordinate):

		self.nucleus.add(tuple(snow_coordinate))
		self.nucleus_num += 1
		 

	def check_out_bound(self, snow_coordinate):
	
		if snow_coordinate[0] >= 0:
			if snow_coordinate[0] > self.mesh_length or snow_coordinate[1] > self.mesh_length - snow_coordinate[0] or snow_coordinate[1] < -self.mesh_length:
				return True
			else:
				return False
		else:
			if snow_coordinate[0] < -self.mesh_length or snow_coordinate[1] < -self.mesh_length - snow_coordinate[0] or snow_coordinate[1] > self.mesh_length:
				return True
			else:
				return False


class snow_flake():
	# 雪粒类
	def __init__(self, mesh_length): 
		base_vector_one_weight = random.randint(-mesh_length, mesh_length)


		if base_vector_one_weight >= 0:
			base_vector_two_weight = random.randint(-mesh_length, mesh_length - base_vector_one_weight)
		else:
			base_vector_two_weight = random.randint(-mesh_length - base_vector_one_weight, mesh_length)

		self.coordinate = [
			base_vector_one_weight, 
			base_vector_two_weight, 
			]

	def random_walk_one_step(self, choice_from):

		random_vector_mode = {
		1 : [1, 0],
		2 : [0, 1],
		3 : [-1, 1],
		4 : [1 , -1],
		5 : [-1, 0],
		6 : [0, -1]
		}

		choose_mode = random.choice(choice_from)
		self.coordinate[0] += random_vector_mode[choose_mode][0]
		self.coordinate[1] += random_vector_mode[choose_mode][1]


class snow_simulate():

	def __init__(self, mesh_length, nucleus_upper_limit, wind_level):

		if wind_level < 0 or wind_level > 1/6:
			print ("wind_level must satisfies: 0 <= wind_level <= 1/6 !")
			exit()

		self.triangular_mesh = triangular_mesh(mesh_length, nucleus_upper_limit)
		decrease_p_num = ceil((1/6 - wind_level) * 5000)
		increase_p_num = ceil((1/6 + wind_level) * 5000)
		self.choice_from = \
		[1] * decrease_p_num + \
		[2] * decrease_p_num + \
		[3] * decrease_p_num + \
		[4] * increase_p_num + \
		[5] * increase_p_num + \
		[6] * increase_p_num

	def random_walk(self):

		temp_snow_flake = snow_flake(self.triangular_mesh.mesh_length)
		#print (temp_snow_flake.coordinate)
		while True:
			flag = self.triangular_mesh.check_nucleus(temp_snow_flake.coordinate)
		
			if flag == 1:
				return False

			elif flag == 2: 
				self.triangular_mesh.add_nucleus(temp_snow_flake.coordinate)
				#print ('add')
				return True

			elif flag == 0:
				temp_snow_flake.random_walk_one_step(self.choice_from)
				#print (temp_snow_flake.coordinate)
				if self.triangular_mesh.check_out_bound(temp_snow_flake.coordinate):
					return False

	def check_nucleus_upper_limit(self):

		temp = self.triangular_mesh.mesh_length
		total_vertices = 3 * temp**2 + 3 * temp + 1
		if self.triangular_mesh.nucleus_upper_limit > total_vertices:
			print ('nucleus_upper_limit must be equal or lower than mesh_length!')
			exit()

	def save_nucleus_xy(self):

		with open('nucleus.txt', 'w') as f:
			for temp_vector_nucleus in self.triangular_mesh.nucleus:
				if temp_vector_nucleus == 0:
					f.write('0\t0\n')
				else:
					temp_xy_nucleus = self.convert_vector_to_xy(temp_vector_nucleus)
					f.write(str(temp_xy_nucleus[0]) + '\t' + str(temp_xy_nucleus[1]) + '\n')

	def convert_vector_to_xy(self, nucleus_vector):


		x = nucleus_vector[1] + (1/2) * nucleus_vector[0]
		y = (sqrt(3)/2) * nucleus_vector[0]			
		return (x, y)


	def visualization(self):

		plt.figure(figsize = (10, 7), dpi = 80)
		with open('nucleus.txt', 'r') as f:
			for line in f:
				#print (line.strip())
				x = float(line.split('\t')[0])
				y = float(line.split('\t')[1])
				plt.scatter(x, y, s = 4, color = 'b')
		plt.axis([-self.triangular_mesh.mesh_length, self.triangular_mesh.mesh_length, -(sqrt(3)/2) * self.triangular_mesh.mesh_length, (sqrt(3)/2) * self.triangular_mesh.mesh_length])

		x = np.linspace(-self.triangular_mesh.mesh_length, self.triangular_mesh.mesh_length, 1000)
		y = sqrt(3) * x
		plt.plot(x, y, color = '#666262', linestyle = '--')
		y = -sqrt(3) * x
		plt.plot(x, y, color = '#666262', linestyle = '--')
		y = np.zeros(1000)
		plt.plot(x, y, color = '#666262', linestyle = '--')
		plt.show()


	def start(self):
		self.check_nucleus_upper_limit()
		while self.triangular_mesh.nucleus_num < self.triangular_mesh.nucleus_upper_limit:
			self.random_walk()
		self.save_nucleus_xy()


time_start = time.clock()

sim = snow_simulate(mesh_length = 90, nucleus_upper_limit = 3000, wind_level = 0)
sim.start()

time_end = time.clock()
print ('Time Elapsed: %f' % (time_end - time_start))
sim.visualization()
#print (sim.triangular_mesh.nucleus)


