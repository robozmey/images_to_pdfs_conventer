def replace_yo(text):
    return list(map(lambda line: ''.join(['е' if letter == 'ё' else letter for letter in line]), text))


def get_fi_tour():
    file_fi = open('участники_тура.txt', encoding='utf-8', mode='r')
    fis = replace_yo(list(filter(lambda x: x != '', file_fi.read().split('\n'))))

    fi_list = []
    for line in [list(filter(lambda x: x != '', line1.split())) for line1 in fis]:
        fi_list.append(line[0] + ' ' + line[1])

    return fi_list

def get_fi_emails_all():

    file_all_fi_and_email = open('участники_почта.txt', encoding='utf-8', mode='r')
    all_fis_and_email = replace_yo(list(filter(lambda x: x != '', file_all_fi_and_email.read().split('\n'))))

    list2 = []
    added = []
    for line in [line1.split() for line1 in all_fis_and_email]:
        if added.count(line[0] + ' ' + line[1] + ' ' + line[2]) == 0:
            added.append(line[0] + ' ' + line[1] + ' ' + line[2])
            list2.append(line)

    return list2


def get_fi_emails_tour(fis, fi_emails_all):
    return [x[0] + ' ' + x[1] + ' ' + x[2] for x in
                                sorted(list(filter(lambda x: fis.count(x[1] + ' ' + x[2]) > 0, fi_emails_all)),
                                       key=lambda x: (x[1], x[2]))]


def save_fi_emails_tour(fi_emails_tour):
    file_tour_emails = open('участники_тура_почты.txt', encoding='utf-8', mode='w')

    file_tour_emails.write('\n'.join(fi_emails_tour))

    file_tour_emails.close()

def save_emails_tour(fi_emails_tour):

    list1 = list(dict.fromkeys([x[0] for x in sorted(list(filter(lambda x: fis.count(x[1] + ' ' + x[2]) > 0, fi_emails_tour)),
                                                     key=lambda x: (x[1], x[2]))]))

    file_tour_emails = open('участники_тура_почты_just.txt', encoding='utf-8', mode='w')

    file_tour_emails.write('\n'.join(list1))

    file_tour_emails.close()


if __name__ == "__main__":
    fis = get_fi_tour()

    fi_emails_all = get_fi_emails_all()

    fi_emails_tour = get_fi_emails_tour(fis, fi_emails_all)

    save_fi_emails_tour(fi_emails_tour)

    print('\n'.join(fi_emails_tour))
