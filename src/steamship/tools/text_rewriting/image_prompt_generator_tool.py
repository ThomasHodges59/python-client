from steamship.agents.debugging import ToolREPL
from steamship.tools.text_rewriting.text_rewriting_tool import TextRewritingTool

DEFAULT_PROMPT = """Instructions:
Please rewrite the following passage to create an excellent prompt for use with DALL-E or Stable Diffusion. Add
keywords that improve the drama and style to create dramatic, photographic effects.

Passage:
{input}

Image Generation Prompt:"""


class ImagePromptGenerator(TextRewritingTool):
    """
    Example tool to illustrate rewriting an input query to become a better prompt.
    """

    name: str = "ImagePromptGenerator"
    human_description: str = "Improves a prompt for use with image generation."
    ai_description: str = (
        "Use this tool to improve a prompt for stable diffusion and other image and video generators. "
        "This tool will refine your prompt to include key words and phrases that make "
        "stable diffusion and other art generation algorithms perform better. The input is a prompt text string "
        "and the output is a prompt text string"
    )
    rewrite_prompt: str = DEFAULT_PROMPT


if __name__ == "__main__":
    ToolREPL(ImagePromptGenerator()).run()
