from screeninfo import get_monitors


def get_second_screen_info():
    for m in get_monitors():
        if not m.is_primary:
            return m.width, m.height, m.x, m.y
