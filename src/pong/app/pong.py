import math


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ball:
    def __init__(self, coor, size, angle, velocity):
        self.coor = coor
        self.size = size
        self.dir = Vec2(0, 0)
        self.angle = angle
        self.vel = velocity
        self.start = coor
        self.startangle = angle
        self.startvel = velocity

    def update(self):
        self.coor.x += self.dir.x
        self.coor.y += self.dir.y

    def update_dir(self):
        self.dir.x = math.cos(math.radians(self.angle)) * self.vel
        self.dir.y = math.sin(math.radians(self.angle)) * self.vel

    def reset(self):
        self.coor.x = 100 / 2 - self.size.x / 2
        self.coor.y = 100 / 2 - self.size.y / 2
        self.vel = self.startvel
        self.startangle = self.startangle + 180
        self.angle = self.startangle
        self.dir.x = 0
        self.dir.y = 0


class Paddle:
    def __init__(self, coor, size, vel, ai):
        self.coor = coor
        self.size = size
        self.dir = 0
        self.key = 0
        self.vel = vel
        self.ai = ai

    def update_ai(self, Ball):
        if self.ai == 1 and Ball.dir.x > 0 and Ball.coor.x > 50:
            self.dir = 0
            if self.size.y / 2 + self.coor.y < Ball.size.y / 2 + Ball.coor.y:
                self.dir = self.vel
            elif self.size.y / 2 + self.coor.y > Ball.size.y / 2 + Ball.coor.y:
                self.dir = -self.vel
        elif self.ai == 2 and Ball.dir.x > 0:
            self.dir = 0
            if self.size.y / 2 + self.coor.y < Ball.size.y / 2 + Ball.coor.y:
                self.dir = self.vel
            elif self.size.y / 2 + self.coor.y > Ball.size.y / 2 + Ball.coor.y:
                self.dir = -self.vel
        elif self.ai == 3:
            self.dir = 0
            if self.size.y / 2 + self.coor.y < Ball.size.y / 2 + Ball.coor.y:
                self.dir = self.vel
            elif self.size.y / 2 + self.coor.y > Ball.size.y / 2 + Ball.coor.y:
                self.dir = -self.vel

    def update(self):
        self.coor.y += self.dir
        self.dir = self.key
        self.key = 0


def AngleInterpolation(
    ymin: float, ymax: float, xmin: float, xmax: float, x: float
) -> float:
    if x < xmin:
        return ymin
    elif x > xmax:
        return ymax
    y = ymax * ((x - xmin) / (xmax - xmin)) + ymin * ((xmax - x) / (xmax - xmin))
    return y


def CheckPaddleCollisionWithEdge(Paddle):
    if Paddle.coor.y + Paddle.dir <= 0:
        Paddle.dir = -Paddle.coor.y
    elif Paddle.coor.y + Paddle.size.y + Paddle.dir >= 100:
        Paddle.dir = 100 - Paddle.size.y - Paddle.coor.y


def CheckBallCollisionWithEdge(Ball):
    if Ball.coor.y + Ball.dir.y <= 2:
        newDir = (Ball.coor.y - 2) / -Ball.dir.y
        Ball.dir.x *= newDir
        Ball.dir.y *= newDir
        Ball.angle = 360 - Ball.angle
    elif Ball.coor.y + Ball.size.y + Ball.dir.y >= 98:
        newDir = (98 - Ball.coor.y - Ball.size.y) / Ball.dir.y
        Ball.dir.x *= newDir
        Ball.dir.y *= newDir
        Ball.angle = 360 - Ball.angle


def CheckBallCollisionWithPaddle(Ball, Paddle, Score):
    if Ball.coor.x < 100 / 2 and Paddle.coor.x < 100 / 2:
        if Ball.coor.x + Ball.dir.x < Paddle.coor.x + Paddle.size.x:
            if (
                Ball.coor.y + Ball.size.y + Ball.dir.y >= Paddle.coor.y + Paddle.dir
                and Ball.coor.y + Ball.dir.y
                <= Paddle.coor.y + Paddle.dir + Paddle.size.y
            ):
                hitZone = (Ball.coor.y + Ball.dir.y + (Ball.size.y / 2)) - (
                    Paddle.coor.y + Paddle.dir + (Paddle.size.y / 2)
                )
                # Ball.angle = 90 + (hitZone - 0.5) * 120
                Ball.angle = AngleInterpolation(
                    -45, 45, -Paddle.size.y / 2.0, Paddle.size.y / 2.0, hitZone
                )
                # Ball.angle = 180 - Ball.angle
                newDir = (Paddle.coor.x + Paddle.size.x - Ball.coor.x) / Ball.dir.x
                Ball.dir.x *= newDir
                Ball.dir.y *= newDir
                Ball.vel += 0.166666666666666666666666666666666
            else:
                Ball.reset()
                Score += 1
    if Ball.coor.x > 100 / 2 and Paddle.coor.x > 100 / 2:
        if Ball.coor.x + Ball.size.x + Ball.dir.x > Paddle.coor.x:
            if (
                Ball.coor.y + Ball.size.y + Ball.dir.y >= Paddle.coor.y + Paddle.dir
                and Ball.coor.y + Ball.dir.y
                <= Paddle.coor.y + Paddle.dir + Paddle.size.y
            ):
                hitZone = (Ball.coor.y + Ball.dir.y + (Ball.size.y / 2)) - (
                    Paddle.coor.y + Paddle.dir + (Paddle.size.y / 2)
                )
                # Ball.angle = 90 + (hitZone - 0.5) * 120
                Ball.angle = AngleInterpolation(
                    225, 135, -Paddle.size.y / 2.0, Paddle.size.y / 2.0, hitZone
                )
                # Ball.angle = 180 - Ball.angle
                # c'est debile
                newDir = (Paddle.coor.x + Paddle.size.x - Ball.coor.x) / Ball.dir.x
                newDir = (Paddle.coor.x - Ball.coor.x - Ball.size.x) / Ball.dir.x
                Ball.dir.x *= newDir
                Ball.dir.y *= newDir
                Ball.vel += 0.166666666666666666666666666666666
            else:
                Ball.reset()
                Score += 1
    return Score


def gameUpdate(PaddleL, PaddleR, Ball, ScoreL, ScoreR):
    PaddleL.update()
    PaddleR.update()
    Ball.update()
    PaddleL.update_ai(Ball)
    PaddleR.update_ai(Ball)
    Ball.update_dir()
    CheckPaddleCollisionWithEdge(PaddleL)
    CheckPaddleCollisionWithEdge(PaddleR)
    CheckBallCollisionWithEdge(Ball)
    ScoreR = CheckBallCollisionWithPaddle(Ball, PaddleL, ScoreR)
    ScoreL = CheckBallCollisionWithPaddle(Ball, PaddleR, ScoreL)
    return PaddleL, PaddleR, Ball, ScoreL, ScoreR
