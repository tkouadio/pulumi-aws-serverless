import json
import pulumi
import pulumi_aws as aws
from pulumi import FileArchive, Output

# 1) DynamoDB (on-demand, parfait Free Tier)
table = aws.dynamodb.Table(
    "messages",
    attributes=[aws.dynamodb.TableAttributeArgs(name="id", type="S")],
    hash_key="id",
    billing_mode="PAY_PER_REQUEST"
)

# 2) IAM Role pour Lambda
assume_role = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
    effect="Allow",
    principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
        type="Service", identifiers=["lambda.amazonaws.com"])],
    actions=["sts:AssumeRole"]
)])
lambda_role = aws.iam.Role("lambdaRole", assume_role_policy=assume_role.json)

# Logs CloudWatch
aws.iam.RolePolicyAttachment("lambdaBasicExec",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")

# Accès DynamoDB (PutItem/Scan/GetItem)
ddb_policy = aws.iam.Policy("ddbAccessPolicy",
    policy=Output.all(table.arn).apply(lambda args: json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": ["dynamodb:PutItem", "dynamodb:Scan", "dynamodb:GetItem"],
            "Resource": args[0]
        }]
    }))
)
aws.iam.RolePolicyAttachment("ddbAccessAttach",
    role=lambda_role.name,
    policy_arn=ddb_policy.arn)

# 3) Lambda (code = dossier app/)
lambda_fn = aws.lambda_.Function(
    "apiHandler",
    role=lambda_role.arn,
    runtime="python3.11",
    handler="lambda_handler.handler",
    code=FileArchive("app"),
    environment=aws.lambda_.FunctionEnvironmentArgs(
        variables={"TABLE_NAME": table.name}
    ),
    timeout=10,
    memory_size=256,
)

# 4) API Gateway v2 (HTTP API) + intégration Lambda
api = aws.apigatewayv2.Api("httpApi", protocol_type="HTTP")

integration = aws.apigatewayv2.Integration(
    "lambdaIntegration",
    api_id=api.id,
    integration_type="AWS_PROXY",
    integration_uri=lambda_fn.arn,
    payload_format_version="2.0"
)

route_get = aws.apigatewayv2.Route(
    "getRoute",
    api_id=api.id,
    route_key="GET /",
    target=integration.id.apply(lambda i: f"integrations/{i}")
)
route_post = aws.apigatewayv2.Route(
    "postRoute",
    api_id=api.id,
    route_key="POST /",
    target=integration.id.apply(lambda i: f"integrations/{i}")
)

stage = aws.apigatewayv2.Stage(
    "prodStage",
    api_id=api.id,
    name="$default",
    auto_deploy=True
)

# 5) Permission pour que l’API invoque Lambda
invoke_perm = aws.lambda_.Permission(
    "apiInvokePermission",
    action="lambda:InvokeFunction",
    function=lambda_fn.name,
    principal="apigateway.amazonaws.com",
    source_arn=api.execution_arn.apply(lambda arn: f"{arn}/*/*")
)

# 6) Exports visibles dans les logs du pipeline
pulumi.export("endpoint_url", api.api_endpoint)
pulumi.export("table_name", table.name)