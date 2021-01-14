import os
import shutil
import sys, getopt
from fpdf import FPDF


def get_opts():
    opts, _ = getopt.getopt(sys.argv[1:], 'st:rp')
    return opts

def get_suffix():
    opts = get_opts()
    for opt, arg in opts:
        if opt == '-s':
            return arg
    return ''


def get_new_filenames():
    file_fio = open('фио.txt', encoding='utf-8', mode='r')
    fios = file_fio.read().split('\n')

    grade_fio = open('классы.txt', encoding='utf-8', mode='r')
    grades = grade_fio.read().split('\n')

    new_filenames = []
    count_of_students = len(fios)
    for i in range(count_of_students):
        fio = fios[i].split(' ')
        new_filenames.append(fio[0] + '_' + fio[1] + '_' + grades[i] + 'кл' + get_suffix() + '.pdf')
    return new_filenames


def get_filenames_from_dir(dir):
    _, _, filenames = next(os.walk(dir))
    return sorted(filenames)


def copy_file(old_filename, new_filename):
    print(old_filename + ' -> ' + new_filename)
    shutil.copy('old/' + old_filename, 'new/' + new_filename)

def rename_files():
    old_filenames = get_filenames_from_dir('old')
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

def group(image_filenames, template):
    grouped_image_filenames = []

    count_of_images = len(get_template())
    count_of_pdfs = len(image_filenames) // count_of_images

    for index_of_pdf in range(count_of_pdfs):

        grouped_image_filenames.append([])
        for index_of_image, t in enumerate(template):
            if t != '1':
                continue
            grouped_image_filenames[-1].append(image_filenames[index_of_image * count_of_pdfs + index_of_pdf])

    return grouped_image_filenames


def images_to_pdf():
    image_filenames = get_filenames_from_dir("images")

    grouped_image_filenames = group(image_filenames, get_template())

    pdf_filenames = get_new_filenames()

    assert(len(pdf_filenames) == len(grouped_image_filenames))

    for index_of_pdf, chunk_of_image_filenames in enumerate(grouped_image_filenames):
        print('creating pdf No.', index_of_pdf + 1)

        pdf = FPDF()
        for index_of_image, image_filename in enumerate(chunk_of_image_filenames):
            pdf.add_page()
            pdf.image('images/' + image_filename)

        pdf.output('pdfs/' + pdf_filenames[index_of_pdf], "F")




if __name__ == "__main__":
    if sys.argv.count('-r'):
        rename_files()
    elif sys.argv.count('-p'):
        images_to_pdf()