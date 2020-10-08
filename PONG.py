import pygame


pygame.init()
screenHeight = 500
screenWidth = 800
screen = pygame.display.set_mode((screenWidth, screenHeight))  # screen size
pygame.display.set_caption("PONG!")  # game title
font = pygame.font.Font("ARCADECLASSIC.TTF", 82)  # pixel Font
clock = pygame.time.Clock()  # FPS clock
# loading missing the ball sound effect
BallMissedSound = pygame.mixer.Sound("ball missed.wav")
# loading hitting wall sound effect
wallHitSound = pygame.mixer.Sound("wall hit.wav")
# loading paddle hitting sound effect
paddleHitSound = pygame.mixer.Sound("paddel hit.wav")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class paddle(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = WHITE
        self.dy = 0.5
        self.score = 0

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y,
                                         self.width, self.height), 0)

    def move(self, dy):
        if self.y < 5:
            self.y = 5
        elif self.y > screenHeight - self.height - 5:
            self.y = screenHeight - self.height - 5

        self.dy = dy
        self.y += self.dy
        self.dy = 0

    def viewScore(self, screen, x, y):
        playerScore = font.render(str(self.score), 1, WHITE)
        screen.blit(playerScore, (x, y))


class ballSquare(object):
    def __init__(self, x, y, side):
        self.x = x
        self.y = y
        self.side = side
        self.color = WHITE
        self.dy = 0.1
        self.dx = 0.1

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y,
                                         self.side, self.side), 0)
        self.move()

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # reflecting the ball out of the floor and ceiling
        if self.y < 5 or self.y > screenHeight - self.side - 5:
            self.dy *= - 1
            wallHitSound.play()

        # ball hitiing p1 paddle
        if self.x + self.side >= p1.x and self.x + self.side < p1.x + p1.width and self.y > p1.y and self.y < p1.y + p1.height:
            self.speedUp()
            self.x = p1.x - p1.width
            self.dx *= - 1
            paddleHitSound.play()

        # ball hitiing p2 paddle
        if self.x >= p2.x and self.x <= p2.x + p2.width and self.y >= p2.y and self.y <= p2.y + p2.height:
            self.speedUp()
            self.x = p2.x + p2.width
            self.dx *= - 1
            paddleHitSound.play()

        # ball going out of the screen
        if self.x - self.side > screenWidth or self.x + self.side < 0:
            if self.x - self.side > screenWidth:
                p2.score += 1
            else:
                p1.score += 1
            self.dy = self.dy*abs(0.1/self.dy)
            self.dx = self.dx*abs(0.1/self.dx)
            BallMissedSound.play(0)

            # center of the screen
            self.x = screenWidth/2 - self.side / 2
            self.y = 245

    def speedUp(self):  # speeding up the ball if it hits one of the paddels
        if abs(self.dx) < 0.5:
            self.dx *= 1.08
        if abs(self.dy) < 0.5:
            self.dy *= 1.08


class button():  # button Object
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textColour = BLACK
        self.value = None

    def draw(self, win):
        # Call this method to draw the button on the screen
        pygame.draw.rect(win, self.color, (self.x, self.y,
                                           self.width, self.height), 0)

        text = font.render(self.text, 1, self.textColour)
        win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                        self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def pausedGameUpdate(screen):
    screen.fill(BLACK)
    QuitButton.draw(screen)
    playAgainButton.draw(screen)
    p1.viewScore(screen, 456, 31)
    p2.viewScore(screen, 300, 31)
    p1.draw(screen)
    p2.draw(screen)
    pygame.display.update()


def GameOnUpdate(screen):
    screen.fill(BLACK)

    pygame.draw.line(screen, WHITE, (screenWidth/2, 0),
                     (screenWidth/2, screenWidth), 2)

    ball.draw(screen)
    p1.viewScore(screen, 456, 20)
    p2.viewScore(screen, 300, 20)
    p1.draw(screen)
    p2.draw(screen)

    pygame.display.update()


# new Game
pause = False
QuitButton = button(WHITE, 310, 240, 180, 80, " QUIT")
QuitButton.value = False  # as the Quit Button is not clicked
playAgainButton = button(WHITE, 215, 146, 370, 70, "NEW GAME")
playAgainButton.value = True  # as the play again Button is already clicked
ball = ballSquare(screenWidth/2 - 7.5, 245, 15)
p1 = paddle(screenWidth-35, 215, 15, 100)
p2 = paddle(20, 215, 15, 100)
# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            if clickPos[0] > QuitButton.x and clickPos[1] > QuitButton.y and clickPos[0] < QuitButton.x + QuitButton.width and clickPos[1] < QuitButton.y + QuitButton.height:
                running = False
            if clickPos[0] > playAgainButton.x and clickPos[1] > playAgainButton.y and clickPos[0] < playAgainButton.x + playAgainButton.width and clickPos[1] < playAgainButton.y + playAgainButton.height:
                playAgainButton.value = True
                pause = False
                ball = ballSquare(screenWidth/2 - 7.5, 245, 15)
                p1 = paddle(screenWidth-35, 215, 15, 100)
                p2 = paddle(20, 215, 15, 100)
        if event.type == pygame.MOUSEMOTION and playAgainButton.value == False:
            hoverPos = pygame.mouse.get_pos()

            if QuitButton.isOver(hoverPos):
                QuitButton.color = BLACK
                QuitButton.textColour = WHITE
            else:
                QuitButton.color = WHITE
                QuitButton.textColour = BLACK

            if playAgainButton.isOver(hoverPos):
                playAgainButton.color = BLACK
                playAgainButton.textColour = WHITE
            else:
                playAgainButton.color = WHITE
                playAgainButton.textColour = BLACK

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause = not pause
    keys = pygame.key.get_pressed()  # list of all keys got pressed

    if keys[pygame.K_UP]:
        p1.move(-0.5)
    if keys[pygame.K_DOWN]:
        p1.move(0.5)
    if keys[pygame.K_w]:
        p2.move(-0.5)
    if keys[pygame.K_s]:
        p2.move(0.5)

    if pause == False:
        playAgainButton.value == True
        GameOnUpdate(screen)
    else:
        playAgainButton.value = False
        pausedGameUpdate(screen)

pygame.quit()
