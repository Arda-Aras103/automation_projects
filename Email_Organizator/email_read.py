import email
import imaplib 
from email.header import decode_header

sender_labels = {
    "":""
}

def decode_mime_header(header_value):
    decoded_parts = decode_header(header_value)
    full_string = ""
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            full_string += part.decode(charset or 'utf-8', errors='ignore')
        else:
            full_string += part
    return full_string


def mail_process(user_name,user_password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com",993)
    mail.login(user_name,user_password)
    mail.select("INBOX")

    status, messages = mail.search(None,"ALL")


    for num in reversed(messages[0].split()):
        status, messages_data = mail.fetch(num,"(RFC822)")
        raw_email = messages_data[0][1]
        msg = email.message_from_bytes(raw_email)

        print("="*50)
        print(decode_mime_header(msg["From"]))
        print(decode_mime_header(msg["Subject"]))
        print(decode_mime_header(msg["Date"]))
        print("-"*50)

        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                print(part.get_payload(decode=True).decode(errors="ignore"))
        


        if decode_mime_header(msg["From"]) in sender_labels:
            label = sender_labels[decode_mime_header(msg["From"])]
            mail.store(num, '+X-GM-LABELS', label)
            mail.store(num, '+FLAGS', r'(\Deleted)')
            print(f"Mail from {decode_mime_header(msg['From'])} labeled as {label}")
        mail.expunge()
        

    print("="*50)

    mail.close()
    mail.logout()

if __name__ == "__main__":
    user_name = input("Enter email adress: ")
    user_password = input("Enter email password: ")

    mail_process(user_name,user_password)
