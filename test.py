import imaplib 
import email
import getpass
import sys 
import base64
import os 
import csv
from email.header import decode_header, make_header

# ログイン情報
EMAIL_ADDRESS = "" 

"""
csv の column名
"""

header_for_test = [
    '表記ブレミス数',
    '改行ミス数',
    '全角半角ミス数',
    '求人IDミス数',
    '顧客IDミス数',
    'コピー欄ミス数',
    '給与情報ミス数',
    '仕事内容のミス数',
    'indeed titleミス数',
    '勤務地情報ミス数',
    '企業情報ミス数',
    '備考ミス数',
    '職種コードミス数',
    '特徴コードミス数',
    ''
    ]
    
def getEmailBody(gmail, base64):
    gmail.select("inbox")
    # select the labels　data[0].split():
    head, data = gmail.search(None, 'ALL')

    for num in data[0].split():
        # メッセージのenconding をutf-8として指定。.decode('utf-8')
        h, d = gmail.fetch(num, '(RFC822)')
        raw_email = d[0][1]
        email_message = email.message_from_bytes(raw_email)
        # import pdb;pdb.set_trace()
        message = email.message_from_bytes(raw_email)
        message_encoding = email.header.decode_header(message.get('Subject'))[0][1] or 'iso-2022-jp'
        message_subject = email.header.decode_header(message.get('Subject'))[0][0]
        # メールのヘッダーをstringに
        subject = str(message_subject.decode(message_encoding))
        print(subject)
        
        body = message.get_payload(decode=True)
        print(body)

def getPromptForEmail(gmail):
    try: 
        EMAIL_ADDRESS = input("Enter your email address: ")
        gmail.login(EMAIL_ADDRESS, getpass.getpass())
    except imaplib.IMAP4.error:
        print("login error, re-run the program")
        sys.exit(1)

def main():
    gmail = imaplib.IMAP4_SSL("imap.gmail.com", "993")
    getPromptForEmail(gmail) 
    getEmailBody(gmail, base64)
    gmail.close()
    gmail.logout()

def get_test_input(input_file):
    """
    csvを読み込み始め、input csv にある情報を array に渡す
    """
    # csv 編
    input_file = 'test.csv'
    output_file = 'output.csv'
    input_array = get_test_input(input_file)
    write_output_csv(input_array, output_file, header_for_test)

    print("done")

if __name__ == "__main__":
    main()
