"""An Azure RM Python Pulumi program"""
import pulumi
import pulumi_azure_native as az

stack_name = pulumi.get_stack()
pulumi_config = pulumi.Config()
shared_resource_group_name = pulumi_config.require("shared_resources_group_name")
shared_container_app_environment_id = pulumi_config.require(
    "shared_container_app_environment_id"
)


resource_group = az.resources.ResourceGroup(f"{stack_name}-app-resources")

container_app = az.app.ContainerApp(
    f"{stack_name}-app",
    resource_group_name=resource_group.name,
    managed_environment_id=shared_container_app_environment_id,
    configuration=az.app.ConfigurationArgs(
        ingress=az.app.IngressArgs(external=True, target_port=80),
    ),
    template=az.app.TemplateArgs(
        containers=[
            az.app.ContainerArgs(
                name="myapp",
                image="mcr.microsoft.com/k8se/quickstart:latest",
            )
        ]
    ),
)


pulumi.export("app fqdn", container_app.latest_revision_fqdn)
