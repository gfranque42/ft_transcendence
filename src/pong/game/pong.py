class	Vec2:
	def	__init__(self, x, y):
		self.x = x
		self.y = y

class	Ball:
	def	__init__(self, coor, radius, direction, velocity, ai):
		self.coor = coor
		self.radius = radius
		self.dir = direction
		self.vel = velocity
		self.ai = ai
	def	update(self):
		self.coor.x += self.vel.x
		self.coor.y += self.vel.y
	def	getXMin(self):
		return (self.coor.x)
	def	getXMax(self):
		return (self.coor.x + self.radius)
	def	getYMin(self):
		return (self.coor.y)
	def	getYMax(self):
		return (self.coor.y + self.radius)

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
	def	setXMax(self, x):
		self.coor.x = x - self.size.x
	def	setYMin(self, y):
		self.coor.y = y
	def	setYMax(self, y):
		self.coor.y = y - self.size.y

def	checkCollisionBallWithPaddle(ball, paddle):
	if (ball.coor.x < 50 and ball.coor.x - ball.radius < paddle.coor.x + paddle.size.x) or (ball.coor.x > 50 and ball.coor.x + ball.radius > paddle.coor.x):
		ball.vel.x *= -1
		ball.vel.y *= -1

def checkCollisionOfPaddleWithEdge(paddle):
	if (paddle.coor.y < 0):
		paddle.coor.y = 0
	if (paddle.coor.y + paddle.size.y):
		paddle.coor.y = 100 - paddle.size.y

def	checkCollisionBallWithEdge(ball):
	if (ball.coor.y - ball.radius <= 0 or ball.coor.y + ball.radius >= 100):
		ball.vel.y *= -1

