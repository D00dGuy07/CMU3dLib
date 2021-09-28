from cmu_graphics import *
from opensimplex import OpenSimplex
import random
import math
import glm
import cmu3dlib

app.setMaxShapeCount(10000)

class World:
	Data: list
	Size: int

	def __init__(self, size: int):
		self.Size = size
		self.Data = [] # Data stored in nested list
		for x in range(size):
			self.Data.append([])
			for y in range(size):
				self.Data[x].append([])
				for z in range(size):
					self.Data[x][y].append(0)

	def GetVoxel(self, x: int, y: int, z: int):
		return self.Data[x][y][z]

	def SetVoxel(self, value: int, x: int, y: int, z: int):
		self.Data[x][y][z] = value

class WorldMeshBuilder:
	@staticmethod
	def getNeighbors(world: World, x: int, y: int, z: int):
		return {
			"Front"  : 1 if (z - 1) <  0          else world.GetVoxel(x,     y,     z - 1),
			"Back"   : 1 if (z + 1) >= world.Size else world.GetVoxel(x,     y,     z + 1),
			"Left"   : 1 if (x - 1) <  0          else world.GetVoxel(x - 1, y,     z),
			"Right"  : 1 if (x + 1) >= world.Size else world.GetVoxel(x + 1, y,     z),
			"Bottom" : 1 if (y - 1) <  0          else world.GetVoxel(x,     y - 1, z),
			"Top"    : 1 if (y + 1) >= world.Size else world.GetVoxel(x,     y + 1, z)
		}

	@staticmethod
	def GenMesh(world: World):
		verticesCount = 0

		vertices = []
		indices = []
		for x in range(world.Size):
			for y in range(world.Size):
				for z in range(world.Size):
					voxel = world.GetVoxel(x, y, z)
					neighbors = WorldMeshBuilder.getNeighbors(world, x, y, z)

					worldCoords = glm.vec3(x - world.Size / 2, y - world.Size / 2, z - world.Size / 2)
					if voxel == 1 and neighbors["Front"] == 0:
						vertices.append(glm.vec3( 0.5, -0.5, -0.5) + worldCoords)
						vertices.append(glm.vec3(-0.5, -0.5, -0.5) + worldCoords)
						vertices.append(glm.vec3(-0.5,  0.5, -0.5) + worldCoords)
						vertices.append(glm.vec3( 0.5,  0.5, -0.5) + worldCoords)
						indices.append(glm.ivec3(0 + verticesCount, 1 + verticesCount, 2 + verticesCount))
						indices.append(glm.ivec3(2 + verticesCount, 3 + verticesCount, 0 + verticesCount))
						verticesCount += 4
					if voxel == 1 and neighbors["Back"] == 0:
						vertices.append(glm.vec3(-0.5, -0.5,  0.5) + worldCoords)
						vertices.append(glm.vec3( 0.5, -0.5,  0.5) + worldCoords)
						vertices.append(glm.vec3( 0.5,  0.5,  0.5) + worldCoords)
						vertices.append(glm.vec3(-0.5,  0.5,  0.5) + worldCoords)
						indices.append(glm.ivec3(0 + verticesCount, 1 + verticesCount, 2 + verticesCount))
						indices.append(glm.ivec3(2 + verticesCount, 3 + verticesCount, 0 + verticesCount))
						verticesCount += 4
					if voxel == 1 and neighbors["Left"] == 0:
						vertices.append(glm.vec3(-0.5, -0.5, -0.5) + worldCoords)
						vertices.append(glm.vec3(-0.5, -0.5,  0.5) + worldCoords)
						vertices.append(glm.vec3(-0.5,  0.5,  0.5) + worldCoords)
						vertices.append(glm.vec3(-0.5,  0.5, -0.5) + worldCoords)
						indices.append(glm.ivec3(0 + verticesCount, 1 + verticesCount, 2 + verticesCount))
						indices.append(glm.ivec3(2 + verticesCount, 3 + verticesCount, 0 + verticesCount))
						verticesCount += 4
					if voxel == 1 and neighbors["Right"] == 0:
						vertices.append(glm.vec3( 0.5, -0.5,  0.5) + worldCoords)
						vertices.append(glm.vec3( 0.5, -0.5, -0.5) + worldCoords)
						vertices.append(glm.vec3( 0.5,  0.5, -0.5) + worldCoords)
						vertices.append(glm.vec3( 0.5,  0.5,  0.5) + worldCoords)
						indices.append(glm.ivec3(0 + verticesCount, 1 + verticesCount, 2 + verticesCount))
						indices.append(glm.ivec3(2 + verticesCount, 3 + verticesCount, 0 + verticesCount))
						verticesCount += 4
					if voxel == 1 and neighbors["Top"] == 0:
						vertices.append(glm.vec3(-0.5,  0.5,  0.5) + worldCoords)
						vertices.append(glm.vec3( 0.5,  0.5,  0.5) + worldCoords)
						vertices.append(glm.vec3( 0.5,  0.5, -0.5) + worldCoords)
						vertices.append(glm.vec3(-0.5,  0.5, -0.5) + worldCoords)
						indices.append(glm.ivec3(0 + verticesCount, 1 + verticesCount, 2 + verticesCount))
						indices.append(glm.ivec3(2 + verticesCount, 3 + verticesCount, 0 + verticesCount))
						verticesCount += 4
					if voxel == 1 and neighbors["Bottom"] == 0:
						vertices.append(glm.vec3(-0.5, -0.5, -0.5) + worldCoords)
						vertices.append(glm.vec3( 0.5, -0.5, -0.5) + worldCoords)
						vertices.append(glm.vec3( 0.5, -0.5,  0.5) + worldCoords)
						vertices.append(glm.vec3(-0.5, -0.5,  0.5) + worldCoords)
						indices.append(glm.ivec3(0 + verticesCount, 1 + verticesCount, 2 + verticesCount))
						indices.append(glm.ivec3(2 + verticesCount, 3 + verticesCount, 0 + verticesCount))
						verticesCount += 4

		return cmu3dlib.Mesh(vertices, indices)

