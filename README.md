# Impferator

Checks availability on Doctolib, sends a notification to a slack channel.

## How to use

Create a slack app, add a new incoming webhook integration, copy the url and add it to env variables as `SLACK_WEBHOOK`.

### Dependencies:

```
requests
```

### Example usage:

```
pip3 install requests
SLACK_WEBHOOK=<url> python3 check.py
```

You can create a cronjob configuration or a simple bash loop to make it run regularly:

```
pip3 install requests
export SLACK_WEBHOOK=<url>
while true; do python3 checkall.py; sleep 60; done
```

