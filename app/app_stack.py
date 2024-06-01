from aws_cdk import Stack, aws_lambda as _lambda, aws_apigateway as apigw, Duration
from constructs import Construct


class AppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_function = _lambda.Function(
            self,
            "TestLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(10),
        )

        lambda_function2 = _lambda.Function(
            self,
            "TestLambda2",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function2.handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(10),
        )

        default_lambda = _lambda.Function(
            self,
            "DefaultFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="default_function.handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(10),
        )

        api = apigw.LambdaRestApi(
            self,
            "TestApi",
            handler=default_lambda,
            deploy_options=apigw.StageOptions(stage_name="local"),
        )

        resource1 = api.root.add_resource("test")
        resource1.add_method("GET", apigw.LambdaIntegration(lambda_function))

        resource2 = api.root.add_resource("test2")
        resource2.add_method("POST", apigw.LambdaIntegration(lambda_function2))
