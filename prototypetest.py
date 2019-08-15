import imaplib 
import email
import getpass
import sys 
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

def getPromptForEmail(gmail):
    try: 
        EMAIL_ADDRESS = input("Enter your email address: ")
        gmail.login(EMAIL_ADDRESS, getpass.getpass())
    except imaplib.IMAP4.error:
        print("login error, re-run the program")
        sys.exit(1)

# "[Gmail]/Sent Mail"
def getEmailBody(gmail):
    gmail.select(mailbox='"[Gmail]/Sent Mail"')
    head, data = gmail.search(None, 'all')
    for num in data[0].split():
        h, d = gmail.fetch(num, 'BODYSTRUCTURE')
        print
        raw_email = d[0][1]
        message = email.message_from_bytes(raw_email)
        # 件名を出していく
        email_from = str(make_header(decode_header(message['From'])))
        print("FROM: "+ email_from)
        
        subject = str(make_header(decode_header(message['Subject'])))
        print("SUBJECT: "+ subject)
        # エンコーディンを指定
        msg_encoding = 'iso-2022-jp'

         # シングルパートかマルチか割り当てる。
        if message.is_multipart() == False:
            single  = bytearray(message.get_payload(), msg_encoding)
            body = single.decode(encoding=msg_encoding)
        else:  
            multi = message.get_payload()[0]
            body = multi.get_payload(decode=True).decode(encoding=msg_encoding)
        
        # 本文
        print("BODY: " + body)


def main():
    gmail = imaplib.IMAP4_SSL("imap.gmail.com", "993")
    getPromptForEmail(gmail) 
    sys.stderr.write("----------------開始----------------\n")
    try:
        getEmailBody(gmail)
        gmail.close()
        gmail.logout()
    except Exception as ee:
        sys.stderr.write("*** error ***\n")
        sys.stderr.write(str(ee) + '\n')
    sys.stderr.write("----------------終了----------------\n")
    
#     input_file = 'test.csv'
#     output_file = 'output.csv'
#     input_array = get_test_input(input_file)
#     write_output_csv(input_array, output_file, header_for_test)

# def get_test_input(input_file):
#     """
#     csvを読み込み始め、input csv にある情報を array に渡す
#     """
#     # csv 編
    

#     print("done")

if __name__ == "__main__":
    main()
