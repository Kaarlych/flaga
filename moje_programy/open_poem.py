def open_poem():
    text_lines = open('dane/poem.txt').readlines()

    poem_lines = []
    for line in text_lines:
        line = line.strip()
        poem_lines.append(line)
        
    return poem_lines


