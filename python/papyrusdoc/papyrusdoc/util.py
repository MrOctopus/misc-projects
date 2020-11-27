def sanitize_line(line):
    start_index = 0

    while True:
        index = line.find(';', start_index) 
        if index == -1:
            break

        if line[index - 1] != '\\':
            line = line[:index].strip()
            break

        start_index = index + 1

    return line