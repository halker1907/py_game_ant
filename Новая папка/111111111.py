code = []
while True:
    line = input()
    if '#' in line:
        break
    if line:
        code.append(line)
X = 0
Y = 0
#вне цикла без аргумента line[0:4] != '    ':#вне цикла
#вне цикла с аргументом
#в цикле без аргумента line[0:4] == '    ':#вне цикла
#в цикле с аргументом
#сам цикл
for line in code:
    if line[0:4] != '    ':#вне цикла
        pass