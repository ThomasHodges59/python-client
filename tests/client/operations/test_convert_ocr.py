# from os import path
#
# from steamship import MimeTypes
#
# from .helpers import _random_name, _steamship
#
# __copyright__ = "Steamship"
# __license__ = "MIT"
#
#
# def test_image_upload():
#     steamship = _steamship()
#     test_filename = path.join(
#         path.dirname(path.realpath(__file__)),
#         'test_img.png'
#     )
#     with open(test_filename, "rb") as f:
#         name_c = "{}.png".format(_random_name())
#         c = steamship.upload(
#             name=name_c,
#             content=f
#         ).data
#         assert (c.id is not None)
#         assert (c.name == name_c)
#         assert (c.mimeType == MimeTypes.PNG)
#
#         blockifyResp = c.blockify(plugin="ocr_ms_vision_default")
#         assert (blockifyResp.error is None)
#         blockifyResp.wait()
#         assert (blockifyResp.data is not None)
#
#         q1 = c.query().data
#         assert (len(q1.blocks) == 3)
#
#         c.delete()