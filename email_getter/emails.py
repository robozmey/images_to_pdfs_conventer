file_fio = open('участники_тура.txt', encoding='utf-8', mode='r')
fios = list(map(lambda x: str(('е' if i == 'ё' else i) for i in x), (lambda x: x != '', file_fio.read().split('\n'))))

file_all_fio_and_email = open('участники_почта.txt', encoding='utf-8', mode='r')
all_fios_and_email = reversed(list(filter(lambda x: x != '', file_all_fio_and_email.read().split('\n'))))

list2 = []
added = []
for line in [line1.split() for line1 in all_fios_and_email]:
    if added.count(line[1] + ' ' + line[2] + ' ' + line[3]) == 0:
        added.append(line[1] + ' ' + line[2] + ' ' + line[3])
        list2.append(line)

#  + ' ' + x[1] + ' ' + x[2] + ' ' + x[3]

list2 = list(dict.fromkeys([x[0] + ' ' + x[1] + ' ' + x[2] + ' ' + x[3] for x in sorted(list(filter(lambda x: fios.count(x[1] + ' ' + x[2] + ' ' + x[3]) > 0, list2)), key = lambda x: (x[1], x[2], x[3]))]))


file_tour_emails = open('участники_тура_почты.txt', encoding='utf-8', mode='w')

file_tour_emails.write('\n'.join(list2))

file_tour_emails.close()

list1 = list(dict.fromkeys([x[0] for x in sorted(list(filter(lambda x: fios.count(x[1] + ' ' + x[2] + ' ' + x[3]) > 0, list2)), key = lambda x: (x[1], x[2], x[3]))]))

file_tour_emails = open('участники_тура_почты_just.txt', encoding='utf-8', mode='w')

file_tour_emails.write('\n'.join(list1))

file_tour_emails.close()

print('\n'.join(list2))