def GenWorld(world: World, seed: int, smoothing):
	noiseGen = OpenSimplex(seed=seed)
	for x in range(world.Size):
		for z in range(world.Size):
			height = (noiseGen.noise2d(x / smoothing, z / smoothing) / 2 + 1) * (world.Size / 2 - 3)
			for y in range(world.Size):
				if y <= height:
					world.SetVoxel(1, x, y, z)

world = World(30)

seed = random.randint(0, 1000000)
print(seed)
GenWorld(world, seed, 15)

mesh = WorldMeshBuilder.GenMesh(world)
mesh.Position = glm.vec3(0, 0, -10)

camera = cmu3dlib.FlyCamera(glm.vec3(0, 0, 0), glm.vec3(0, 0, -1), 5)

color = glm.vec3(170, 100, 230)
def shadeFunction(v1, v2, v3):
	normal = cmu3dlib.getNormal(v1, v2, v3)

	# Shading hack
	if normal == glm.vec3(0, 0, -1): # Front
		return color * 0.7
	elif normal == glm.vec3(0, 0, 1): # Back
		return color * 0.86
	elif normal == glm.vec3(-1, 0, 0): # Left
		return color * 0.8
	elif normal == glm.vec3(1, 0, 0): # Right
		return color * 0.75
	elif normal == glm.vec3(0, 1, 0): # Top
		return color
	elif normal == glm.vec3(0, -1, 0): # Bottom
		return color * 0.67

	return glm.vec3(0, 0, 0)

def colorShadeFunction(v1, v2, v3):
	normal = cmu3dlib.getNormal(v1, v2, v3)

	# Shading hack
	if normal == glm.vec3(0, 0, -1): # Front
		return glm.vec3(105, 59, 10)#glm.vec3(52, 229, 235)
	elif normal == glm.vec3(0, 0, 1): # Back
		return glm.vec3(105, 59, 10)#glm.vec3(52, 235, 137)
	elif normal == glm.vec3(-1, 0, 0): # Left
		return glm.vec3(105, 59, 10)#glm.vec3(235, 73, 52)
	elif normal == glm.vec3(1, 0, 0): # Right
		return glm.vec3(105, 59, 10)#glm.vec3(235, 171, 52)
	elif normal == glm.vec3(0, 1, 0): # Top
		return glm.vec3(99, 245, 66)#glm.vec3(208, 52, 235)
	elif normal == glm.vec3(0, -1, 0): # Bottom
		return glm.vec3(105, 59, 10)#glm.vec3(235, 52, 119)

	return glm.vec3(0, 0, 0)

def onStep():
	global mesh
	global camera
	camera.step()

	app.group.clear()
	cmu3dlib.Renderer.Draw(mesh, camera, colorShadeFunction)

lastMouseX = None
lastMouseY = None
def onMouseDrag(mouseX, mouseY):
	global lastMouseX
	global lastMouseY
	global camera

	if lastMouseX == None and lastMouseY == None:
		lastMouseX = mouseX
		lastMouseY = mouseY
		return

	offset = glm.vec2(mouseX - lastMouseX, mouseY - lastMouseY)
	camera.mouseMoved(offset)

	lastMouseX = mouseX
	lastMouseY = mouseY

def onMouseMove(mouseX, mouseY):
	global lastMouseX
	global lastMouseY
	lastMouseX = mouseX
	lastMouseY = mouseY

def onKeyPress(key):
	global camera
	camera.keyChanged(key, True)

def onKeyRelease(key):
	global camera
	camera.keyChanged(key, False)