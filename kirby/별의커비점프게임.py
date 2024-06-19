import sys
import pygame
import random

# 게임 화면 크기
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 색상
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 139)
LIGHT_YELLOW = (255, 255, 224)
PASTEL_BROWN = (205, 133, 63)
PASTEL_DARK_GREEN = (60, 179, 113)
BLACK = (0, 0, 0)
APPLE_RED = (255, 102, 102)
PASTEL_PINK = (255, 182, 193)
PASTEL_BLUE = (173, 216, 230)
PASTEL_GREEN = (152, 251, 152)
PASTEL_YELLOW = (255, 247, 153)
PASTEL_ORANGE = (255, 228, 181)
PASTEL_PURPLE = (216, 191, 216)
PASTEL_SKY_BLUE = (176, 224, 230)
PASTEL_RED = (255, 105, 97)

# 속도와 질량 기본 값
VELOCITY = 7
MASS = 2


class Kirby:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.rect = pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 140, 40, 40)
        self.isJump = 0
        self.v = VELOCITY  # 속도
        self.m = MASS  # 질량

    # Kirby를 스크린에 그리기
    def draw_kirby(self):
        # 몸통
        pygame.draw.circle(SCREEN, PASTEL_PINK, (self.rect.x + 20, self.rect.y + 20), 20)
        # 왼쪽 눈
        pygame.draw.ellipse(SCREEN, BLACK, [self.rect.x + 8, self.rect.y + 10, 6, 12])
        pygame.draw.ellipse(SCREEN, PASTEL_BLUE, [self.rect.x + 9, self.rect.y + 12, 3, 6])
        # 오른쪽 눈
        pygame.draw.ellipse(SCREEN, BLACK, [self.rect.x + 26, self.rect.y + 10, 6, 12])
        pygame.draw.ellipse(SCREEN, PASTEL_BLUE, [self.rect.x + 27, self.rect.y + 12, 3, 6])
        # 볼
        pygame.draw.circle(SCREEN, PASTEL_RED, (self.rect.x + 10, self.rect.y + 28), 3)
        pygame.draw.circle(SCREEN, PASTEL_RED, (self.rect.x + 30, self.rect.y + 28), 3)
        # 입
        pygame.draw.arc(SCREEN, BLACK, [self.rect.x + 12, self.rect.y + 22, 16, 10], 3.14, 2 * 3.14)
        # 손
        pygame.draw.ellipse(SCREEN, PASTEL_PINK, [self.rect.x - 10, self.rect.y + 15, 10, 15])  # 왼쪽 손
        pygame.draw.ellipse(SCREEN, PASTEL_PINK, [self.rect.x + 40, self.rect.y + 15, 10, 15])  # 오른쪽 손
        # 발
        pygame.draw.ellipse(SCREEN, PASTEL_RED, [self.rect.x + 5, self.rect.y + 30, 15, 10])  # 왼쪽 발
        pygame.draw.ellipse(SCREEN, PASTEL_RED, [self.rect.x + 20, self.rect.y + 30, 15, 10])  # 오른쪽 발

    # x 좌표 이동 : Kirby의 움직임 제어할 때 필요
    def move_x(self):
        self.rect.x += self.dx

    # 화면 밖으로 못 나가게 방지
    def check_screen(self):
        if self.rect.bottom > WINDOW_HEIGHT or self.rect.y < 0:
            self.rect.y -= self.dy

    def jump(self, j):
        self.isJump = j

    def update(self, platforms):
        if self.isJump > 0:
            if self.isJump == 2:
                self.v = VELOCITY

            # 역학공식 계산 (F). F = 0.5 * mass * velocity^2.
            if self.v > 0:
                # 속도가 0보다 클때는 위로 올라감
                F = (0.5 * self.m * (self.v * self.v))
            else:
                # 속도가 0보다 작을때는 아래로 내려감
                F = -(0.5 * self.m * (self.v * self.v))

            # 좌표 수정 : 위로 올라가기 위해서 y 좌표를 줄여줌
            self.rect.y -= round(F)

            # 속도 줄여줌
            self.v -= 1

            # 바닥에 닿았을 때, 변수 리셋
            if self.rect.bottom > WINDOW_HEIGHT - 100:
                self.rect.bottom = WINDOW_HEIGHT - 100
                self.isJump = 0
                self.v = VELOCITY

        # 플랫폼과의 충돌 확인
        on_platform = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.v < 0:  # 커비가 위로 올라가는 중일 때만
                    self.rect.y = platform.rect.top - self.rect.height
                    on_platform = True  # 플랫폼 위에 있는 상태로 설정

        # 어느 플랫폼에도 닿지 않았을 경우, 공중에 떠있는 상태로 설정
        if not on_platform:
            self.isJump = 1  # 일단 공중에 떠 있는 상태로 설정


