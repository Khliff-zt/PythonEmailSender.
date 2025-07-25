# Python Email Repository

This repository demonstrates how to send emails using Python with the `smtplib` and `email` standard libraries, as well as the third-party `emails` library for advanced email handling. It includes examples for sending plain text emails, HTML emails, emails with attachments, and templated emails using Jinja2.

## Repository Structure

```
python-email-repo/
│
├── src/
│   ├── plain_text_email.py        # Send a simple plain text email
│   ├── html_email.py             # Send an HTML email
│   ├── attachment_email.py       # Send an email with attachments
│   ├── template_email.py         # Send a templated email using Jinja2
│
├── templates/
│   ├── receipt_template.html      # Jinja2 HTML template for emails
│
├── config/
│   ├── config.ini                # Configuration file for SMTP settings
│
├── requirements.txt              # Dependencies
├── README.md                     # This file
└── LICENSE                       # MIT License
```

## Prerequisites

- Python 3.6 or higher
- A valid SMTP server (e.g., Gmail, Outlook, or a local SMTP server for testing)
- Install required packages: `pip install -r requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/python-email-repo.git
   cd python-email-repo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure SMTP settings:
   - Copy `config/config.ini.example` to `config/config.ini`
   - Update `config.ini` with your SMTP server details and credentials:
     ```ini
     [smtp]
     server = smtp.gmail.com
     port = 587
     from_addr = your_email@gmail.com
     password = your_password
     ```

   **Note**: For Gmail, you may need to use an App Password if 2FA is enabled, and enable "Less secure app access" (not recommended for production).

## Usage

### 1. Sending a Plain Text Email
Run the script to send a simple plain text email:
```bash
python src/plain_text_email.py
```

### 2. Sending an HTML Email
Run the script to send an HTML-formatted email:
```bash
python src/html_email.py
```

### 3. Sending an Email with Attachments
Run the script to send an email with a file attachment:
```bash
python src/attachment_email.py
```

### 4. Sending a Templated Email
Run the script to send an email using a Jinja2 template:
```bash
python src/template_email.py
```

## Example Scripts

### `src/plain_text_email.py`
```python
import smtplib
import configparser
from email.mime.text import MIMEText

def send_plain_text_email(subject, to_addr, body_text):
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    
    host = config.get('smtp', 'server')
    port = config.get('smtp', 'port')
    from_addr = config.get('smtp', 'from_addr')
    password = config.get('smtp', 'password')

    msg = MIMEText(body_text, 'plain')
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr

    try:
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()

if __name__ == "__main__":
    subject = "Test Email from Python"
    to_addr = "recipient@example.com"
    body_text = "This is a test email sent using Python's smtplib."
    send_plain_text_email(subject, to_addr, body_text)
```

### `src/html_email.py`
```python
import smtplib
import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_html_email(subject, to_addr, html_content):
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    
    host = config.get('smtp', 'server')
    port = config.get('smtp', 'port')
    from_addr = config.get('smtp', 'from_addr')
    password = config.get('smtp', 'password')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr

    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)

    try:
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        print("HTML email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()

if __name__ == "__main__":
    subject = "HTML Test Email"
    to_addr = "recipient@example.com"
    html_content = """
    <html>
        <body>
            <h1>Hello from Python!</h1>
            <p>This is an <b>HTML</b> email sent using Python.</p>
        </body>
    </html>
    """
    send_html_email(subject, to_addr, html_content)
```

### `src/attachment_email.py`
```python
import smtplib
import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_attachment_email(subject, to_addr, body_text, filename):
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    
    host = config.get('smtp', 'server')
    port = config.get('smtp', 'port')
    from_addr = config.get('smtp', 'from_addr')
    password = config.get('smtp', 'password')

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg.attach(MIMEText(body_text, 'plain'))

    try:
        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        msg.attach(part)
        
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        print("Email with attachment sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()

if __name__ == "__main__":
    subject = "Email with Attachment"
    to_addr = "recipient@example.com"
    body_text = "This email contains an attachment."
    filename = "example.txt"  # Ensure this file exists in the project directory
    send_attachment_email(subject, to_addr, body_text, filename)
```

### `src/template_email.py`
```python
import smtplib
import configparser
from emails import Message
from emails.template import JinjaTemplate as T

def send_template_email(to_addr, template_data):
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    
    host = config.get('smtp', 'server')
    port = config.get('smtp', 'port')
    from_addr = config.get('smtp', 'from_addr')
    password = config.get('smtp', 'password')

    message = Message(
        html=T(open('templates/receipt_template.html').read()),
        subject=T('Payment Receipt No.{{ billno }}'),
        mail_from=( 'Your Company', from_addr)
    )

    try:
        r = message.send(
            to=to_addr,
            render=template_data,
            smtp={'host': host, 'port': port, 'ssl': False, 'tls': True, 'user': from_addr, 'password': password}
        )
        if r.status_code == 250:
            print("Templated email sent successfully!")
        else:
            print(f"Failed to send email: Status code {r.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    to_addr = "recipient@example.com"
    template_data = {'name': 'John Doe', 'billno': '123456789'}
    send_template_email(to_addr, template_data)
```

### `templates/receipt_template.html`
```html
<html>
    <head>
        <style>
            h1 { color: #333; }
            p { font-family: Arial, sans-serif; }
        </style>
    </head>
    <body>
        <h1>Dear {{ name }}!</h1>
        <p>This is your receipt for payment No. {{ billno }}.</p>
        <p>Thank you for your purchase!</p>
    </body>
</html>
```

### `config/config.ini.example`
```ini
[smtp]
server = smtp.gmail.com
port = 587
from_addr = your_email@gmail.com
password = your_password
```

### `requirements.txt`
```
emails==0.6
Jinja2==3.1.2
```

### `LICENSE`
```
MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Notes

- **Security**: Avoid hardcoding credentials in scripts. Use environment variables or a secure configuration file (like `config.ini`) for sensitive data.
- **Gmail SMTP**: If using Gmail, ensure "Less secure app access" is enabled or use an App Password with 2FA. For production, consider using an email API like MailerSend or Elastic Email for better reliability and analytics.[](https://www.mailersend.com/blog/send-email-with-python)
- **Third-Party Library**: The `emails` library simplifies advanced email tasks like templating and DKIM signatures. See its documentation for more features.[](https://github.com/lavr/python-emails)[](https://python-emails.readthedocs.io/en/latest/)
- **Testing**: Use a local SMTP server (e.g., `smtpd` for debugging) to test email sending without risking real email accounts.[](https://realpython.com/python-send-email/)
- **Further Enhancements**: Add error handling for SMTP-specific exceptions (`SMTPAuthenticationError`, `SMTPConnectError`), deduplicate recipient lists, or integrate with APIs like Mailtrap or MailerSend for bulk sending.[](https://mailtrap.io/blog/python-send-email/)[](https://www.mailersend.com/blog/send-email-with-python)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.