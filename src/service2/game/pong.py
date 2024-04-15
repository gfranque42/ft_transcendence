class	vec2:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class	ball:
	def __init__(self, pos, velocity, size, shape):
		self.pos = pos
		self.velocity = velocity
		self.size = size
		self.shape = shape
	def update(self):
		self.pos.x += self.velocity.x
		self.pos.y += self.velocity.y
	def getHalfWidth(self):
		return (self.size.x / 2)
	def getHalfHeight(self):
		return (self.size.y / 2)
	def getCenter(self):
		return (vec2(self.pos.x + self.getHalfWidth(), self.pos.y + self.getHalfHeight()))

class	paddle:
	def __init__(self, pos, velocity, size, name):
		self.pos = pos
		self.velocity = velocity
		self.size = size
		self.name = name
		self.score = 0
		self.type = 0
		if (name == "AI"):
			self.type = 1
	def update(self):
		if (self.type == 1):
			return
		# self.pos.y += self.velocity.y
	def getHalfWidth(self):
		return (self.size.x / 2)
	def getHalfHeight(self):
		return (self.size.y / 2)
	def getCenter(self):
		return (vec2(self.pos.x + self.getHalfWidth(), self.pos.y + self.getHalfHeight()))

def	paddleAI(ball, paddle):
	if (paddle.type == 0):
		return
	if (ball.pos.x > paddle.pos.x and ball.velocity.x < 0):
		if (ball.pos.y > paddle.getCenter().y):
			paddle.pos.y += paddle.velocity.y
		if (ball.pos.y < paddle.getCenter().y):
			paddle.pos.y -= paddle.velocity.y
	if (ball.pos.x < paddle.pos.x and ball.velocity.x > 0):
		if (ball.pos.y > paddle.getCenter().y):
			paddle.pos.y += paddle.velocity.y
		if (ball.pos.y < paddle.getCenter().y):
			paddle.pos.y -= paddle.velocity.y

def	ballCollisionWithEdge(ball):
	if (ball.pos.y + ball.size.y >= 100 or ball.pos.y <= 0):
		ball.velocity.y *= -1

def	paddleCollisionWithEdge(paddle):
	if (paddle.pos.y < 0):
		paddle.pos.y = 0
	if (paddle.pos.y + paddle.size.y > 100):
		paddle.pos.y = 100 - paddle.size.y

def	ballPaddleCollision(ball, paddle):
	if (((ball.pos.y <= paddle.pos.y + paddle.size.y)
		and (ball.pos.y + ball.size.y >= paddle.pos.y))
		and (ball.pos.x <= (paddle.pos.x + paddle.size.x)
		or (ball.pos.x + ball.size.x) >= paddle.pos.x)):
		ball.velocity.x *= -1

def	respawnBall(ball):
	ball.pox.x = 50 - ball.getHalfWidth()
	ball.pos.y = 50 - ball.getHalfHeight()
	ball.velocity.x *= -1
	#mettre en place un vitesse normee ?
	#ajouter une velocite standard pour le respawn ?

def	increaseScore(ball, paddleG, paddleD):
	if (ball.pos.x < paddleG.pos.x + paddleG.size.x and ball.velocity.x < 0):
		paddleG.score += 1
		respawnBall(ball)
		return
	if (ball.pos.x + ball.size.x > paddleD.pos.x and ball.velocity.x > 0):
		paddleD.score += 1
		respawnBall(ball)
		return
	
def	gameUpdate(ball, paddleG, paddleD):
	ball.update()
	paddleG.update()
	paddleD.update()
	paddleAI(ball, paddleG)
	paddleAI(ball, paddleD)
	ballCollisionWithEdge(ball)
	paddleCollisionWithEdge(paddleG)
	paddleCollisionWithEdge(paddleD)
	ballPaddleCollision(ball, paddleG)
	ballPaddleCollision(ball, paddleD)
	increaseScore(ball, paddleG, paddleD)
