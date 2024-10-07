import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os

# Job Application Form
def main():
    st.title("Job Application Form")

    st.write("Please fill out the form below to apply for the job. Don't forget to upload your CV!")

    # Form to collect user details
    with st.form("job_application_form"):
        # Collect basic information
        full_name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        position = st.selectbox("Position Applying For", ["Software Engineer", "Data Scientist", "Product Manager", "Designer", "Other"])

        # Add more fields as needed
        cover_letter = st.text_area("Cover Letter (Optional)")
        
        # File uploader for CV
        cv_file = st.file_uploader("Upload your CV", type=["pdf", "doc", "docx"])

        # Submit button
        submit_button = st.form_submit_button("Submit Application")

        # Process the submitted data
        if submit_button:
            if full_name and email and phone and position and cv_file:
                # Save form data (for demo purposes, we'll display it)
                application_data = {
                    "Full Name": full_name,
                    "Email": email,
                    "Phone": phone,
                    "Position": position,
                    "Cover Letter": cover_letter,
                    "CV Filename": cv_file.name,
                    "Application Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # Convert data to DataFrame for display
                df = pd.DataFrame([application_data])

                # Display confirmation and form data
                st.success(f"Thank you, {full_name}, for applying for the {position} position!")
                st.write("We have received your application. Here’s a summary of your details:")
                st.dataframe(df)

                # Send email with CV attached
                send_email_with_attachment(full_name, email, phone, position, cover_letter, cv_file)

                st.success("Your CV has been sent to the HR team.")

            else:
                st.error("Please fill out all the required fields and upload your CV.")


def send_email_with_attachment(full_name, email, phone, position, cover_letter, cv_file):
    # Email configuration
    from_address = "rdxkeerthi@gmail.com"
    to_address = "ipsqsofttech@gmail.com"
    subject = f"Job Application from {full_name} for {position}"
    password = "dyng vpzp prfm tgui"  # Use app-specific password if using Gmail

    # Create message object
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    # Body of the email
    body = f"""
    Name: {full_name}
    Email: {email}
    Phone: {phone}
    Position: {position}
    Cover Letter: {cover_letter}
    """
    msg.attach(MIMEText(body, 'plain'))

    # Attach the CV file
    cv_file_name = cv_file.name
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(cv_file.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename= {cv_file_name}')
    msg.attach(attachment)

    # Send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, password)
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        st.info("Email sent successfully.")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

if __name__ == '__main__':
    main()
