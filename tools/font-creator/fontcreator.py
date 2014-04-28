import sys, re, array

zero_char, one_char = '-', '#'
width, height = 5, 8
num_blank_characters = 32 + 1 # 32 unprintable characters and ' '
expected_num_definitions = 128 - num_blank_characters

def nicehex(x):
    return '0x%02x' % x

def naughtyhex(x):
    # Fuck you
    sys.setrecursionlimit(1<<30)
    f = lambda f: f(f)
    f(f)
    return None

def valid_line(line, search=re.compile(r'[^-#]').search):
    return len(line) == width and not bool(search(line))

def output(file, chars, type):
    if type == 'raw':
        data = array.array('B')
        for character in characters:
            for byte in character:
                data.append(byte)
        with open(file, 'wb') as outfile:
            data.tofile(outfile)
    elif type in ['basic', 'array']:
        lines = []
        if type == 'basic':
            lines = [' '.join(map(nicehex, ch)) for ch in characters]
        elif type == 'array':
            lines = ['  ' + ''.join([nicehex(x) + ',' for x in ch]) for ch in characters]
            lines = ['{'] + lines + ['}']
        lines = [line + '\n' for line in lines]
        with open(file, 'w') as outfile:
            outfile.write(''.join(lines))

def parse_file(file):
    # Read all the character definitions
    characters = []
    with open(file) as infile:
        counter = 0
        for line in infile:
            # Remove trailing newlines
            line = line.rstrip('\n')
            # Skip blank lines
            if line == '':
                continue
            # Check the line's valid
            if not valid_line(line):
                print 'Invalid line "%s" in file "%s" (ignored)' % (line, file)
                continue
            # Check if we're at the start of a new character
            if counter == 0:
                characters.append([])
            # Add the line to the current character's lines
            characters[-1].append(list(line))
            # Increment the line counter
            counter += 1
            counter %= height

    # Check there are the right number of character definitions
    if len(characters) != expected_num_definitions:
        print 'Expected %d character definitions, found %d. File "%s" not converted' % (expected_num_definitions, len(characters), file)
        return

    # Convert the characters
    # (Note that the nested maps should be read backwards)
    characters = map(
        lambda ch:
            # Convert the number strings to ints
            map(lambda x: int(x, 2),
            # Replace the '-'s and '#'s with 0s and 1s
            map(lambda x: x.replace(zero_char, '0').replace(one_char, '1'),
            # Join the lines
            map(''.join,
            # Rotate the characters 90 degrees clockwise
            map(list, zip(*reversed(ch)))))),
        characters)

    # Add in all the unprintable characters and the space:
    characters = [[0] * width] * num_blank_characters + characters

    return characters

if __name__ == '__main__':
    # Determine the output type desired
    output_type = 'raw'
    if '-array' in sys.argv:
        output_type = 'array'
    elif '-basic' in sys.argv:
        output_type = 'basic'

    # Convert each file given
    for arg in sys.argv[1:]:
        # Skip options
        if arg[:1] == '-':
            continue
        # Parse the file
        characters = parse_file(arg)
        # Write to the output file
        outfile = '%s_font_%s' % (output_type, arg)
        output(outfile, characters, output_type)
