import aws_cdk as core
import aws_cdk.assertions as assertions

from my_codebuild.my_codebuild_stack import MyCodebuildStack

# example tests. To run these tests, uncomment this file along with the example
# resource in my_codebuild/my_codebuild_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MyCodebuildStack(app, "my-codebuild")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
