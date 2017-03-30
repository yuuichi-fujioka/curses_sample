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


class Forcus(object):
    def __init__(self):
        self._items = []

    def regist_item(self, item):
        self._items.append(item)

    def handle(self, c):
        if c != ord('\t'):
            return
        prev_has_forcus = False
        for i in self._items:
            if prev_has_forcus:
                i._has_forcus = True
                return True

            if i._has_forcus:
                prev_has_forcus = True
                i._has_forcus = False


        self._items[0]._has_forcus = True
        return True

class Menu(object):
    def __init__(self, pos, items, width=40):
        self._items = items
        self._selected = 0
        self._has_forcus = False
        self._win = curses.newwin(len(items) + 2, width + 2, *pos)

    def draw(self, stdscr):
        self._win.erase()
        self._win.border(0)
        y, x = 1, 1
        i = 0
        for item in self._items:
            flags = curses.color_pair(1)
            if i == self._selected:
                flags |= curses.A_BOLD
                if self._has_forcus:
                    flags |= curses.A_REVERSE
                else:
                    flags |= curses.A_UNDERLINE
            self._win.addstr(y + i, x, _fill(item, 40),  flags)
            i += 1
        self._win.refresh()

    def handle(self, c):
        if not self._has_forcus:
            return

        refresh = False
        if c in (curses.KEY_UP, ord('k')):
            self._selected -= 1
            refresh = True
        elif c in (curses.KEY_DOWN, ord('j')):
            self._selected += 1
            refresh = True
        MAX_INDEX = len(self._items) - 1
        if self._selected < 0:
            self._selected = MAX_INDEX
        elif self._selected > MAX_INDEX:
            self._selected = 0
        return refresh


def refresh_screen(objects):
    height, width = stdscr.getmaxyx()

    for o in objects:
        o.draw(stdscr)


def gui_main():
    stdscr.border(0)
    stdscr.refresh()

    forcus = Forcus()
    menu = Menu(
        (1,1),
        ['nova', 'keystone', 'glance', 'cinder', 'neutron'],
        40)
    menu._has_forcus = True
    menu2 = Menu(
        (1,43),
        ['heat', 'swift', 'horizon', 'murano', 'tacker', 'ceilometer'])

    _input.regist_handler(menu)
    _input.regist_handler(menu2)
    _input.regist_handler(forcus)
    forcus.regist_item(menu)
    forcus.regist_item(menu2)

    refresh_screen((menu,menu2))
    while 1:
        refresh = _input.on_frame()
        if refresh:
            refresh_screen((menu,menu2))


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
