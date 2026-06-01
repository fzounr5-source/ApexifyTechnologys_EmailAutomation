import tkinter as tk
from tkinter import messagebox, scrolledtext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

def send_all_emails():
    # get all input values from GUI
    gmail_user = email_entry.get()
    app_pass = password_entry.get()
    mail_subject = subject_entry.get()
    mail_body = message_text.get("1.0", tk.END).strip()
    
    # split emails by line and remove empty lines
    email_list_raw = emails_text.get("1.0", tk.END).strip()
    all_emails = []
    for e in email_list_raw.split("\n"):
        if e.strip():
            all_emails.append(e.strip())
    
    if not gmail_user or not app_pass or not mail_subject or not mail_body or not all_emails:
        messagebox.showerror("Missing Info", "Please fill all fields")
        return
    
    log_text.delete("1.0", tk.END)
    log_text.insert(tk.END, f"Found {len(all_emails)} emails. Starting...\n\n")
    log_text.update()
    
    try:
        # connect to gmail
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login(gmail_user, app_pass)
        
        sent_count = 0
        fail_count = 0
        
        # send to each email one by one
        for single_email in all_emails:
            try:
                email_msg = MIMEMultipart()
                email_msg["From"] = gmail_user
                email_msg["To"] = single_email
                email_msg["Subject"] = mail_subject
                email_msg.attach(MIMEText(mail_body, "plain"))
                
                smtp_server.sendmail(gmail_user, single_email, email_msg.as_string())
                log_text.insert(tk.END, f"Sent -> {single_email}\n")
                sent_count = sent_count + 1
                
                # wait 2 sec so gmail doesn't block us
                time.sleep(2)
                log_text.see(tk.END)  # auto scroll
                log_text.update()
                
            except Exception as err:
                log_text.insert(tk.END, f"Error -> {single_email} : {str(err)}\n")
                fail_count = fail_count + 1
                log_text.update()
        
        smtp_server.quit()
        
        log_text.insert(tk.END, f"\n--- Finished ---\n")
        log_text.insert(tk.END, f"Total Sent: {sent_count}\n")
        log_text.insert(tk.END, f"Total Failed: {fail_count}\n")
        
        messagebox.showinfo("Complete", f"Done! Sent: {sent_count}, Failed: {fail_count}")
        
    except Exception as error:
        messagebox.showerror("Login Error", f"Could not connect: {str(error)}")

# main window
window = tk.Tk()
window.title("Bulk Email Sender")
window.geometry("600x700")

tk.Label(window, text="Gmail Address:").pack(anchor="w", padx=10, pady=(10,0))
email_entry = tk.Entry(window, width=70)
email_entry.pack(padx=10)

tk.Label(window, text="App Password:").pack(anchor="w", padx=10, pady=(10,0))
password_entry = tk.Entry(window, width=70, show="*")
password_entry.pack(padx=10)

tk.Label(window, text="Email Subject:").pack(anchor="w", padx=10, pady=(10,0))
subject_entry = tk.Entry(window, width=70)
subject_entry.pack(padx=10)

tk.Label(window, text="Email Message:").pack(anchor="w", padx=10, pady=(10,0))
message_text = scrolledtext.ScrolledText(window, width=70, height=8)
message_text.pack(padx=10)

tk.Label(window, text="Recipient Emails - one per line:").pack(anchor="w", padx=10, pady=(10,0))
emails_text = scrolledtext.ScrolledText(window, width=70, height=10)
emails_text.pack(padx=10)

send_btn = tk.Button(window, text="Start Sending", command=send_all_emails, bg="#2E8B57", fg="white", font=("Arial", 12))
send_btn.pack(pady=15)

tk.Label(window, text="Status Log:").pack(anchor="w", padx=10)
log_text = scrolledtext.ScrolledText(window, width=70, height=10)
log_text.pack(padx=10, pady=5)

window.mainloop()
