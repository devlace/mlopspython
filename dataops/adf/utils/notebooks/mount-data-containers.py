# Databricks Notebook mounting blob storage containers (input,training,testing)

storage_account_name = getArgument("storage_account_name")  # noqa: F821
storage_account_key = getArgument("storage_account_key")  # noqa: F821

input_container_name = getArgument("input_container_name")  # noqa: F821
input_mount_point_name = getArgument("input_mount_point_name")  # noqa: F821
training_container_name = getArgument("training_container_name")  # noqa: F821
training_mount_point_name = getArgument("training_mount_point_name")  # noqa: F821, E501
testing_container_name = getArgument("testing_container_name")  # noqa: F821
testing_mount_point_name = getArgument("testing_mount_point_name")  # noqa: F821, E501


def mount_storage(container_name, mount_point_name):
    if not any(mount.mountPoint == mount_point_name for mount in dbutils.fs.mounts()):  # noqa: F821, E501
        dbutils.fs.mount(  # noqa: F821
            source="wasbs://" + container_name + "@" +
            storage_account_name + ".blob.core.windows.net",
            mount_point=mount_point_name,
            extra_configs={"fs.azure.account.key." + storage_account_name + ".blob.core.windows.net": storage_account_key})  # noqa: E501


mount_storage(input_container_name, input_mount_point_name)
mount_storage(training_container_name, training_mount_point_name)
mount_storage(testing_container_name, testing_mount_point_name)
