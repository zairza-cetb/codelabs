import yaml
import shutil
import os
import markdown
import sys
from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
# from mdx_partial_gfm import PartialGithubFlavoredMarkdownExtension


PORT = 8000
DEST = 'dist'
ASSET_DIR = 'assets'
CONF = 'codelabs.yaml'
TEMPLATES = 'templates'


def build():
    shutil.rmtree(DEST, ignore_errors=True)

    # make sure dest exists
    os.makedirs(DEST, exist_ok=True)

    with open(CONF) as conf:
        meta = yaml.load(conf)

    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(['html', 'xml'])
    )

    md = markdown.Markdown(extensions=[
        'extra',
        #    PartialGithubFlavoredMarkdownExtension()
    ])

    for codelab in meta['codelabs']:
        render_codelab(env, md, codelab)

    build_index(env, md, meta)

    shutil.copytree(ASSET_DIR, os.path.join(DEST, ASSET_DIR))


def render_codelab(env, md, codelab):
    pass


def build_index(env, md, meta):
    with open(os.path.join(DEST, 'index.html'), 'w') as index, open('index.md') as index_md:

        homepage_html = md.convert(index_md.read())

        html = env.get_template('index.html.j2').render({
            'meta': meta,
            'homepage': homepage_html,
            'now': datetime.utcnow(),
        })
        index.write(html)

# Grabbed from: https://stackoverflow.com/a/46332163/2328165


class HTTPHandler(SimpleHTTPRequestHandler):
    """This handler uses server.base_path instead of always using os.getcwd()"""

    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.base_path, relpath)
        return fullpath


class HTTPServer(BaseHTTPServer):
    """The main server, you pass in base_path which is the path you want to serve requests from"""

    def __init__(self, base_path, server_address, RequestHandlerClass=HTTPHandler):
        self.base_path = base_path
        BaseHTTPServer.__init__(self, server_address, RequestHandlerClass)


def serve():
    httpd = HTTPServer(DEST, ("", 8000))
    print('Serving at port 8000')
    httpd.serve_forever()


def main():
    build()

    if 'serve' in sys.argv:
        serve()


if __name__ == '__main__':
    main()
