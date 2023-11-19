"""An Azure RM Python Pulumi program"""

import pulumi
import pulumi_azure_native as az

stack_name = pulumi.get_stack()

resource_group = az.resources.ResourceGroup(f"{stack_name}-resources")

logs_workspace = az.operationalinsights.Workspace(
    f"{stack_name}-logs",
    resource_group_name=resource_group.name,
    sku=az.operationalinsights.WorkspaceSkuArgs(name="PerGB2018"),
    retention_in_days=30,
)

logs_workspace_key = pulumi.Output.all(resource_group.name, logs_workspace.name).apply(
    lambda args: az.operationalinsights.get_shared_keys(
        resource_group_name=args[0], workspace_name=args[1]
    ).primary_shared_key
)

# Create a shared Container Apps Environment
container_app_environment = az.app.ManagedEnvironment(
    f"{stack_name}-cae",
    resource_group_name=resource_group.name,
    app_logs_configuration=az.app.AppLogsConfigurationArgs(
        destination="log-analytics",
        log_analytics_configuration=az.app.LogAnalyticsConfigurationArgs(
            customer_id=logs_workspace.customer_id,
            shared_key=logs_workspace_key,
        ),
    ),
)


pulumi.export("shared resources group name", resource_group.name)
pulumi.export("shared container app environment id", container_app_environment.id)
