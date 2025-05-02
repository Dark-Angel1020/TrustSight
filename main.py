import csv
import os
import time
import webbrowser
from prettytable import PrettyTable
from dotenv import load_dotenv
import cert
import checkchange
import alertmailer

load_dotenv()
SMTP_SENDER = os.getenv("SMTP_SENDER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SNAPSHOT_FOLDER = 'html_snapshots'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    print("""

████████╗██████╗ ██╗   ██╗███████╗████████╗███████╗██╗ ██████╗ ██╗  ██╗████████╗
╚══██╔══╝██╔══██╗██║   ██║██╔════╝╚══██╔══╝██╔════╝██║██╔════╝ ██║  ██║╚══██╔══╝
   ██║   ██████╔╝██║   ██║███████╗   ██║   ███████╗██║██║  ███╗███████║   ██║   
   ██║   ██╔══██╗██║   ██║╚════██║   ██║   ╚════██║██║██║   ██║██╔══██║   ██║   
   ██║   ██║  ██║╚██████╔╝███████║   ██║   ███████║██║╚██████╔╝██║  ██║   ██║   
   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
""")
    print("Website Monitoring System".center(50))
    print("="*50)

def certificate_validation():
    clear_screen()
    print("\n🔐 Certificate Validation Module")
    print("="*50)
    
    websites = []
    with open('websites.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            websites.append({
                'si_number': row['si number'],
                'url': row['website address'],
                'email': row['email']
            })
    results = []
    table = PrettyTable()
    table.field_names = ["SI No", "Website", "Status", "From", "To", "Days Remaining", "Issuer"]
    table.align = "l"
    
    for site in websites:
        print(f"\n🔍 Checking certificate for: {site['url']}")
        cert_info = cert.get_certificate_details(site['url'])
        
        results.append({
            'si_number': site['si_number'],
            'url': site['url'],
            'status': cert_info['status'],
            'from': cert_info['not_before'],
            'to': cert_info['not_after'],
            'days_remaining': cert_info['days_remaining'],
            'issuer': cert_info['issuer'],
            'email': site['email']
        })
        
        table.add_row([
            site['si_number'],
            site['url'],
            cert_info['status'],
            cert_info['not_before'],
            cert_info['not_after'],
            cert_info['days_remaining'],
            cert_info['issuer']
        ])
    
    print("\n" + "="*50)
    print("SSL Certificate Validation Results")
    print("="*50)
    print(table)
    

    expiring_sites = [site for site in results if isinstance(site['days_remaining'], int) and site['days_remaining'] < 90]
    
    if expiring_sites:
        print("\n⚠️  Alert: The following certificates are expiring soon (less than 90 days):")
        for site in expiring_sites:
            print(f" - {site['url']} (Expires in {site['days_remaining']} days)")
        
        while True:
            print("\nOptions:")
            print("1. Send alerts for all expiring certificates")
            print("2. Select which certificates to alert")
            print("3. Don't send any alerts (return to main menu)")
            
            choice = input("\nEnter your choice (1/2/3): ")
            
            if choice == '1':
                for site in expiring_sites:
                    subject = f"Alert: SSL Certificate Expiring Soon - {site['url']}"
                    body = f"""
Hello,

The SSL certificate for {site['url']} is expiring soon.
Expiration Date: {site['to']}
Days Remaining: {site['days_remaining']}

Please renew the certificate as soon as possible.

Best Regards,
Your Monitoring System
"""
                    if alertmailer.send_alert(
                        receiver_email=site['email'],
                        subject=subject,
                        body=body,
                        sender_email=SMTP_SENDER,
                        sender_password=SMTP_PASSWORD
                    ):
                        print(f"✓ Alert sent for {site['url']} to {site['email']}")
                    else:
                        print(f"✗ Failed to send alert for {site['url']}")
                break
            
            elif choice == '2':
                for site in expiring_sites:
                    send_alert = input(f"Send alert for {site['url']}? (y/n): ").lower()
                    if send_alert == 'y':
                        subject = f"Alert: SSL Certificate Expiring Soon - {site['url']}"
                        body = f"""
Hello,

The SSL certificate for {site['url']} is expiring soon.
Expiration Date: {site['to']}
Days Remaining: {site['days_remaining']}

Please renew the certificate as soon as possible.

Best Regards,
Your Monitoring System
"""
                        if alertmailer.send_alert(
                            receiver_email=site['email'],
                            subject=subject,
                            body=body,
                            sender_email=SMTP_SENDER,
                            sender_password=SMTP_PASSWORD
                        ):
                            print(f"✓ Alert sent for {site['url']} to {site['email']}")
                        else:
                            print(f"✗ Failed to send alert for {site['url']}")
                break
            
            elif choice == '3':
                break
            
            else:
                print("Invalid choice. Please try again.")
    else:
        print("\n✅ All certificates are valid with more than 90 days remaining.")
        input("\nPress Enter to return to main menu...")

def defacement_checker():
    clear_screen()
    print("\n🛡️ Website Defacement Checker")
    print("="*50)
    
    print("\n🔍 Checking websites for changes...")
    changed_sites = checkchange.check_websites()
    
    if changed_sites:
        print("\n🚨 Changes Detected on the Following Sites:")
        for i, site in enumerate(changed_sites, 1):
            status = "DEFACEMENT DETECTED" if site['defaced'] else "Content Changed"
            print(f"{i}. {site['url']} - {status}")
        
        while True:
            print("\nOptions:")
            print("1. Send alerts for all changed sites")
            print("2. Select which sites to alert")
            print("3. Verify and update specific sites")
            print("4. Return to main menu")
            
            choice = input("\nEnter your choice (1/2/3/4): ")
            
            if choice == '1':
                for site in changed_sites:
                    if site['defaced']:
                        subject = f"URGENT: Defacement Detected - {site['url']}"
                        body = f"""
URGENT ALERT,

Potential website defacement has been detected on: {site['url']}

The content of the website contains suspicious keywords that may indicate a defacement attack.

Please verify the website immediately and take appropriate action.

Best Regards,
Your Monitoring System
"""
                    else:
                        subject = f"Alert: Content Change Detected - {site['url']}"
                        body = f"""
Alert,

A content change has been detected on: {site['url']}

Please verify if this change was intentional.

Best Regards,
Your Monitoring System
"""
                    if alertmailer.send_alert(
                        receiver_email=site['email'],
                        subject=subject,
                        body=body,
                        sender_email=SMTP_SENDER,
                        sender_password=SMTP_PASSWORD
                    ):
                        print(f"✓ Alert sent for {site['url']} to {site['email']}")
                    else:
                        print(f"✗ Failed to send alert for {site['url']}")
                
                hashes = checkchange.load_hashes()
                for site in changed_sites:
                    hashes[site['url']] = site['new_hash']
                    checkchange.save_cleaned_html(site['domain'], site['html'])
                checkchange.save_hashes(hashes)
                print("\n[✓] Updated hashes for all changed sites")
                break
            
            elif choice == '2':
                for site in changed_sites:
                    send_alert = input(f"Send alert for {site['url']}? (y/n): ").lower()
                    if send_alert == 'y':
                        if site['defaced']:
                            subject = f"URGENT: Defacement Detected - {site['url']}"
                            body = f"""
URGENT ALERT,

Potential website defacement has been detected on: {site['url']}

The content of the website contains suspicious keywords that may indicate a defacement attack.

Please verify the website immediately and take appropriate action.

Best Regards,
Your Monitoring System
"""
                        else:
                            subject = f"Alert: Content Change Detected - {site['url']}"
                            body = f"""
Alert,

A content change has been detected on: {site['url']}

Please verify if this change was intentional.

Best Regards,
Your Monitoring System
"""
                        if alertmailer.send_alert(
                            receiver_email=site['email'],
                            subject=subject,
                            body=body,
                            sender_email=SMTP_SENDER,
                            sender_password=SMTP_PASSWORD
                        ):
                            print(f"✓ Alert sent for {site['url']} to {site['email']}")
                        else:
                            print(f"✗ Failed to send alert for {site['url']}")
                
                # After selective alerts, ask if they want to update hashes
                update_all = input("\nUpdate hashes for all changed sites? (y/n): ").lower()
                if update_all == 'y':
                    hashes = checkchange.load_hashes()
                    for site in changed_sites:
                        hashes[site['url']] = site['new_hash']
                        checkchange.save_cleaned_html(site['domain'], site['html'])
                    checkchange.save_hashes(hashes)
                    print("\n[✓] Updated hashes for all changed sites")
                break
            
            elif choice == '3':
                for site in changed_sites[:]:  # Create a copy for iteration
                    print(f"\nSite: {site['url']}")
                    print(f"Status: {'DEFACEMENT DETECTED' if site['defaced'] else 'Content Changed'}")
                    
                    while True:
                        print("\nOptions:")
                        print("1. Open site in browser")
                        print("2. Verify and update hash (mark as no change)")
                        print("3. Skip this site")
                        
                        sub_choice = input("Enter your choice (1/2/3): ")
                        
                        if sub_choice == '1':
                            print(f"Opening {site['url']} in browser...")
                            webbrowser.open(site['url'])
                            input("Press Enter after verification...")
                        
                        elif sub_choice == '2':
                            # Update the hash
                            hashes = checkchange.load_hashes()
                            hashes[site['url']] = site['new_hash']
                            checkchange.save_hashes(hashes)
                            checkchange.save_cleaned_html(site['domain'], site['html'])
                            print(f"✓ Updated hash for {site['url']}")
                            changed_sites.remove(site)  # Remove from changed list
                            break
                        
                        elif sub_choice == '3':
                            break
                        
                        else:
                            print("Invalid choice. Please try again.")
                
                if not changed_sites:
                    print("\n✅ All changes have been verified.")
                    break
            
            elif choice == '4':
                break
            
            else:
                print("Invalid choice. Please try again.")
    else:
        print("\n✅ No changes detected on any monitored websites.")
        input("\nPress Enter to return to main menu...")
    clear_screen()
    print("\n🛡️ Website Defacement Checker")
    print("="*50)
    
    print("\n🔍 Checking websites for changes...")
    changed_sites = checkchange.check_websites()
    
    if changed_sites:
        print("\n🚨 Changes Detected on the Following Sites:")
        for i, site in enumerate(changed_sites, 1):
            status = "DEFACEMENT DETECTED" if site['defaced'] else "Content Changed"
            print(f"{i}. {site['url']} - {status}")
        
        while True:
            print("\nOptions:")
            print("1. Send alerts for all changed sites")
            print("2. Select which sites to alert")
            print("3. Verify and update specific sites")
            print("4. Return to main menu")
            
            choice = input("\nEnter your choice (1/2/3/4): ")
            
            if choice == '1':
                for site in changed_sites:
                    if site['defaced']:
                        subject = f"URGENT: Defacement Detected - {site['url']}"
                        body = f"""
URGENT ALERT,

Potential website defacement has been detected on: {site['url']}

The content of the website contains suspicious keywords that may indicate a defacement attack.

Please verify the website immediately and take appropriate action.

Best Regards,
Your Monitoring System
"""
                    else:
                        subject = f"Alert: Content Change Detected - {site['url']}"
                        body = f"""
Alert,

A content change has been detected on: {site['url']}

Please verify if this change was intentional.

Best Regards,
Your Monitoring System
"""
                    if alertmailer.send_alert(
                        receiver_email=site['email'],
                        subject=subject,
                        body=body,
                        sender_email=SMTP_SENDER,
                        sender_password=SMTP_PASSWORD
                    ):
                        print(f"✓ Alert sent for {site['url']} to {site['email']}")
                    else:
                        print(f"✗ Failed to send alert for {site['url']}")
                break
            
            elif choice == '2':
                for site in changed_sites:
                    send_alert = input(f"Send alert for {site['url']}? (y/n): ").lower()
                    if send_alert == 'y':
                        if site['defaced']:
                            subject = f"URGENT: Defacement Detected - {site['url']}"
                            body = f"""
URGENT ALERT,

Potential website defacement has been detected on: {site['url']}

The content of the website contains suspicious keywords that may indicate a defacement attack.

Please verify the website immediately and take appropriate action.

Best Regards,
Your Monitoring System
"""
                        else:
                            subject = f"Alert: Content Change Detected - {site['url']}"
                            body = f"""
Alert,

A content change has been detected on: {site['url']}

Please verify if this change was intentional.

Best Regards,
Your Monitoring System
"""
                        if alertmailer.send_alert(
                            receiver_email=site['email'],
                            subject=subject,
                            body=body,
                            sender_email=SMTP_SENDER,
                            sender_password=SMTP_PASSWORD
                        ):
                            print(f"✓ Alert sent for {site['url']} to {site['email']}")
                        else:
                            print(f"✗ Failed to send alert for {site['url']}")
                break
            
            elif choice == '3':
                for site in changed_sites[:]:
                    print(f"\nSite: {site['url']}")
                    print(f"Status: {'DEFACEMENT DETECTED' if site['defaced'] else 'Content Changed'}")
                    
                    while True:
                        print("\nOptions:")
                        print("1. Open site in browser")
                        print("2. Verify and update hash (mark as no change)")
                        print("3. Skip this site")
                        
                        sub_choice = input("Enter your choice (1/2/3): ")
                        
                        if sub_choice == '1':
                            print(f"Opening {site['url']} in browser...")
                            webbrowser.open(site['url'])
                            input("Press Enter after verification...")
                        
                        elif sub_choice == '2':
                            # Update the hash
                            hashes = checkchange.load_hashes()
                            hashes[site['url']] = site['new_hash']
                            checkchange.save_hashes(hashes)
                            checkchange.save_cleaned_html(site['domain'], site['html'])
                            print(f"✓ Updated hash for {site['url']}")
                            changed_sites.remove(site)
                            break
                        
                        elif sub_choice == '3':
                            break
                        
                        else:
                            print("Invalid choice. Please try again.")
                
                if not changed_sites:
                    print("\n✅ All changes have been verified.")
                    break
            
            elif choice == '4':
                break
            
            else:
                print("Invalid choice. Please try again.")
    else:
        print("\n✅ No changes detected on any monitored websites.")
        input("\nPress Enter to return to main menu...")

def main_menu():
    while True:
        clear_screen()
        display_banner()
        print("\nMain Menu:")
        print("1. Certificate Validation")
        print("2. Defacement Checker")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1/2/3): ")
        
        if choice == '1':
            certificate_validation()
        elif choice == '2':
            defacement_checker()
        elif choice == '3':
            print("\nThank you for using the Website Monitoring System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    # Create necessary folders if they don't exist
    os.makedirs(SNAPSHOT_FOLDER, exist_ok=True)
    main_menu()