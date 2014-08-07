import SimpleHTTPServer
import SocketServer
import threading


from docker_plugin import tasks
from tests.TestCaseBase import TestCaseBase


_PORT = 8000
_HOST = 'localhost'
_IMAGE_DIR = '/tests/advanced_tests_cloudify_docker_plugin/mini.tar.xz'
_IMAGE = 'http://{}:{}{}'.format(_HOST, _PORT, _IMAGE_DIR)


def _get_request(httpd):
    httpd.handle_request()
    httpd.server_close()


class TestImageImport(TestCaseBase):
    def test_image_import(self):
        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer((_HOST, _PORT), Handler)
        request_thread = threading.Thread(target=_get_request, args=(httpd,))
        request_thread.start()
        self.ctx.properties['image_import'].update({'src': _IMAGE})
        self.ctx.properties['container_remove'].update({'remove_image': True})
        tasks.create(self.ctx)
        self.assertIsNotNone(
            self.client.inspect_image(self.ctx.runtime_properties['image'])
        )
        request_thread.join()