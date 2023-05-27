import time
import requests
import shutil
import signal
import sys

GREEN = "\033[92m"
RESET = "\033[0m"

DEFAULT_USERNAME = "carbon"

def send_webhook_message(url, username, message):
    data = {"content": message, "username": username}
    response = requests.post(url, json=data)
    return response.status_code == 204

def select_option(options):
    while True:
        choice = input("Enter your choice: ")
        if choice.isdigit() and int(choice) in range(1, len(options) + 1):
            return int(choice)
        print(f"{GREEN}Invalid choice. Please try again.{RESET}")

def print_error_message(message):
    print(f"{GREEN}Error: {message}{RESET}")

def print_success_message(message):
    print(f"{GREEN}{message}{RESET}")

def print_title(title):
    terminal_width = shutil.get_terminal_size().columns
    title_length = len(title)
    padding = (terminal_width - title_length) // 2
    print(f"{GREEN}{padding * ' '}{title}{RESET}")
    print("-" * terminal_width)

def save_configuration(webhooks, usernames):
    with open("config.txt", "w") as file:
        for webhook, username in zip(webhooks, usernames):
            file.write(f"{webhook},{username}\n")
    print_success_message("\nWebhook configuration saved successfully.")

def load_configuration():
    webhooks = []
    usernames = []
    try:
        with open("config.txt", "r") as file:
            for line in file:
                webhook, username = line.strip().split(",")
                webhooks.append(webhook)
                usernames.append(username)
        print_success_message("\nWebhook configuration loaded successfully.")
    except FileNotFoundError:
        print_error_message("\nConfiguration file not found.")
    return webhooks, usernames

def delete_webhook(webhooks, usernames):
    if not webhooks:
        print_error_message("\nNo webhooks added. Please add a webhook first.")
        return

    print_title("Delete Webhook")
    print("Available Webhooks:")
    for i, webhook in enumerate(webhooks, start=1):
        print(f"{GREEN}{i}. {webhook}{RESET}")

    webhook_index = select_option(range(1, len(webhooks) + 1)) - 1
    deleted_webhook = webhooks.pop(webhook_index)
    deleted_username = usernames.pop(webhook_index)
    print_success_message(f"\nWebhook {deleted_webhook} deleted successfully.")

def edit_webhook_configuration(webhooks, usernames):
    if not webhooks:
        print_error_message("\nNo webhooks added. Please add a webhook first.")
        return

    print_title("Edit Webhook Configuration")
    print("Available Webhooks:")
    for i, webhook in enumerate(webhooks, start=1):
        print(f"{GREEN}{i}. {webhook}{RESET}")

    webhook_index = select_option(range(1, len(webhooks) + 1)) - 1
    new_username = input("Enter the new username for the selected webhook: ")
    webhooks[webhook_index] = input("Enter the new webhook URL: ")
    usernames[webhook_index] = new_username
    print_success_message("\nWebhook configuration updated successfully.")

def view_webhook_configuration(webhooks, usernames):
    if not webhooks:
        print_error_message("\nNo webhooks added. Please add a webhook first.")
        return

    print_title("Webhook Configuration")
    for webhook, username in zip(webhooks, usernames):
        print(f"{GREEN}Webhook: {webhook}")
        print(f"Username: {username}{RESET}")
        print("-" * shutil.get_terminal_size().columns)

def signal_handler(signal, frame):
    print_success_message("\nSaving webhook configuration...")
    save_configuration(webhooks, usernames)
    sys.exit(0)

def main():
    webhooks, usernames = load_configuration()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        print_title("Discord Webhook Manager")
        print("1. Add Webhook")
        print("2. Edit Webhook Configuration")
        print("3. View Webhook Configuration")
        print("4. Delete Webhook")
        print("5. Send Messages")
        print("6. Exit")

        choice = select_option(range(1, 7))

        if choice == 1:
            print_title("Add Webhook")
            num_webhooks = int(input("Enter the number of webhooks you want to add: "))
            for _ in range(num_webhooks):
                webhooks.append(input("\nEnter the Discord webhook URL: "))
                usernames.append(DEFAULT_USERNAME)
            print_success_message("\nWebhooks added successfully.")

        elif choice == 2:
            edit_webhook_configuration(webhooks, usernames)

        elif choice == 3:
            view_webhook_configuration(webhooks, usernames)

        elif choice == 4:
            delete_webhook(webhooks, usernames)

        elif choice == 5:
            if not webhooks:
                print_error_message("\nNo webhooks added. Please add a webhook first.")
                continue

            print_title("Send Messages")
            message = input("Enter the message you want to send: ")
            times = int(input("Enter the number of times you want to send the message: "))

            for i in range(times):
                for webhook, username in zip(webhooks, usernames):
                    result = send_webhook_message(webhook, username, message)
                    if result:
                        print_success_message(f"\nMessage sent successfully using webhook {webhook} as {username}.")
                    else:
                        print_error_message(f"\nFailed to send message using webhook {webhook} as {username}.")
                    time.sleep(0.5)

        elif choice == 6:
            save_configuration(webhooks, usernames)

if __name__ == "__main__":
    main()
