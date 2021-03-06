#-*- coding:utf-8 -*-
import imaplib 
import email
import getpass
import sys 
import os 
import csv
from email.header import decode_header, make_header
import mailbox
import datetime

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

email_array = []

# ログイン情報
EMAIL_ADDRESS = "" 

def getPromptForAccessingEmail(gmail, prompt):
    while prompt == True:     
        try: 
            EMAIL_ADDRESS = input("Enter your email address: ")
            gmail.login(EMAIL_ADDRESS, getpass.getpass())
            prompt = False
        except imaplib.IMAP4.error as error:
            sys.stderr.write("LOGIN ERROR, "+ str(error) + '\n')
            error_prompt=input("Do you want to try again? (Y/N): ")
            if error_prompt.lower() == "y":
                sys.stderr.write("Okay, try again." + '\n')
                continue
            elif error_prompt.lower() == "n":
                sys.stderr.write("Okay, good bye." + '\n')
                sys.exit(1)
        

# "[Gmail]/Sent Mail"
def getEmailBody(gmail):
    gmail.select(mailbox='"[Gmail]/Sent Mail"')
    gmail.list()
    result, data = gmail.uid('search', None, 'all')
    result, data = gmail.search(None, 'all')
    num_emails = len(data[0].split())
    for message in range(num_emails):
        latest = data[0].split()[message]
        result, email_data = gmail.uid('fetch', latest, '(RFC822)')
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
    
        # 日付を出力する
        date = email.utils.parsedate_tz(email_message['Date'])
        if date:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date))
            string_date = str(local_date.strftime("%a, %d %b %Y %H: %M: %S"))

        '''
        email_from, email_to, email_subject, email_date, email_body =  -- からのメール, 宛先, 件名, 日時, 本文 
        '''
        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
        email_subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
        email_date = "%s" %(string_date)
    
        # Body details 本文を出力
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body_decode = part.get_payload(decode=True)
                email_body = body_decode.decode('utf-8')
                print("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" %(email_from, email_to, email_date, email_subject, email_body))
                email_array.append([email_body])
            else:
                continue


def write_output_csv(email_array, output_file, header_for_test):
    """
    処理したarrayをoutput file に書く。
    """
    with open(output_file, "w") as output_file:
        csv_writer = csv.writer(output_file, delimiter=',')
        csv_writer.writerow(header_for_test)
        csv_writer.writerows(email_array)

def clean_array():
    """
    we clean up the array given from the email output. Therefore we only take the body of the email. 

    """
    pass 

def count_for_keyword():
    pass

def main():
    os.system('clear')
    prompt = True
    gmail = imaplib.IMAP4_SSL("imap.gmail.com")
    getPromptForAccessingEmail(gmail, prompt) 
    sys.stderr.write("----------------開始----------------\n")
    try:
        getEmailBody(gmail)
        gmail.close()
        gmail.logout()
    except Exception as ee:
        sys.stderr.write("*** error ***\n")
        sys.stderr.write(str(ee) + '\n')
    sys.stderr.write("----------------終了----------------\n")
    
    output_file = 'output.csv'
    write_output_csv(email_array, output_file, header_for_test)


if __name__ == "__main__":
    main()
