from steamship import File, PluginInstance
from steamship.client.operations.corpus_importer import CorpusImportRequest, CorpusImportResponse
from tests import PLUGINS_PATH
from tests.utils.client import get_steamship_client
from tests.utils.deployables import deploy_plugin

HANDLE = "test-importer-plugin-v1"
TEST_H1 = "A Poem"
TEST_S1 = "Roses are red."
TEST_S2 = "Violets are blue."
TEST_S3 = "Sugar is sweet, and I love you."
TEST_DOC = f"# {TEST_H1}\n\n{TEST_S1} {TEST_S2}\n\n{TEST_S3}\n"


def test_e2e_corpus_importer():
    client = get_steamship_client()
    corpus_importer_path = PLUGINS_PATH / "importers" / "plugin_corpus_importer.py"

    test_file_importer_instance = PluginInstance.create(
        client, plugin_handle="test-fileImporter-valueOrData", upsert=True
    ).data
    with deploy_plugin(client, corpus_importer_path, "corpusImporter") as (
        plugin,
        version,
        instance,
    ):
        corpus_id = "1"
        req = CorpusImportRequest(
            type="corpus",
            value="dummy-value",
            url=corpus_id,
            pluginInstance=instance.handle,
            fileImporterPluginInstance=test_file_importer_instance.handle,
        )
        client.post(
            "plugin/instance/importCorpus",
            req,
            expect=CorpusImportResponse,
        )

        # We should now have two files!
        files = File.list(client, corpus_id=corpus_id).data
        assert files.files is not None
        assert len(files.files) == 2

        for file in files.files:
            data = file.raw().data
            assert data.decode("utf-8") == TEST_DOC
            file.delete()