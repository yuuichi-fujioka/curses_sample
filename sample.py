import curses
import json


stdscr = None

def refresh_screen(win, x, y):
    height, width = stdscr.getmaxyx()
    stdscr.erase()
    stdscr.addstr(height - 1, 0, "%d:%d"%(x,y), curses.A_REVERSE)
    stdscr.refresh()

    win.erase()
    win.border(0)
    win.addstr(y + 1, x + 1, "B", curses.color_pair(1))
    win.refresh()


def gui_main():
    stdscr.refresh()

    win = curses.newwin(22, 42, 1, 1)

    # stdscr.addstr(0, 0, "Current mode: Typing mode", curses.A_REVERSE)
    x = 0
    y = 0
    refresh_screen(win, x, y)
    while 1:
        c = stdscr.getch()
        refresh = False
        if c == curses.KEY_ENTER:
            return
        elif c == curses.KEY_LEFT:
            if x > 0:
                x -= 1
                refresh = True
        elif c == curses.KEY_RIGHT:
            if x < 40 - 1:
                x += 1
                refresh = True
        elif c == curses.KEY_UP:
            if y > 0:
                y -= 1
                refresh = True
        elif c == curses.KEY_DOWN:
            if y < 20 - 1:
                y += 1
                refresh = True
        if refresh:
            refresh_screen(win, x, y)


def main():
    global stdscr
    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()  # no key echo
    curses.cbreak()  # don't wait enter
    stdscr.keypad(1) # special key input
    curses.curs_set(0)  # cursor invisible

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLUE)

    try:
        gui_main()
    finally:
        curses.echo()
        curses.nocbreak()
        stdscr.keypad(0)
        curses.endwin()


if __name__ == '__main__':
    main()