class Background:
    def __init__(self):
        self.time = 0
        self.is_day = True  # 낮인지 밤인지 여부를 나타내는 변수 추가

    def update(self):
        self.time += 1
        if self.time >= 1200:
            self.time = 0
            self.is_day = not self.is_day  # 낮 밤 전환

    def draw_star(self, x, y, size):
        points = [
            (x, y - size),
            (x + size * 0.38, y - size * 0.38),
            (x + size, y - size * 0.38),
            (x + size * 0.62, y),
            (x + size * 0.82, y + size * 0.62),
            (x, y + size * 0.24),
            (x - size * 0.82, y + size * 0.62),
            (x - size * 0.62, y),
            (x - size, y - size * 0.38),
            (x - size * 0.38, y - size * 0.38),
        ]
        pygame.draw.polygon(SCREEN, PASTEL_YELLOW, points)

    def draw_sun(self, x, y, radius):
        # 태양의 원형 부분
        pygame.draw.circle(SCREEN, PASTEL_YELLOW, (x, y), radius)

        # 태양의 빛 부분
        for i in range(13):
            angle = i * (360 / 13)
            length = radius + 20
            width = 50  # 빛의 두께
            end_x = x + length * pygame.math.Vector2(1, 0).rotate(angle).x
            end_y = y + length * pygame.math.Vector2(1, 0).rotate(angle).y
            points = [(x, y),
                      (x + width * pygame.math.Vector2(1, 0).rotate(angle + 10).x,
                       y + width * pygame.math.Vector2(1, 0).rotate(angle + 10).y),
                      (end_x, end_y),
                      (x + width * pygame.math.Vector2(1, 0).rotate(angle - 10).x,
                       y + width * pygame.math.Vector2(1, 0).rotate(angle - 10).y)]
            pygame.draw.polygon(SCREEN, PASTEL_YELLOW, points)

    def draw_crescent_moon(self, x, y, radius):
        # 큰 원으로 기본 모양 그리기
        pygame.draw.circle(SCREEN, LIGHT_YELLOW, (x, y), radius)

        # 작은 원으로 초승달 모양 만들기
        pygame.draw.circle(SCREEN, DARK_BLUE, (x + radius // 2, y), radius)

    def draw_tree(self, x, y):
        pygame.draw.rect(SCREEN, PASTEL_BROWN, (x, y, 20, 50))
        pygame.draw.circle(SCREEN, PASTEL_DARK_GREEN, (x + 10, y - 10), 20)
        pygame.draw.circle(SCREEN, PASTEL_DARK_GREEN, (x - 10, y - 20), 20)
        pygame.draw.circle(SCREEN, PASTEL_DARK_GREEN, (x + 30, y - 20), 20)
        pygame.draw.circle(SCREEN, PASTEL_DARK_GREEN, (x + 10, y - 30), 20)

    def draw_flower(self, x, y):
        # 꽃잎 그리기
        pygame.draw.circle(SCREEN, PASTEL_RED, (x, y), 7)
        pygame.draw.circle(SCREEN, PASTEL_RED, (x + 14, y), 7)
        pygame.draw.circle(SCREEN, PASTEL_RED, (x, y + 14), 7)
        pygame.draw.circle(SCREEN, PASTEL_RED, (x + 14, y + 14), 7)
        pygame.draw.circle(SCREEN, PASTEL_YELLOW, (x + 7, y + 7), 7)

        # 줄기 그리기
        pygame.draw.rect(SCREEN, PASTEL_DARK_GREEN, (x + 6, y + 14, 2, 15))

    def draw(self):
        if self.is_day:
            SCREEN.fill(PASTEL_SKY_BLUE)
            self.draw_sun(700, 100, 50)  # 해
            pygame.draw.rect(SCREEN, PASTEL_GREEN, (0, WINDOW_HEIGHT - 100, WINDOW_WIDTH, 100))  # 잔디

            # 꽃 그리기
            self.draw_flower(200, WINDOW_HEIGHT - 130)
            self.draw_flower(300, WINDOW_HEIGHT - 130)
            self.draw_flower(400, WINDOW_HEIGHT - 130)
            self.draw_flower(600, WINDOW_HEIGHT - 130)

        else:
            SCREEN.fill(DARK_BLUE)
            self.draw_crescent_moon(700, 100, 50)

            for _ in range(20):  # 별 크기 다양하게
                x = random.randint(0, WINDOW_WIDTH)
                y = random.randint(0, WINDOW_HEIGHT // 2)
                size = random.randint(5, 10)
                self.draw_star(x, y, size)
            pygame.draw.rect(SCREEN, PASTEL_PURPLE, (0, WINDOW_HEIGHT - 100, WINDOW_WIDTH, 100))

        self.draw_tree(100, WINDOW_HEIGHT - 150)
        self.draw_tree(400, WINDOW_HEIGHT - 150)


class Item:
    def __init__(self, x, y, type):
        self.type = type
        self.rect = pygame.Rect(x, y, 20, 20)

    def draw(self):
        if self.type == 'apple':
            pygame.draw.circle(SCREEN, APPLE_RED, (self.rect.x + 10, self.rect.y + 17), 10)  # 사과 위치 조정
            pygame.draw.rect(SCREEN, APPLE_RED, (self.rect.x + 8, self.rect.y + 10, 4, 6))  # 사과 줄기 위치 조정
        elif self.type == 'grape':
            self.draw_grape(self.rect.x, self.rect.y)

    def draw_grape(self, x, y):
        # 포도 송이를 그리는 함수
        grape_color = (138, 43, 226)  # 포도 색상
        # 포도알 위치 (8개의 포도알)
        positions = [
            (x + 10, y + 3),
            (x + 16, y + 9),
            (x + 4, y + 9),
            (x + 10, y + 15),
            (x + 20, y + 15),
            (x, y + 15),
            (x + 4, y + 21),
            (x + 16, y + 21)
        ]

        for pos in positions:
            pygame.draw.circle(SCREEN, grape_color, pos, 5)

        # 줄기 그리기
        pygame.draw.line(SCREEN, PASTEL_GREEN, (x + 10, y - 5), (x + 10, y + 3), 2)
        pygame.draw.line(SCREEN, PASTEL_GREEN, (x + 10, y + 18), (x + 10, y + 23), 2)
        pygame.draw.line(SCREEN, PASTEL_GREEN, (x + 5, y + 8), (x, y + 13), 2)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)


class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        # 기본 플랫폼 색상
        pygame.draw.rect(SCREEN, PASTEL_BROWN, self.rect)

        # 땅의 굴곡 표현을 위한 추가적인 디테일
        for i in range(self.rect.x, self.rect.x + self.rect.width, 10):
            pygame.draw.line(SCREEN, PASTEL_ORANGE, (i, self.rect.y), (i + 5, self.rect.y - 5), 2)
            pygame.draw.line(SCREEN, PASTEL_ORANGE, (i + 5, self.rect.y - 5), (i + 10, self.rect.y), 2)

        # 잔디 추가
        grass_height = 10
        grass_rect = pygame.Rect(self.rect.x, self.rect.y - grass_height, self.rect.width, grass_height)
        pygame.draw.rect(SCREEN, PASTEL_GREEN, grass_rect)

        # 잔디의 굴곡 표현
        for i in range(grass_rect.x, grass_rect.x + grass_rect.width, 5):
            pygame.draw.line(SCREEN, PASTEL_DARK_GREEN, (i, grass_rect.y), (i + 3, grass_rect.y - 3), 1)
            pygame.draw.line(SCREEN, PASTEL_DARK_GREEN, (i + 3, grass_rect.y - 3), (i + 6, grass_rect.y), 1)

def main():
    global SCREEN, WINDOW_WIDTH, WINDOW_HEIGHT

    # pygame 초기화 및 스크린 생성
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Kirby Game")

    clock = pygame.time.Clock()

    # Kirby 캐릭터 생성
    player = Kirby()

    # 배경 생성
    background = Background()

    # 아이템 생성
    items = [Item(random.randint(0, WINDOW_WIDTH - 20), random.randint(0, WINDOW_HEIGHT - 120), random.choice(['apple', 'grape'])) for _ in range(13)]

    # 공중 플랫폼 생성
    platforms = [Platform(random.randint(0, WINDOW_WIDTH - 100), random.randint(100, WINDOW_HEIGHT - 200), 100, 10) for _ in range(5)]

    playing = True

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.dx = 5
                elif event.key == pygame.K_LEFT:
                    player.dx = -5
                elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    if player.isJump == 0:
                        player.jump(1)
                    elif player.isJump == 1:
                        player.jump(2)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.dx = 0
                elif event.key == pygame.K_LEFT:
                    player.dx = 0

        # 배경 업데이트 및 그리기
        background.update()
        background.draw()

        # Kirby 업데이트 및 그리기
        player.move_x()
        player.update(platforms)
        player.draw_kirby()
        player.check_screen()

        # 아이템 그리기 및 충돌 확인
        for item in items[:]:
            item.draw()
            if item.check_collision(player.rect):
                items.remove(item)  # 충돌한 아이템 삭제

        # 플랫폼 그리기
        for platform in platforms:
            platform.draw()

        # 플랫폼과 Kirby 충돌 확인
        for platform in platforms:
            if player.rect.colliderect(platform.rect):
                player.rect.y = platform.rect.top - player.rect.height

        # 화면 업데이트
        pygame.display.update()

        # 프레임 설정
        clock.tick(30)

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
