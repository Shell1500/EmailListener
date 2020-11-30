import imaplib
import email
import pyperclip ## pyperclip to copy to clipboard
import downloader_vid ## yt-dl to download video
import time
from email.header import Header, decode_header, make_header

print('''##______________________________________________
## Shell1500
## A small program to listen to emails
## Currently Using to download yt videos to pc or copy links etc to clipboard
##______________________________________________
      ''')

## https://myaccount.google.com/lesssecureapps  ## enable less secure apps before continuing

FROM_EMAIL  = "" + "@gmail.com"  ## your email
FROM_PWD    = "" ## your password
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993


## function that fetches the latest email
def get_mail():
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)
    mail.select('inbox')
    type, data = mail.search(None, 'ALL')

    ## iterate over data[0].split() to get all the mails
    ## using data[0].split()[-1] to get the latest email
    
    typ, msg_data = mail.fetch(data[0].split()[-1], '(RFC822)')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])

        maintype = msg.get_content_maintype()
        
        ## getting body of the email
        if maintype == 'multipart':
            for part in msg.get_payload():
                if part.get_content_maintype() == 'text':
                    ## getting the subject along with body
                    ## use msg['from'] or msg['to'] to get sender and reciever
                    return (msg['subject'], part.get_payload().strip())
        elif maintype == 'text':
            ## getting the subject along with body
            ## use msg['from'] or msg['to'] to get sender and reciever
            return (msg['subject'], msg.get_payload().strip())
        
        
prev = () ## keeping track of last email
print('Fetching Mails\n')
while True:
    message = get_mail() ## getting last email
    if message != prev:
        print(message)
        
        ## message[0] --> subject
        ## message[1] --> body
        
        ## downloading vid by link if 'Youtube' or 'download' in subject
        if 'download' in message[0] or 'YouTube' in message[0]:
            link = message[1]
            print('Got Link: ' + link)
            downloader_vid.download_link(link)
            print(link + ' Downloaded!')
            
        ## copying to clipboard
        if 'copy' in message[0] or 'cp' in message[0]:
            value = message[1]
            print(value + ' Copied!')
            pyperclip.copy(value)
        
        ## setting previous email
        prev = message
        
    else:
        print('no new found')
    
    ## adding 5 second delay between request
    time.sleep(5)
