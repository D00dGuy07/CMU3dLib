from cmu_graphics import *
import math
import glm
import cmu3dlib

vertices = [
	glm.vec3(-0.5, -0.5,  0.5),
	glm.vec3( 0.5, -0.5,  0.5),
	glm.vec3( 0.5,  0.5,  0.5),
	glm.vec3(-0.5,  0.5,  0.5),

	glm.vec3(-0.5, -0.5, -0.5),
	glm.vec3( 0.5, -0.5, -0.5),
	glm.vec3( 0.5,  0.5, -0.5),
	glm.vec3(-0.5,  0.5, -0.5)
]

indices = [
	glm.ivec3(0, 1, 2),
	glm.ivec3(2, 3, 0),

	glm.ivec3(4, 0, 3),
	glm.ivec3(3, 7, 4),

	glm.ivec3(5, 4, 7),
	glm.ivec3(7, 6, 5),

	glm.ivec3(1, 5, 6),
	glm.ivec3(6, 2, 1),

	glm.ivec3(3, 2, 6),
	glm.ivec3(6, 7, 3),

	glm.ivec3(4, 5, 1),
	glm.ivec3(1, 0, 4)
]

mesh = cmu3dlib.Mesh(vertices, indices)
mesh.Position = glm.vec3(0, 0, -5)

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
		return glm.vec3(52, 229, 235)
	elif normal == glm.vec3(0, 0, 1): # Back
		return glm.vec3(52, 235, 137)
	elif normal == glm.vec3(-1, 0, 0): # Left
		return glm.vec3(235, 73, 52)
	elif normal == glm.vec3(1, 0, 0): # Right
		return glm.vec3(235, 171, 52)
	elif normal == glm.vec3(0, 1, 0): # Top
		return glm.vec3(208, 52, 235)
	elif normal == glm.vec3(0, -1, 0): # Bottom
		return glm.vec3(235, 52, 119)

	return glm.vec3(0, 0, 0)

def onStep():
	global mesh
	global camera
	camera.step()

	app.group.clear()
	print(camera.Position)
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