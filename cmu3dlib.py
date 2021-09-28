from cmu_graphics import *
import math
import glm

# Matrix to convert -1:1 screen coordinates to pixel coordinates
def viewport(width: float, height: float):
	x1 = 0
	y1 = 0
	x2 = width
	y2 = height

	result = glm.mat4(0)

	result[0][0] = (x2 - x1) / 2
	result[1][1] = (y2 - y1) / 2
	result[2][2] = 0.5
	result[3][3] = 1
	result[3][2] = 0.5
	result[3][1] = (y2 + y1) / 2
	result[3][0] = (x2 + x1) / 2

	return result

def getNormal(v1: glm.vec3, v2: glm.vec3, v3: glm.vec3):
	return glm.cross(v2 - v1, v3 - v1)

def Vec4toVec3(vec: glm.vec4):
	return glm.vec3(vec.x, vec.y, vec.z)

class Mesh:
	Vertices: list
	Indices: list
	Position: glm.vec3
	Scale: glm.vec3
	Rotation: glm.mat4

	def __init__(self, vertices: list, indices: list):
		self.Vertices = vertices
		self.Indices = indices
		self.Position = glm.vec3(0, 0, 0)
		self.Scale = glm.vec3(1, 1, 1)
		self.Rotation = glm.mat4(1)

	def GetTransformedVertices(self):
		vertices = []

		model = self.Rotation * glm.scale(glm.mat4(1), self.Scale) 
		for vertex in self.Vertices:
			# Apply transform
			result = glm.vec4(vertex.x, vertex.y, vertex.z, 1) * model
			result += glm.vec4(self.Position, 0)
			vertices.append(result)

		return vertices


class Camera:
	Position: glm.vec3
	LookVector: glm.vec3
	FOV: float
	NearClip: float
	FarClip: float


	def __init__(self, position: glm.vec3, lookVector: glm.vec3):
		self.Position = position
		self.LookVector = lookVector
		self.FOV = 70
		self.NearClip = 0.1
		self.FarClip = 100

	def GetViewMatrix(self):
		return glm.lookAt(self.Position, self.Position + glm.normalize(self.LookVector), glm.vec3(0, 1, 0))


class FlyCamera(Camera):
	Speed: float

	wPressed: bool
	aPressed: bool
	sPressed: bool
	dPressed: bool

	RightVector: glm.vec3

	def __init__(self, position: glm.vec3, lookVector: glm.vec3, speed: float):
		super().__init__(position, lookVector)
		self.Speed = speed

		self.wPressed = False
		self.aPressed = False
		self.sPressed = False
		self.dPressed = False

		self.RightVector = glm.normalize(glm.cross(glm.vec3(0, 1, 0), self.LookVector))

	def mouseMoved(self, offset: glm.vec2):
		rotationMat = glm.mat4(1)
		rotationMat = glm.rotate(rotationMat, glm.radians(-offset.x / 2), glm.vec3(0, 1, 0))

		self.RightVector = glm.normalize(glm.cross(glm.vec3(0, 1, 0), self.LookVector))
		rotationMat = glm.rotate(rotationMat, glm.radians(offset.y / 2), self.RightVector)

		self.LookVector = glm.vec3(rotationMat * glm.vec4(self.LookVector, 1))

	def keyChanged(self, key: str, state: bool):
		if key == 'w':
			self.wPressed = state
		elif key == 'a':
			self.aPressed = state
		elif key == 's':
			self.sPressed = state
		elif key == 'd':
			self.dPressed = state

	def step(self):
		movementAmount = self.Speed / app.stepsPerSecond

		if self.wPressed:
			self.Position += self.LookVector * movementAmount
		if self.aPressed:
			self.Position += self.RightVector * movementAmount
		if self.sPressed:
			self.Position -= self.LookVector * movementAmount
		if self.dPressed:
			self.Position -= self.RightVector * movementAmount


def indicesSort(indices, camPos, vertices):
	pos = (vertices[indices.x] + vertices[indices.y] + vertices[indices.z]) / 3
	return glm.distance(camPos, Vec4toVec3(pos))

class Renderer:
	@staticmethod
	def Draw(mesh: Mesh, camera: Camera, shadeFunc):
		view = camera.GetViewMatrix()
		projection = glm.perspective(glm.radians(camera.FOV), 1, camera.NearClip, camera.FarClip)
		pvmatrix = projection * view
		viewTransform = viewport(400, 400)

		vertices = mesh.GetTransformedVertices()
		indices = mesh.Indices.copy()
		indices.sort(reverse=True, key=lambda e : indicesSort(e, camera.Position, vertices)) # Sort triangles by distance to camera

		for triangle in indices:
			triVertices = [
				vertices[triangle.x],
				vertices[triangle.y],
				vertices[triangle.z]
			]

			# Cull triangles behind camera
			verticesInFront = 0
			for vertex in triVertices:
				dot = glm.dot(camera.LookVector, glm.normalize(glm.vec3(vertex) - camera.Position))

				if math.copysign(1, dot) == 1:
					verticesInFront += 1

			# Cull backfaces (this bit is kinda sus)
			shouldntCull = False
			normal = getNormal(
				glm.vec3(triVertices[0]), 
				glm.vec3(triVertices[1]), 
				glm.vec3(triVertices[2])
			)
			facingVector = glm.normalize(
				(glm.vec3(triVertices[0]) + glm.vec3(triVertices[1]) + glm.vec3(triVertices[2])) / 3 - camera.Position)
			if not glm.dot(normal, facingVector) >= 0 and math.copysign(1, glm.dot(facingVector, camera.LookVector)) == 1:
				shouldntCull = True

			if verticesInFront > 0 and shouldntCull:
				color = shadeFunc(
					Vec4toVec3(triVertices[0]), 
					Vec4toVec3(triVertices[1]), 
					Vec4toVec3(triVertices[2])
				)

				screenCoords = []
				for vertex in triVertices:
					# Apply view matrix and projection matrix
					vertex = pvmatrix * vertex

					if (vertex.w != 0):
						vertex.x /= vertex.w
						vertex.y /= vertex.w

					# Apply viewport transform
					vertex *= viewTransform

					# Convert to vec2 and put in list
					screenCoords.append(glm.vec2(vertex.x + 200, -vertex.y + 200))

				coordsOutScreen = 0
				for coord in screenCoords:
					if coord.x < 0 or coord.y < 0 or coord.x > 399 or coord.y > 399:
						coordsOutScreen += 1

				if coordsOutScreen < 3:
					Polygon(
						screenCoords[0].x, screenCoords[0].y,
						screenCoords[1].x, screenCoords[1].y,
						screenCoords[2].x, screenCoords[2].y,
						fill=rgb(color.x, color.y, color.z)
					)