import math

class	Vec2:
	def	__init__(self, x, y):
		self.x = x
		self.y = y

class	Ball:
	def	__init__(self, coor, size, direction, velocity, ai):
		self.coor = coor
		self.size = size
		self.dir = direction
		self.vel = velocity
		self.ai = ai
	def	update(self):
		self.coor.x += self.dir.x
		self.coor.y += self.dir.y
	def	velUpdate(self):
		self.vel.x += self.vel.y
	def	getXMin(self):
		return (self.coor.x)
	def	getXMax(self):
		return (self.coor.x + self.size.x)
	def	getYMin(self):
		return (self.coor.y)
	def	getYMax(self):
		return (self.coor.y + self.size.y)
	def	getXDir(self):
		return (self.dir.x)
	def	getYDir(self):
		return (self.dir.y)
	def	getVel(self):
		return (self.vel.x)
	def	setXMin(self, x):
		self.coor.x = x
	def	setYMin(self, y):
		self.coor.y = y
	def	setXSize(self, x):
		self.size.x = x
	def	setYSize(self, y):
		self.size.y = y
	def	setXDir(self, x):
		self.dir.x = x
	def	setYDir(self, y):
		self.dir.y = y
	def	getMiddleHeight(self):
		return (self.coor.y + self.size.y / 2)

class	Paddle:
	def	__init__(self, coor, size):
		self.coor = coor
		self.size = size
	def	getCenter(self):
		return (Vec2(self.coor.x + self.size.x / 2,
		  			self.coor.y + self.size.y / 2))
	def	getXMin(self):
		return (self.coor.x)
	def	getXMax(self):
		return (self.coor.x + self.size.x)
	def	getYMin(self):
		return (self.coor.y)
	def	getYMax(self):
		return (self.coor.y + self.size.y)
	def	setXMin(self, x):
		self.coor.x = x
	def	setYMin(self, y):
		self.coor.y = y
	def	setXSize(self, x):
		self.size.x = x
	def	setYSize(self, y):
		self.size.y = y
	def	getMiddleHeight(self):
		return (self.coor.y + self.size.y / 2)
	def	getHitZone(self, ball):
		a = (ball.getMiddleHeight() - self.getYMin()) / self.size.y	* 100
		if (a < 0 or a > 100):
			return (0)
		return (a % 50)

def	angleCalculation(c):
	a = -1.0
	b = 0.0
	d = 50.0
	e = 90.0
	r = (e * (c - a) + b * (a  - d)) / (d - a)
	return (r)

def	checkCollisionBallWithPaddle(ball, paddle):
	if ((ball.getXMin() <= paddle.getXMax()) or (ball.getXMax() >= paddle.getXMin())):
		if ((ball.getYMax() >= paddle.getYMin()) and (ball.getYMin() <= paddle.getYMax())):
			x = paddle.getHitZone(ball)
			if (ball.getMiddleHeight() == paddle.getMiddleHeight()):
				angle = 90.0
			else:
				angle = angleCalculation(x)
			ball.velUpdate()
			ball.setXDir(math.sin(math.radians(angle)) * ball.getVel())
			ball.setYDir(math.cos(math.radians(angle)) * ball.getVel())
			if (ball.getMiddleHeight() < paddle.getMiddleHeight()):
				ball.setYDir(ball.getYDir() * -1)

def checkCollisionOfPaddleWithEdge(paddle):
	if (paddle.coor.y < 0):
		paddle.coor.y = 0
	if (paddle.coor.y + paddle.size.y):
		paddle.coor.y = 100 - paddle.size.y

def	checkCollisionBallWithEdge(ball):
	if (ball.coor.y - ball.radius <= 0 or ball.coor.y + ball.radius >= 100):
		ball.vel.y *= -1

