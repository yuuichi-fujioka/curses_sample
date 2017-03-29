import curses
import itertools


stdscr = None
_input = None


def _fill(text, length, c=' '):
    return text + c * (length - len(text))


class Input(object):
    def __init__(self):
        self._handlers = []

    def regist_handler(self, h):
        self._handlers.append(h)

    def on_frame(self):
        c = stdscr.getch()
        if c in (10, 13):
            c = curses.KEY_ENTER
        return any(itertools.imap(lambda h: h.handle(c), self._handlers))

    def getc(self):
        return self._c


class Menu(object):
    def __init__(self):
        self._items = [
            'nova',
            'glance',
            'cinder',
            'keystone',
            'neutron',
        ]
        self._selected = 0
        self._has_forcus = True

    def draw(self, win, x, y):
        i = 0
        for item in self._items:
            flags = curses.color_pair(1)
            if i == self._selected:
                flags |= curses.A_UNDERLINE | curses.A_BOLD
            win.addstr(y + i, x, _fill(item, 40),  flags)
            i += 1

    def handle(self, c):
        if not self._has_forcus:
            return

        refresh = False
        if c == curses.KEY_UP:
            self._selected -= 1
            refresh = True
        elif c == curses.KEY_DOWN:
            self._selected += 1
            refresh = True
        MAX_INDEX = len(self._items) - 1
        if self._selected < 0:
            self._selected = MAX_INDEX
        elif self._selected > MAX_INDEX:
            self._selected = 0
        return refresh


def refresh_screen(win, menu):
    height, width = stdscr.getmaxyx()

    win.erase()
    win.border(0)
    menu.draw(win, 1, 1)

    win.refresh()


def gui_main():
    stdscr.border(0)
    stdscr.refresh()

    win = curses.newwin(22, 42, 1, 1)
    menu = Menu()
    _input.regist_handler(menu)

    refresh_screen(win, menu)
    while 1:
        refresh = _input.on_frame()
        if refresh:
            refresh_screen(win, menu)


def main():
    global stdscr
    global _input
    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()     # no key echo
    curses.cbreak()     # don't wait enter
    stdscr.keypad(1)    # special key input
    curses.curs_set(0)  # cursor invisible

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLUE)

    _input = Input()
    try:
        gui_main()
    finally:
        curses.echo()
        curses.nocbreak()
        stdscr.keypad(0)
        curses.endwin()


if __name__ == '__main__':
    main()
