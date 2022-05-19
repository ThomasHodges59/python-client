from tests import PLUGINS_PATH
from tests.utils.client import get_steamship_client
from tests.utils.deployables import deploy_plugin
from tests.utils.file import upload_file


def test_e2e_csv_blockifier_plugin():
    client = get_steamship_client()
    csv_blockifier_plugin_path = PLUGINS_PATH / "blockifiers" / "csv_blockifier.py"

    version_config_template = dict(
        text_column=dict(type="string"),
        tag_columns=dict(type="string"),
        tag_kind=dict(type="string"),
    )  # TODO (enias): Derive this from Config
    instance_config = dict(  # Has to match up
        text_column="Message",
        tag_columns="Category",
        tag_kind="Intent",
    )
    with deploy_plugin(
        client,
        csv_blockifier_plugin_path,
        "blockifier",
        version_config_template=version_config_template,
        instance_config=instance_config,
    ) as (plugin, version, instance):
        with upload_file(client, "utterances.csv") as file:
            assert len(file.refresh().data.blocks) == 0
            file.blockify(plugin_instance=instance.handle).wait()
            # Check the number of blocks
            blocks = file.refresh().data.blocks
            assert len(blocks) == 5
            for block in blocks:
                assert block.tags is not None
                assert len(block.tags) > 0
                for tag in block.tags:
                    assert tag.name is not None
                    assert tag.kind is not None
            file.delete()