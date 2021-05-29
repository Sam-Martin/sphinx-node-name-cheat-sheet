from sphinx.parsers import RSTParser
from docutils.frontend import OptionParser
from sphinx.util.docutils import SphinxDirective, nodes
from docutils.utils import new_document


def classname(obj):
    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is not None and module != "__builtin__":
        name = module + "." + name
    return name


def recurse_children(obj, depth=0):
    tab = "\t " * depth
    result = ""
    result += f"{tab}* ``{classname(obj)}``\n"
    if obj.children:
        result += "\n".join(recurse_children(x, depth + 1) for x in obj.children)
        result += "\n"
    return result


class DisplayRSTClasses(SphinxDirective):
    has_content = True

    def run(self) -> list:
        content_string = "\n\t".join(self.content)
        classes = "\n".join(recurse_children(x) for x in self.parse_rst(self.content))
        result = ""
        result += "\n".join(self.content) + "\n"
        result += "\n\nIs rendered from:\n\n"
        result += f".. code-block ::\n\n\t{content_string}"
        result += f"\n\nWhich is composed of:\n\n"
        result += f"{classes}\n\n"

        return self.parse_rst(result)

    def parse_rst(self, text):
        parser = RSTParser()
        parser.set_application(self.env.app)

        settings = OptionParser(
            defaults=self.env.settings,
            components=(RSTParser,),
            read_config_files=True,
        ).get_default_values()
        document = new_document("<rst-doc>", settings=settings)
        parser.parse(text, document)
        return document.children


def setup(app: object) -> dict:
    app.add_directive("display-rst-classes", DisplayRSTClasses)
