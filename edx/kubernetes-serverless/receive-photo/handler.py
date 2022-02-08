def handle(event, context):
    return {
        "statusCode": 200,
        "body": "Received {} bytes from caller".format(len(event.body))
    }
