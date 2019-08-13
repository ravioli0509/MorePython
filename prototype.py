import imaplib 
import email
import getpass
import sys 

# ログイン情報
EMAIL_ADDRESS = "" 
    
def getEmailBody(gmail):
    gmail.select("inbox")
    # select the labels　data[0].split():
    head, data = gmail.search(None, 'ALL')

    for num in data[0].split():
        # メッセージのenconding をutf-8として指定。
        h, d = gmail.fetch(num, '(RFC822)')
        raw_email = d[0][1]
        # import pdb;pdb.set_trace()
        message = email.message_from_string(raw_email.decode('utf-8'))
        message_encoding = email.header.decode_header(message.get('Subject'))[0][1] or 'iso-2022-jp'
        message_subject = email.header.decode_header(message.get('Subject'))[0][0]
        # メールのヘッダーをstringに
        subject = str(message_subject.decode(message_encoding))
        print(subject)
        
        body = message.get_payload()
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
    getEmailBody(gmail)
    gmail.close()
    gmail.logout()

    print("done")

if __name__ == "__main__":
    main()
