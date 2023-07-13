from PIL import Image

def table_to_csv(table):
    result = ''
    for y, line in enumerate(table):
        for x, elt in enumerate(line):
            result += str(elt) + ','

        result += '\n'
    return result

def table_to_ansi(table):
    red    = "\u001b[48;5;9m\u001b[38;5;15m"
    yellow = "\u001b[48;5;3m\u001b[38;5;0m"
    green  = "\u001b[48;5;10m\u001b[38;5;0m"
    green2 = "\u001b[48;5;2m\u001b[38;5;0m"
    end    = "\u001b[0m"

    upper = max(max(line) for line in table[1:])
    size = len(str(upper)) + 2

    result = ''
    for y, line in enumerate(table):
        for x, elt in enumerate(line):
            if elt == 0 or (x, y) == (0, 0):
                result += green
            elif abs(elt) == 2:
                result += green2
            elif abs(elt) == upper:
                result += red
            else:
                result += yellow
            result += str(elt).rjust(size)
            result += end
        result += '\n'
    return result

def table_to_png(table):
    red    = (255, 0, 0),
    green  = (0, 255, 0),
    green2 = (22, 222, 22),
    yellow = (255, 255, 0),

    #upper = max(max(line) for line in table[1:])
    upper = table[0][0]
    size = len(str(upper)) + 2

    width = len(table[0])
    height = len(table)

    image = Image.new("RGB", (width, height))

    for y, line in enumerate(table):
        for x, elt in enumerate(line):
            if elt == 0 or (x, y) == (0, 0):
                color = green
            elif abs(elt) == 2:
                color = green2
            elif abs(elt) == upper:
                color = red
            else:
                ratio = 1 - (abs(elt) - 4) / (upper - 4)
                color = (255, int(255*ratio), 0)
            image.putpixel((x, y), color)

    return image

def print_table(table, format='ansi', filename='stdout'):
    if format == 'ansi':
        output = table_to_ansi(table)
    elif format == 'csv':
        output = table_to_csv(table)
    elif format == 'png':
        output = table_to_png(table)

    if filename == 'stdout':
        if format == 'png':
            print(output.tobytes().hex())
        else:
            print(output)
    elif format == 'png':
        output.save(filename, "png")
    else:
        with open(filename, 'w') as file:
            file.write(output)

def to_polynomial(x, variable='x'):
    polynomial = []
    i = 0
    while x > 0:
        if x % 2 == 1:
            polynomial.append(f'{variable}{i}')
        x //= 2
        i += 1
    polynomial.reverse()

    return " ⊕ ".join(polynomial)
