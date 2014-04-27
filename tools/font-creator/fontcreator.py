import sys, re

zero_char, one_char = '-', '#'
width, height = 5, 8
num_blank_characters = 32 + 1 # 32 unprintable characters and ' '
expected_num_definitions = 128 - num_blank_characters

def valid_line(line, search=re.compile(r'[^-#]').search):
    return len(line) == width and not bool(search(line))

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
    # Rotate the characters 90 degrees clockwise
    characters = map(lambda ch: map(list, zip(*reversed(ch))), characters)
    # Join the lines
    characters = map(lambda ch: map(''.join, ch), characters)
    # Replace the '-'s and '#'s with 0s and 1s
    characters = map(lambda ch: map(lambda x: x.replace(zero_char, '0').replace(one_char, '1'), ch), characters)
    # Convert the number strings ints
    characters = map(lambda ch: map(lambda x: int(x, 2), ch), characters)
    # Add in all the unprintable characters and the space:
    characters = [[0] * width] * num_blank_characters + characters
    # Write to the output file
    with open('font_' + file, 'w') as outfile:
        outfile.write('{\n')
        for character in characters:
            outfile.write('  ' + ''.join(['0x%02x,' % x for x in character]) + '\n')
        outfile.write('}\n')

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        parse_file(arg)
