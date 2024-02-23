import pygame


class Splash:
    def __init__(self, frame, window):
        coefficient = frame.get_width() / 3840
        big_font = pygame.font.Font("../data/media/fonts/AmaticSC-Bold.ttf", int(1100 * coefficient))
        fan = big_font.render("FAN", 1, "white")
        x, y = frame.get_width() * 0.5 - fan.get_width() * 0.5, frame.get_height() * 0.5 - fan.get_height() * 0.5
        frame.blit(fan, (x, y))
        small_font = pygame.font.Font("../data/media/fonts/AmaticSC-Bold.ttf", int(120 * coefficient))
        loading = small_font.render("Loading...", 1, pygame.Color(117, 87, 82))
        by = small_font.render("by @ bashinvolved", 1, pygame.Color(117, 87, 82))
        beta = small_font.render("BETA", 1, "white")
        frame.blit(beta, (x, y))
        frame.blit(loading, (x + fan.get_width() - loading.get_width(), y + fan.get_height()))
        frame.blit(by, (frame.get_width() - by.get_width(), frame.get_height() - by.get_height()))
        window.blit(frame,
                    (window.get_width() * 0.5 - frame.get_width() * 0.5, window.get_height() * 0.5 - frame.get_height() * 0.5))
        pygame.display.flip()
