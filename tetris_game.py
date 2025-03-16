import pygame
import random

# Configurações do jogo
WIDTH = 300
HEIGHT = 600
BLOCK_SIZE = 30
FPS = 60

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Formas dos tetrominós
SHAPES = [
    [[1, 1, 1, 1]],         # I
    [[1, 1], [1, 1]],       # Quadrado
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1, 0], [0, 1, 1]], # Z
    [[0, 1, 1], [1, 1, 0]], # S
    [[1, 1, 1], [1, 0, 0]], # L
    [[1, 1, 1], [0, 0, 1]]  # L invertido
]

COLORS = [CYAN, YELLOW, PURPLE, ORANGE, BLUE, GREEN, RED]

class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = (WIDTH // BLOCK_SIZE) // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        rotated = [list(row) for row in zip(*self.shape[::-1])]
        self.shape = rotated

    def move(self, dx):
        self.x += dx

    def draw(self, screen):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color,
                                     ((self.x + x) * BLOCK_SIZE, (self.y + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = {}

    def is_valid_position(self, piece):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    px = piece.x + x
                    py = piece.y + y
                    if px < 0 or px >= self.width // BLOCK_SIZE or py >= self.height // BLOCK_SIZE:
                        return False
                    if (px, py) in self.grid:
                        return False
        return True

    def fix_piece(self, piece):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    px = piece.x + x
                    py = piece.y + y
                    self.grid[(px, py)] = piece.color

    def clear_lines(self):
        rows = self.height // BLOCK_SIZE
        cols = self.width // BLOCK_SIZE
        full_rows = []

        for y in range(rows):
            if all((x, y) in self.grid for x in range(cols)):
                full_rows.append(y)

        if full_rows:
            for y in full_rows:
                for x in range(cols):
                    if (x,y) in self.grid:
                        del self.grid[(x, y)]

            new_grid = {}
            for (x, y), color in self.grid.items():
                shift = sum(1 for row in full_rows if y > row)
                new_grid[(x, y + shift)] = color

            self.grid = new_grid

        # Retorna o numero de linhas limpas.
        return len(full_rows)

    def draw(self, screen):
        for y in range(self.height // BLOCK_SIZE):
            for x in range(self.width // BLOCK_SIZE):
                pygame.draw.rect(screen, WHITE,
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        for (x, y), color in self.grid.items():
            pygame.draw.rect(screen, color,
                             (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.running = True

        self.grid = Grid(WIDTH, HEIGHT)
        self.current_piece = self.new_piece()

        self.fall_time = 0
        self.fall_speed = 300
        self.score = 0 # Adicionado: Inicializar a pontuação
        self.font = pygame.font.SysFont('Arial', 30) # Adicionado: Fonte para a pontuação

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return Piece(shape, color)

    def run(self):
        while self.running:
            self.screen.fill(BLACK)
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(FPS)

        self.save_score(self.score) # Passar a pontuação como argumento

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.current_piece.move(-1)
                    if not self.grid.is_valid_position(self.current_piece):
                        self.current_piece.move(1)
                elif event.key == pygame.K_RIGHT:
                    self.current_piece.move(1)
                    if not self.grid.is_valid_position(self.current_piece):
                        self.current_piece.move(-1)
                elif event.key == pygame.K_DOWN:
                    self.current_piece.y += 1
                    if not self.grid.is_valid_position(self.current_piece):
                        self.current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    self.current_piece.rotate()
                    if not self.grid.is_valid_position(self.current_piece):
                        for _ in range(3):
                            self.current_piece.rotate()

    def update(self):
        self.fall_time += self.clock.get_rawtime()

        if self.fall_time > self.fall_speed:
            self.current_piece.y += 1
            if not self.grid.is_valid_position(self.current_piece):
                self.current_piece.y -= 1
                self.grid.fix_piece(self.current_piece)
                lines_cleared = self.grid.clear_lines()
                self.score += lines_cleared * 100 # Adicionado: Calcular a pontuação
                self.current_piece = self.new_piece()
                if not self.grid.is_valid_position(self.current_piece):
                    self.running = False
            self.fall_time = 0

    def draw(self):
        self.grid.draw(self.screen)
        self.current_piece.draw(self.screen)
        score_text = self.font.render(f'Score: {self.score}', True, WHITE) # Adicionado: Renderizar a pontuação
        self.screen.blit(score_text, (10, 10)) # Adicionado: Exibir a pontuação

if __name__ == "__main__":
    game = Tetris()
    game.run()