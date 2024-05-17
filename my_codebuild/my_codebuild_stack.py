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
        app_build_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("CodeBuildAccess"))
        
        build_log_policy = iam.Policy(self,"BuildLogPolicy")
            
        artifact_bucket = s3.Bucket(self,"ArtifactBucket")
        
        # artifact_bucket_policy = s3.BucketPolicy(self, "ArtifactBucketPolicy",
        #     bucket=artifact_bucket)
        
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
        

