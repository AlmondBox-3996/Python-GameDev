import pygame

pygame.init()
font20 = pygame.font.Font('freesansbold.ttf', 20)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock() 
FPS = 30

class Striker:
	def __init__(self, posx, posy, width, height, speed, color):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.speed = speed
		self.color = color
		self.playerRect = pygame.Rect(posx, posy, width, height)
		self.player = pygame.draw.rect(screen, self.color, self.playerRect)

	def display(self):
		self.player = pygame.draw.rect(screen, self.color, self.playerRect)

	def update(self, yFac):
		self.posy = self.posy + self.speed*yFac

		if self.posy <= 0:
			self.posy = 0

		elif self.posy + self.height >= HEIGHT:
			self.posy = HEIGHT-self.height

		self.playerRect = (self.posx, self.posy, self.width, self.height)

	def displayScore(self, text, score, x, y, color):
		text = font20.render(text+str(score), True, color)
		textRect = text.get_rect()
		textRect.center = (x, y)

		screen.blit(text, textRect)

	def getRect(self):
		return self.playerRect

class Ball:
	def __init__(self, posx, posy, radius, speed, color):
		self.posx = posx
		self.posy = posy
		self.radius = radius
		self.speed = speed
		self.color = color
		self.xFac = 1
		self.yFac = -1
		self.ball = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)
		self.firstTime = 1

	def display(self):
		self.ball = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)

	def update(self):
		self.posx += self.speed*self.xFac
		self.posy += self.speed*self.yFac

		if self.posy <= 0 or self.posy >= HEIGHT:
			self.yFac *= -1

		if self.posx <= 0 and self.firstTime:
			self.firstTime = 0
			return 1
		elif self.posx >= WIDTH and self.firstTime:
			self.firstTime = 0
			return -1
		else:
			return 0

	def reset(self):
		self.posx = WIDTH//2
		self.posy = HEIGHT//2
		self.xFac *= -1
		self.firstTime = 1

	def hit(self):
		self.xFac *= -1

	def getRect(self):
		return self.ball

def main():
	running = True

	player1 = Striker(20, 0, 10, 100, 10, GREEN)
	player2 = Striker(WIDTH-30, 0, 10, 100, 10, GREEN)
	ball = Ball(WIDTH//2, HEIGHT//2, 7, 7, WHITE)

	listOfplayers = [player1, player2]

	player1Score, player2Score = 0, 0
	player1YFac, player2YFac = 0, 0

	while running:
		screen.fill(BLACK)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					player2YFac = -1
				if event.key == pygame.K_DOWN:
					player2YFac = 1
				if event.key == pygame.K_w:
					player1YFac = -1
				if event.key == pygame.K_s:
					player1YFac = 1
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					player2YFac = 0
				if event.key == pygame.K_w or event.key == pygame.K_s:
					player1YFac = 0

		for player in listOfplayers:
			if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
				ball.hit()

		player1.update(player1YFac)
		player2.update(player2YFac)
		point = ball.update()

		if point == -1:
			player1Score += 1
		elif point == 1:
			player2Score += 1

		if point: 
			ball.reset()

		player1.display()
		player2.display()
		ball.display()

		player1.displayScore("PLAYER_1 : ", 
						player1Score, 100, 20, WHITE)
		player2.displayScore("PLAYER_2 : ", 
						player2Score, WIDTH-100, 20, WHITE)

		pygame.display.update()
		clock.tick(FPS)	 


if __name__ == "__main__":
	main()
	pygame.quit()
