def replace_yo(text):
    return list(map(lambda line: ''.join(['е' if letter == 'ё' else letter for letter in line]), text))

file_fi = open('участники_тура.txt', encoding='utf-8', mode='r')
fis = replace_yo(list(filter(lambda x: x != '', file_fi.read().split('\n'))))

fi_list = []
for line in [line1.split() for line1 in fis]:
    fi_list.append(line[0] + ' ' + line[1])

fis = fi_list



file_all_fi_and_email = open('участники_почта.txt', encoding='utf-8', mode='r')
all_fis_and_email = replace_yo(list(filter(lambda x: x != '', file_all_fi_and_email.read().split('\n'))))

list2 = []
added = []
for line in [line1.split() for line1 in all_fis_and_email]:
    if added.count(line[1] + ' ' + line[2]) == 0:
        added.append(line[1] + ' ' + line[2])
        list2.append(line)

#  + ' ' + x[1] + ' ' + x[2] + ' ' + x[3]

list2 = list(dict.fromkeys([x[0] + ' ' + x[1] + ' ' + x[2] for x in sorted(list(filter(lambda x: fis.count(x[1] + ' ' + x[2]) > 0, list2)), key = lambda x: (x[1], x[2]))]))


file_tour_emails = open('участники_тура_почты.txt', encoding='utf-8', mode='w')

file_tour_emails.write('\n'.join(list2))

file_tour_emails.close()

list1 = list(dict.fromkeys([x[0] for x in sorted(list(filter(lambda x: fis.count(x[1] + ' ' + x[2]) > 0, list2)), key = lambda x: (x[1], x[2]))]))

file_tour_emails = open('участники_тура_почты_just.txt', encoding='utf-8', mode='w')

file_tour_emails.write('\n'.join(list1))

file_tour_emails.close()

print('\n'.join(list2))
