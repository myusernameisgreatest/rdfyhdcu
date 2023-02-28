import pygame
from Player import Player
from Levels import Level_01_bonuses, Level_01


# Переменные для установки ширины и высоты окна
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
bg = pygame.image.load('images/bg5.jpg')


# Основная функция прогарммы
def main():
	# Инициализация
	pygame.init()

	# Установка высоты и ширины
	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size, flags=pygame.NOFRAME)
	screen.fill((114, 157, 224))

	# Название игры
	pygame.display.set_caption("Cyberpunk 2078")
	icon = pygame.image.load('images/icon1.png')
	pygame.display.set_icon(icon)

	# Создаем игрока
	player = Player()

	# Создаем все уровни
	level_list = []
	level_list.append(Level_01(player))
	level_bonus_list = []
	level_bonus_list.append(Level_01_bonuses(player))

	# Устанавливаем текущий уровень
	current_level_no = 0
	current_level = level_list[current_level_no]
	current_level_bonus = level_bonus_list[current_level_no]

	active_sprite_list = pygame.sprite.Group()
	player.level = current_level
	player.level_bonus = current_level_bonus

	player.rect.x = 340
	player.rect.y = SCREEN_HEIGHT - player.rect.height
	active_sprite_list.add(player)

	# Цикл будет до тех пор, пока пользователь не нажмет кнопку закрытия
	done = False

	# Используется для управления скоростью обновления экрана
	clock = pygame.time.Clock()

	# Основной цикл программы
	while not done:
		# Отслеживание действий
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # Если закрыл программу, то останавливаем цикл
				done = True

			# Если нажали на стрелки клавиатуры, то двигаем объект
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player.go_left()
				if event.key == pygame.K_RIGHT:
					player.go_right()
				if event.key == pygame.K_UP:
					player.jump()
				if event.key == pygame.K_ESCAPE:
					done = True

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and player.change_x < 0:
					player.stop()
				if event.key == pygame.K_RIGHT and player.change_x > 0:
					player.stop()

		# Обновляем игрока
		active_sprite_list.update()

		# Обновляем объекты на сцене
		current_level.update()
		current_level_bonus.update()

		# Если игрок приблизится к правой стороне, то дальше его не двигаем
		if player.rect.right > SCREEN_WIDTH:
			player.rect.right = SCREEN_WIDTH

		# Если игрок приблизится к левой стороне, то дальше его не двигаем
		if player.rect.left < 0:
			player.rect.left = 0

		# Рисуем объекты на окне
		screen.blit(bg, (0, 0))
		current_level.draw(screen)
		current_level_bonus.draw(screen)
		active_sprite_list.draw(screen)
		myfont = pygame.font.Font('ClimateCrisis-Regular.ttf', 14)
		text_surface = myfont.render('«Wake the fuck up, Samurai! We have a city to burn.', True, 'Red')
		screen.blit(text_surface,(50, 50))

		# Устанавливаем количество фреймов
		clock.tick(30)

		# Обновляем экран после рисования объектов
		pygame.display.flip()

	# Корректное закрытие программы
	pygame.quit()


main()