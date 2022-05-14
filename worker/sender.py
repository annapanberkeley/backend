import requests
import simplejson as json

# with open("/Users/anna.qiaoen.pan/Downloads/assignment2/worker/mailgun_config.json", 'r') as file:
with open("./mailgun_config.json", 'r') as file:
    mailgun_config = json.load(file)
    DOMAIN = mailgun_config['MAILGUN_DOMAIN']
    API_KEY = mailgun_config['MAILGUN_API_KEY']

def send_mail(id, taskName, recipient):

    message = f"Your task {id}, {taskName}, is completed!"

    requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", f"{API_KEY}"),
        data={
            "from": f"taskrabbit <mailgun@{DOMAIN}>",
            "to": [recipient],
            "subject": f"Update on task {id}",
            "text": message
        }
    )
