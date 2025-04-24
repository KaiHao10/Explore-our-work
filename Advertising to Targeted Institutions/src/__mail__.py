from auto_send_mail.Mail import MailConfig, Mail, LoginFailedError

SENDER_1 = "yourqqmail@qq.com"
PASS_1 = "qqmailpassword"
TO = ["jingfeng050106@gmail.com"]
QQ_CONFIG = MailConfig(
    host="smtp.qq.com", port=465, user="yourqqmail@qq.com", password="qqmailpassword"
)
html_content_test = """
<html>
  <body>
    <h1>DET</h1>
    <p style="color: green;">Keep up your streak!</p>
  </body>
</html>
"""

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DET Partnership Invitation</title>
  <style>
    /* Reset default styles */
    body {
      margin: 0;
      padding: 0;
      font-family: Arial, sans-serif;
      background-color: #f4f4f4;
    }
    .container {
      width: 100%;
      max-width: 600px;
      margin: 0 auto;
      background-color: #ffffff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .header {
      background-color: #58cc02;
      padding: 20px;
      text-align: center;
      color: #ffffff;
    }
    .header img {
      width: 50px;
      height: auto;
    }
    .content {
      padding: 20px;
      color: #333333;
    }
    .content h1 {
      font-size: 24px;
      margin: 0 0 10px;
    }
    .content p {
      font-size: 16px;
      line-height: 1.5;
      margin: 0 0 20px;
    }
    .progress {
      background-color: #e0e0e0;
      border-radius: 5px;
      padding: 15px;
    }
    .progress span {
      color: #58cc02;
      font-weight: bold;
    }
    .logo {
      background-color: white;
      border-radius: 15%;
    }
    .button {
      display: inline-block;
      padding: 12px 25px;
      background-color: #58cc02;
      color: #ffffff;
      text-decoration: none;
      border-radius: 5px;
      font-size: 16px;
    }
    .footer {
      background-color: #f4f4f4;
      padding: 10px;
      text-align: center;
      font-size: 12px;
      color: #777777;
    }
    @media only screen and (max-width: 600px) {
      .container {
        width: 100%;
      }
      .content h1 {
        font-size: 20px;
      }
      .content p {
        font-size: 14px;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img class='logo' src="https://design.duolingo.com/0ae09c1b67d1113e0ac1.svg" alt="Duolingo Logo">
      <h2>DET Partnership Invitation</h2>
    </div>
    <div class="content">
      <h1>Dear Institution X</h1>
      <p>Hi, We are the Duolingo team! And we are sincerely inviting you to be a partner with Duolingo and accept DET scores for testing your applicants' English proficiency!</p>
      <div class="progress">
        <p>The Duolingo English Test is a computer adaptive test, where the question sequence and difficulty changes for each test taker and test session. It has been accepted by <span>thousands of institutions</span> around the world!</p>
      </div>
      <p>Ready to unlock new potencial for testing your applicants' English proficiency? Click the button below to request a demo!</p>
      <a href="https://www.duolingo.com" class="button">Request a demo</a>
    </div>
    <div class="footer">
      <p>&copy; 2025 Duolingo. All rights reserved. | <a href="#">Unsubscribe</a></p>
    </div>
  </div>
</body>
</html>
"""

if __name__ == "__main__":
    mail = Mail(config=QQ_CONFIG)
    login_success = mail.login()
    mail.create_message(
        subject="Duolingo Progress Update",
        body=html_content,
        sender="3480359228@qq.com",
        receiver=["jingfeng050105@gmail.com"],
        is_html=True,
    )
    mail.send_mail()
    mail.close_connection()
