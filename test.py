import imaplib 
import email 

# ログイン情報
User = "hrf.saiyogo.kenpin@gmail.com"
Pass = "Passkenpin"

gmail = imaplib.IMAP4_SSL("imap.gmail.com", "993")
gmail.login(User, Pass)
gmail.select("inbox")

# select the labels
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

    body = message.get_payload(encode=True)
    print(body)

gmail.close()
gmail.logout()

print("done")