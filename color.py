def colored(cr, cg, cb):
    return "\033[38;2;{};{};{}m".format(cr, cg, cb)


red = colored(220, 45, 35)
green = colored(45, 145, 30)
blue = colored(30, 100, 180)
reset = colored(200, 200, 200)


def r(msg):
    return f"{red}{msg}{reset}"


def g(msg):
    return f"{green}{msg}{reset}"


def b(msg):
    return f"{blue}{msg}{reset}"
