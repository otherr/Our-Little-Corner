import pygame
from settings import *
from timer import Timer

class Menu:
	def __init__(self, player, toggle_menu):

		# General setup
		self.player = player
		self.toggle_menu = toggle_menu
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)

		# Options - Replace with affirmations
		self.width = 600  # Adjust width for longer text
		self.space = 15
		self.padding = 12

		# Loving words instead of merchant options
		self.options = [
			"We're so proud of you!",
			"You are loved more than you know.",
			"You make the world brighter!",
			"I love you so much!",
			"You are so strong my love.",
			"Your love is a gift <3."
		]
		self.setup()

		# Movement
		self.index = 0
		self.timer = Timer(200)

	def setup(self):
		"""Prepare text surfaces for rendering"""
		self.text_surfs = []
		self.total_height = 0

		for phrase in self.options:
			text_surf = self.font.render(phrase, False, 'Black')
			self.text_surfs.append(text_surf)
			self.total_height += text_surf.get_height() + (self.padding * 2)

		self.total_height += (len(self.text_surfs) - 1) * self.space
		self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
		self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2, self.menu_top, self.width, self.total_height)

	def input(self):
		"""Handles player input for menu navigation"""
		keys = pygame.key.get_pressed()
		self.timer.update()

		if keys[pygame.K_ESCAPE]:  # Close menu
			self.toggle_menu()

		if not self.timer.active:
			if keys[pygame.K_UP]:
				self.index = (self.index - 1) % len(self.options)
				self.timer.activate()
			elif keys[pygame.K_DOWN]:
				self.index = (self.index + 1) % len(self.options)
				self.timer.activate()

	def show_entry(self, text_surf, top, selected):
		"""Display loving words"""
		# Background
		bg_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + (self.padding * 2))
		pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)

		# Text
		text_rect = text_surf.get_rect(center=(self.main_rect.centerx, bg_rect.centery))
		self.display_surface.blit(text_surf, text_rect)

		# Highlight selection
		if selected:
			pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)

	def update(self):
		"""Update menu display"""
		self.input()

		for text_index, text_surf in enumerate(self.text_surfs):
			top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
			self.show_entry(text_surf, top, self.index == text_index)
