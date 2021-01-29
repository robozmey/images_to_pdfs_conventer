import smtplib  # Импортируем библиотеку по работе с SMTP
import os  # Функции для работы с операционной системой, не зависящие от используемой операционной системы

import mimetypes  # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders  # Импортируем энкодер
from email.mime.base import MIMEBase  # Общий тип
from email.mime.text import MIMEText  # Текст/HTML
from email.mime.image import MIMEImage  # Изображения
from email.mime.audio import MIMEAudio  # Аудио
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект

from glob import glob


def get_addr_from():
    key_file = open('email_key.txt', encoding='utf-8', mode='r')
    return list(filter(lambda x: x != '', key_file.read().split('\n')))[0]


def get_password():
    key_file = open('email_key.txt', encoding='utf-8', mode='r')
    return list(filter(lambda x: x != '', key_file.read().split('\n')))[1]


def send_email(addr_to, msg_subj, msg_text, files):
    addr_from = get_addr_from()
    password = get_password()

    #print('"' + addr_from + '" "' + password + '"')

    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = addr_from  # Адресат
    msg['To'] = addr_to  # Получатель
    msg['Subject'] = msg_subj  # Тема сообщения


    body = msg_text  # Текст сообщения
    msg.attach(MIMEText(body, 'html'))  # Добавляем в сообщение текст

    process_attachement(msg, files)

    server = smtplib.SMTP('smtp.gmail.com', 587)  # Создаем объект SMTP
    server.starttls()  # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password)  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    server.quit()  # Выходим


def process_attachement(msg, files):  # Функция по обработке списка, добавляемых к сообщению файлов
    for f in files:
        if os.path.isfile(f):  # Если файл существует
            attach_file(msg, f)  # Добавляем файл к сообщению
        elif os.path.exists(f):  # Если путь не файл и существует, значит - папка
            dir = os.listdir(f)  # Получаем список файлов в папке
            for file in dir:  # Перебираем все файлы и...
                attach_file(msg, f + "/" + file)  # ...добавляем каждый файл к сообщению


def attach_file(msg, filepath):  # Функция по добавлению конкретного файла к сообщению
    filename = os.path.basename(filepath)  # Получаем только имя файла
    ctype, encoding = mimetypes.guess_type(filepath)  # Определяем тип файла на основе его расширения
    if ctype is None or encoding is not None:  # Если тип файла не определяется
        ctype = 'application/octet-stream'  # Будем использовать общий тип
    maintype, subtype = ctype.split('/', 1)  # Получаем тип и подтип
    if maintype == 'text':  # Если текстовый файл
        with open(filepath) as fp:  # Открываем файл для чтения
            file = MIMEText(fp.read(), _subtype=subtype)  # Используем тип MIMEText
            fp.close()  # После использования файл обязательно нужно закрыть
    elif maintype == 'image':  # Если изображение
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'audio':  # Если аудио
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
    else:  # Неизвестный тип файла
        with open(filepath, 'rb') as fp:
            file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
            file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
            fp.close()
            encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
    file.add_header('Content-Disposition', 'attachment', filename=filename)  # Добавляем заголовки
    msg.attach(file)  # Присоединяем файл к сообщению


def get_addr_to():
    addr_to_file = open('addr_to.txt', encoding='utf-8', mode='r')
    return [x.split(' ')[0] for x in list(filter(lambda x: x != '', addr_to_file.read().split('\n')))]


def get_email_fio():
    addr_to_file = open('addr_to.txt', encoding='utf-8', mode='r')
    return [x.split(' ') for x in list(filter(lambda x: x != '', addr_to_file.read().split('\n')))]


def get_subject():
    subject_file = open('subject.txt', encoding='utf-8', mode='r')
    return list(filter(lambda x: x != '', subject_file.read().split('\n')))[0]


def get_text():
    text_file = open('text.htm', encoding='windows-1251', mode='r')
    return text_file.read()


def get_file_by_name(fio):
    return glob('personal_attachments/' + fio[0] + '_' + fio[1] + '*')


if __name__ == "__main__":
    mutual_files = ['attachments']

    subject = get_subject()

    text = get_text()

    for email_fio in get_email_fio():
        assert(len(get_file_by_name(email_fio[1:])) > 0)

    for email_fio in get_email_fio():
        personal_files = get_file_by_name(email_fio[1:])

        print(email_fio[0] + ': ' + str(personal_files))

        send_email(email_fio[0], subject, text, mutual_files + personal_files)

    input('Отправка завершена')

