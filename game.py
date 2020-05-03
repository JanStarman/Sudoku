import pygame, os
import time
from tkinter import *
from tkinter import messagebox
from grid import Grid
from button import Button

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.font.init()
screen = pygame.display.set_mode((540, 600))
pygame.display.set_caption("Sudoku")

window = Tk()
window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
window.withdraw()


def redraw_game(board, play_time, check_button, check_all_button, solve_button):
    screen.fill((255, 255, 255))
    # Draw grid and board
    board.draw(screen)

    # Draw time
    font = pygame.font.SysFont(None, 40)
    text = font.render("Time: " + format_time(play_time), 1, (0, 0, 0))
    screen.blit(text, (540 - 160, 560))

    # Draw check buttons
    for button in {check_button, check_all_button}:
        button.draw(screen, 30, (0, 0, 0))
        if button.is_over(pygame.mouse.get_pos()):
            button.colour = (0, 191, 255)
        else:
            button.colour = (0, 0, 255)

    # Draw solve button
    solve_button.draw(screen, 30, (0, 0, 0))
    if solve_button.is_over(pygame.mouse.get_pos()) or solve_button.toggled is True:
        solve_button.colour = (0, 255, 0)
    else:
        solve_button.colour = (34, 139, 34)


def format_time(secs):
    sec = secs % 60
    minute = secs//60
    formatted = " " + str(minute) + ":" + str(sec)
    return formatted


def draw_text(text, color, size, surface, x, y):
    font = pygame.font.SysFont(None, size)
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def game_menu():
    button_easy = Button((255, 255, 255), 170, 100, 200, 50, "Easy")
    button_medium = Button((255, 255, 255), 170, 200, 200, 50, "Medium")
    button_hard = Button((255, 255, 255), 170, 300, 200, 50, "Hard")
    button_help = Button((255, 255, 255), 170, 400, 100, 50, "Help")
    button_quit = Button((255, 255, 255), 270, 400, 100, 50, "Quit")

    while True:
        screen.fill((245, 245, 220))
        draw_text('Choose difficulty', (0, 0, 0), 40, screen, 150, 20)

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_easy.is_over(pos):
                    game(30)
                if button_medium.is_over(pos):
                    game(40)
                if button_hard.is_over(pos):
                    game(50)
                if button_help.is_over(pos):
                    game_help()
                if button_quit.is_over(pos):
                    pygame.quit()
                    sys.exit()

        for button in {button_easy, button_medium, button_hard, button_help, button_quit}:
            button.draw(screen, 35, (0, 0, 0))
            if button.is_over(pos):
                button.colour = (255, 255, 153)
            else:
                button.colour = (255, 255, 255)
        pygame.display.update()


def game(difficulty):
    board = Grid(9, 9, 540, 540, difficulty)
    board.solve()

    check_button = Button((0, 0, 255), 10, 557, 80, 30, 'Check')
    check_all_button = Button((0, 0, 255), 110, 557, 110, 30, 'Check All')
    solve_button = Button((0, 205, 0), 240, 557, 80, 30, 'Solve')

    key = None
    run = True
    start = time.time()
    while run:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if messagebox.askokcancel('Quit', 'Are you sure?') is True:
                    run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_ESCAPE:
                    if messagebox.askokcancel('Quit', 'Are you sure?') is True:
                        run = False

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        board.place(board.cubes[i][j].temp)
                        key = None

                        if board.is_finished():
                            if board.is_correct():
                                messagebox.showinfo('Win!',
                                                    'You succesfully finished sudoku in '
                                                    + format_time(play_time)
                                                    + '!')
                                run = False
                            else:
                                messagebox.showerror('Error', 'This is not a correct solution!')

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if check_button.is_over(pos):
                    board.check()

                if check_all_button.is_over(pos):
                    board.check_all()

                if solve_button.is_over(pos):
                    solve_button.toggle()
                    if solve_button.toggled is True:
                        board.show_solved()
                    else:
                        board.hide_solved()

                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key is not None:
            board.sketch(key)

        redraw_game(board, play_time, check_button, check_all_button, solve_button)
        pygame.display.update()


def game_help():
    button = Button((255, 255, 255), 400, 500, 100, 50, "Back")
    run = True
    while run:
        screen.fill((245, 245, 220))
        draw_text('Rules', (0, 0, 0), 50, screen, 70, 25)

        dot = pygame.Rect(30, 85, 5, 5)
        pygame.draw.rect(screen, (0, 0, 0), dot)
        draw_text('Each row, column, and square can contain', (0, 0, 0), 25, screen, 40, 80)
        draw_text('each number (typically 1 to 9) exactly once.', (0, 0, 0), 25, screen, 70, 105)

        dot2 = pygame.Rect(30, 155, 5, 5)
        pygame.draw.rect(screen, (0, 0, 0), dot2)
        draw_text('The sum of all numbers in any nonet, row,', (0, 0, 0), 25, screen, 40, 150)
        draw_text('or column must match the small number printed in its', (0, 0, 0), 25, screen, 70, 175)
        draw_text('corner. For traditional Sudoku puzzles featuring', (0, 0, 0), 25, screen, 70, 200)
        draw_text('the numbers 1 to 9, this sum is equal to 45.', (0, 0, 0), 25, screen, 70, 225)

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.is_over(pos):
                    run = False

        button.draw(screen, 35, (0, 0, 0))
        if button.is_over(pos):
            button.colour = (255, 255, 153)
        else:
            button.colour = (255, 255, 255)
        pygame.display.update()


game_menu()
