from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_codecommit as CodeCommit,
    aws_codebuild as CodeBuild,
    aws_s3 as s3,
    aws_iam as iam
)
from constructs import Construct

class MyCodebuildStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repo = CodeCommit.Repository(self, "Repository",
            repository_name= "java-project",
            description="The repository",
            code=CodeCommit.Code.from_zip_file("java-project.zip", "main"))
        
        
        app_build_role = iam.Role(self,"AppBuildRole",assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"))
        # app_build_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("CodeBuildAccess"))
        
        policy_document = iam.PolicyDocument(statements=[iam.PolicyStatement(
            resources=["*"],
            actions=["logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"]
            )])
        
        build_log_policy = iam.Policy(self,"BuildLogPolicy",
            document=policy_document)
        
        
        bucket_policy_statement = iam.PolicyStatement(
            resources=["*"],
            actions=["s3:PutObject"],
            effect=iam.Effect.DENY)
        
        bucket_policy_statement.add_any_principal()
            
        artifact_bucket = s3.Bucket(self,"ArtifactBucket")
        artifact_bucket.add_to_resource_policy(bucket_policy_statement)
        

        project = CodeBuild.Project(self,"AppBuildProject",
            artifacts=CodeBuild.Artifacts.s3(
                bucket=artifact_bucket,
                package_zip=True),
            source=CodeBuild.Source.code_commit(
                repository=repo,
                branch_or_ref="main"
            ),
            environment=CodeBuild.BuildEnvironment(
                privileged=True
            ),
            role=app_build_role
        )
        

