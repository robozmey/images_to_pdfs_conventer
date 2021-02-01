import os
import shutil
import sys, getopt

import pygubu
from pygubu.widgets.pathchooserinput import PathChooserInput

import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk




def replace_yo(text):
    return list(map(lambda line: ''.join(['е' if letter == 'ё' else letter for letter in line]), text))


def get_opts():
    opts, _ = getopt.getopt(sys.argv[1:], 's:t:rp')
    return opts





def get_fios_from_file(file_fio_name = 'фио.txt'):
    file_fio = open(file_fio_name, encoding='utf-8', mode='r')
    return list(filter(lambda x: x != '', file_fio.read().split('\n')))


def get_grades_from_file(grade_fio_name = 'классы.txt'):
    grade_fio = open(grade_fio_name, encoding='utf-8', mode='r')
    return list(filter(lambda x: x != '', grade_fio.read().split('\n')))


def get_filenames_from_dir(dir):
    _, _, filenames = next(os.walk(dir))
    return sorted(filenames)


def copy_file(old_filename, new_filename, old_directory='old', new_directory='new'):
    print(old_filename + ' -> ' + new_filename)
    shutil.copy(old_directory + '/' + old_filename, new_directory + '/' + new_filename)



class RenameMainApp:
    def __init__(self, master):
        self.mainwindow = ttk.Frame(master)
        self.participantLabel = ttk.Label(self.mainwindow)
        self.participantLabel.configure(text='Имена участников')
        self.participantLabel.grid(columnspan='1')
        self.participantText = tk.Text(self.mainwindow)
        self.participantText.configure(height='40', relief='ridge', state='normal', undo='true')
        self.participantText.configure(width='50')
        self.participantText.grid(columnspan='2', row='1')
        self.gradeLabel = ttk.Label(self.mainwindow)
        self.gradeLabel.configure(text='Классы участников')
        self.gradeLabel.grid(column='3', row='0')
        self.gradeText = tk.Text(self.mainwindow)
        self.gradeText.configure(blockcursor='false', height='40', relief='ridge', state='normal')
        self.gradeText.configure(undo='true', width='20')
        self.gradeText.grid(column='3', row='1')
        self.namelessPath = PathChooserInput(self.mainwindow)
        self.namelessPath.configure(type='directory')
        self.namelessPath.grid(column='1', columnspan='3', row='2')
        self.namelessLabel = ttk.Label(self.mainwindow)
        self.namelessLabel.configure(text='Директрория с безымянными')
        self.namelessLabel.grid(column='0', row='2')
        self.destinationLabel = ttk.Label(self.mainwindow)
        self.destinationLabel.configure(text='Директория для переименованных')
        self.destinationLabel.grid(column='0', row='3')
        self.destinationPath = PathChooserInput(self.mainwindow)
        self.destinationPath.configure(type='directory')
        self.destinationPath.grid(column='1', columnspan='3', row='3')
        self.renameButton = ttk.Button(self.mainwindow)
        self.renameButton.configure(text='Переименовать')
        self.renameButton.grid(column='3', row='7')
        self.renameButton.bind('<1>', self.rename_files, add='')
        self.suffixEntry = ttk.Entry(self.mainwindow)
        suffix = tk.StringVar()
        self.suffixEntry.configure(font='TkDefaultFont', textvariable=suffix)
        self.suffixEntry.grid(column='0', row='6')
        self.suffixLabel = ttk.Label(self.mainwindow)
        self.suffixLabel.configure(text='Суффикс')
        self.suffixLabel.grid(column='0', row='5')
        self.mainwindow.configure(borderwidth='10', height='200', width='200')
        self.mainwindow.pack(side='top')

        # Main widget
        self.mainwindow = self.mainwindow



    def get_fios(self):
        return list(filter(lambda x: x != '', self.participantText.get("1.0", "end").split('\n')))

    def get_grades(self):
        return list(filter(lambda x: x != '', self.gradeText.get("1.0", "end").split('\n')))

    def get_suffix(self):
        suffix = self.suffixEntry.get()
        if suffix != '':
            return '_' + suffix
        return ''

    def get_new_filenames(self):
        fios = replace_yo(self.get_fios())

        grades = self.get_grades()

        if len(fios) != len(grades):
            tkinter.messagebox.showerror(title='Предупреждение', message='Количество учеников не соответствует количеству их классов. Хотите продолжить?')
            return

        suffix = self.get_suffix()

        new_filenames = []
        count_of_students = len(fios)
        for i in range(count_of_students):
            fio = fios[i].split(' ')
            new_filenames.append(fio[0] + '_' + fio[1] + '_' + grades[i] + 'кл' + suffix + '.pdf')
        return new_filenames

    def rename_files(self, event):
        old_directory = self.namelessPath.cget('path')
        new_directory = self.destinationPath.cget('path')

        print(old_directory)


        if old_directory == '':
            tk.messagebox.showerror(title='Ошибка!', message='Не выбрана директория с файлами для переименовывания')
            return

        if new_directory == '':
            tk.messagebox.showerror(title='Ошибка!', message='Не выбрана директория для переименованных файлов')
            return

        old_filenames = sorted(get_filenames_from_dir(old_directory), key=lambda str: str[:str.rfind('.') - 1])
        new_filenames = self.get_new_filenames()

        if new_filenames == None:
            return

        if len(old_filenames) != len(new_filenames):
            tk.messagebox.showerror(title='Ошибка!', message='Количество файлов для переименования не соответствует количеству учеников')
            return

        popup = tk.Toplevel()
        tk.Label(popup, text="Files have renamed").grid(row=0, column=0, columnspan=2)
        log_field = tk.Text(popup, width=100)
        log_field.grid(row=1, column=0, columnspan=2)
        progress = 0
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(popup, length=400, variable=progress_var, maximum=100)
        progress_bar.grid(row=2, column=0)  # .pack(fill=tk.X, expand=1, side=tk.BOTTOM)
        popup.pack_slaves()

        counter = tk.Label(popup)
        counter.grid(row=2, column=1)

        progress_step = float(100.0 / len(old_filenames))

        popup.update()

        log = ''

        for i in range(len(old_filenames)):

            copy_file(old_filenames[i], new_filenames[i])

            progress += progress_step
            progress_var.set(progress)

            log += old_filenames[i] + ' -> ' + new_filenames[i] + '\n'

            log_field.delete(1.0, "end")
            log_field.insert("end", log)

            counter['text'] = str(i+1) + '/' + str(len(old_filenames))

            popup.update()

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = RenameMainApp(root)
    app.run()
