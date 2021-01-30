import os
import shutil
import sys, getopt

def replace_yo(text):
    return list(map(lambda line: ''.join(['е' if letter == 'ё' else letter for letter in line]), text))


def get_opts():
    opts, _ = getopt.getopt(sys.argv[1:], 's:t:rp')
    return opts


def get_suffix():
    opts = get_opts()
    for opt, arg in opts:
        if opt == '-s':
            return '_' + arg
    return ''


def get_new_filenames():
    file_fio = open('фио.txt', encoding='utf-8', mode='r')
    fios = replace_yo(list(filter(lambda x: x != '', file_fio.read().split('\n'))))

    grade_fio = open('классы.txt', encoding='utf-8', mode='r')
    grades = list(filter(lambda x: x != '', grade_fio.read().split('\n')))

    new_filenames = []
    count_of_students = len(fios)
    for i in range(count_of_students):
        fio = fios[i].split(' ')
        new_filenames.append(fio[0] + '_' + fio[1] + '_' + grades[i] + 'кл' + get_suffix() + '.pdf')
    return new_filenames


def get_counts_of_lists():
    file = open('../img2pdf/количество_листов_в_работах.txt', encoding='utf-8', mode='r')
    fios = filter(lambda x: x != '', file.read().split('\n'))


def get_filenames_from_dir(dir):
    _, _, filenames = next(os.walk(dir))
    return sorted(filenames)


def copy_file(old_filename, new_filename):
    print(old_filename + ' -> ' + new_filename)
    shutil.copy('old/' + old_filename, 'new/' + new_filename)


def rename_files():
    old_filenames = sorted(get_filenames_from_dir("old"), key=lambda str: str[:str.rfind('.') - 1])
    new_filenames = get_new_filenames()

    assert (len(old_filenames) == len(new_filenames))

    for i in range(len(old_filenames)):
        copy_file(old_filenames[i], new_filenames[i])


def get_template():
    opts = get_opts()
    for opt, arg in opts:
        if opt == '-t':
            return arg

    for opt, arg in opts:
        if opt == '-s':
            return '1' * int(arg)
    print(opts)
    print("prog.py -t <template>")


# Формирует список списков имен файлов, из списка файлов отсортированный сначала по номеру листа, а после по коду


def group_from_by_task(image_filenames, template):
    grouped_image_filenames = []

    count_of_images = len(get_template())
    count_of_pdfs = len(image_filenames) // count_of_images

    for index_of_pdf in range(count_of_pdfs):

        grouped_image_filenames.append([])
        for index_of_image, t in enumerate(template):
            if t != '1':
                continue
            if index_of_image % 2 == 0:
                grouped_image_filenames[-1].append(
                    image_filenames[index_of_image // 2 * 2 * count_of_pdfs + index_of_pdf * 2])
            else:
                grouped_image_filenames[-1].append(
                    image_filenames[index_of_image // 2 * 2 * count_of_pdfs + index_of_pdf * 2 + 1])

    return grouped_image_filenames



def images_by_task_to_pdf():
    image_filenames = sorted(get_filenames_from_dir("../img2pdf/images"), key=lambda str: str[:str.rfind('.') - 1])

    grouped_image_filenames = group_from_by_task(image_filenames, get_template())

    pdf_filenames = get_new_filenames()

    assert (len(pdf_filenames) == len(grouped_image_filenames))

    dpi = 200

    for index_of_pdf, group_of_image_filenames in enumerate(grouped_image_filenames):
        print('creating pdf No.', index_of_pdf + 1)

        pdf = FPDF(unit="pt")
        for index_of_image, image_filename in enumerate(group_of_image_filenames):
            pdf.add_page()
            pdf.image('images/' + image_filename, x=1, y=1, w=1654 / dpi * 72, h=2339 / dpi * 72)

        pdf.output('pdfs/' + pdf_filenames[index_of_pdf], "F")


if __name__ == "__main__":
    if sys.argv.count('-p'):
        images_by_task_to_pdf()
    else:
        rename_files()
