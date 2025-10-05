import json, os, time, boto3

table_name = os.environ["TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(table_name)

def respond(status, body):
    return {"statusCode": status, "headers": {"Content-Type": "application/json"},
            "body": json.dumps(body)}

def handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method","GET")

    if method == "POST":
        item = {"id": str(int(time.time())), "Message": "Hello from Pulumi + DynamoDB!"}
        table.put_item(Item=item)
        return respond(200, {"ok": True, "saved": item})

    # GET: lire 5 items (scan simplifié pour la démo)
    resp = table.scan(Limit=5)
    return respond(200, {"items": resp.get("Items", [])})