def process_line(line):
    elements = line.split()
    new_elements = [elements[0]] + elements[2:7] + ['1']
    if elements[1] == '2':
        new_elements.append('2')
    elif elements[1] == '5':
        new_elements.append('3')
    elif elements[1] == '7':
        new_elements.append('4')
    elif elements[1] == '0':
        new_elements.append('1')
    new_elements.append('1')
    return ','.join(new_elements)

with open('tracking_result.txt', 'r') as input_file, open('output.txt', 'w') as output_file:
    for line in input_file:
        new_line = process_line(line.strip())
        output_file.write(new_line + '\n')