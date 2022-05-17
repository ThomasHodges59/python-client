import pytest

from steamship.app.response import Response
from steamship.data.block import Block
from steamship.extension.file import File
from steamship.plugin.inputs.block_and_tag_plugin_input import BlockAndTagPluginInput
from steamship.plugin.inputs.train_plugin_input import TrainPluginInput
from steamship.plugin.inputs.training_parameter_plugin_input import TrainingParameterPluginInput
from steamship.plugin.outputs.block_and_tag_plugin_output import BlockAndTagPluginOutput
from steamship.plugin.service import PluginRequest
from tests.demo_apps.plugins.taggers.plugin_parser import TestParserPlugin

TEST_REQ = BlockAndTagPluginInput(
    file=File(
        blocks=[
            Block(
                id="ABC",
                text="Once upon a time there was a magical ship. "
                     "The ship was powered by STEAM. The ship went to the moon.",
            )
        ]
    )
)
TEST_PLUGIN_REQ = PluginRequest(data=TEST_REQ)
TEST_PLUGIN_REQ_DICT = TEST_PLUGIN_REQ.to_dict()


def _test_resp(res):
    assert type(res) == Response
    assert type(res.data) == BlockAndTagPluginOutput
    assert len(res.data.file.blocks) == 1
    assert res.data.file.blocks[0].text == TEST_REQ.file.blocks[0].text
    assert len(res.data.file.blocks[0].tags) == 3


def test_parser():
    parser = TestParserPlugin()
    res = parser.run(TEST_PLUGIN_REQ)
    _test_resp(res)

    # The endpoints take a kwargs block which is transformed into the appropriate JSON object
    res2 = parser.run_endpoint(**TEST_PLUGIN_REQ_DICT)
    _test_resp(res2)

    # This plugin is not trainable, and thus it refuses trainable parameters requests
    with pytest.raises(Exception):
        parser.get_training_parameters(PluginRequest(data=TrainingParameterPluginInput()))
    with pytest.raises(Exception):
        parser.get_training_parameters_endpoint(**PluginRequest(data=TrainingParameterPluginInput()).to_dict())

    # This plugin is not trainable, and thus it refuses train requests
    with pytest.raises(Exception):
        parser.train(PluginRequest(data=TrainPluginInput()))
    with pytest.raises(Exception):
        parser.train_endpoint(**PluginRequest(data=TrainPluginInput()).to_dict())