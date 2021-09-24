from cmu_graphics import *
import math
import glm

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

triHeight = (math.sqrt(3)/2) * 1

points = [
	glm.vec3(-1, -triHeight, 0),
	glm.vec3(1, -triHeight, 0),
	glm.vec3(0, triHeight, 0)
]

projection = glm.perspective(glm.radians(70), 1, 0.1, 100)
model = glm.mat4(1)
viewTransform = viewport(400, 400)

def onStep():
	global model
	model = glm.rotate(model, glm.radians(1), glm.vec3(0, 1, 0))
	app.group.clear()
	draw()

def draw():

	transformed_points = []
	new_points = []
	for point in points:
		# Translate and Rotate
		result = glm.vec4(point.x, point.y, point.z, 1) * model
		result = result + glm.vec4(0, 0, -10, 0)

		transformed_points.append(glm.vec3(result))

		# Project and apply viewport transform
		result *= projection
		if (result.w != 0):
			result.x /= result.w
			result.y /= result.w
		result *= viewTransform
		new_points.append(glm.vec2(result.x + 200, -result.y + 200))

	# Draw triangle
	Polygon(
		new_points[0].x,
		new_points[0].y,
		new_points[1].x,
		new_points[1].y,
		new_points[2].x,
		new_points[2].y
	)