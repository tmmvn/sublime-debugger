from ..typecheck import *

import sublime

from .. import core
from .component import Component, Inline
from .layout import Layout
from .size import HEIGHT, WIDTH

def _image_to_data(path: str) -> bytes:
	p = '{}/../{}'.format(sublime.packages_path(), path)
	f = open(p, 'rb')
	r = f.read()
	f.close()
	return r


def _b64_data_from_image_data(png_data: bytes) -> str:
	import base64
	return "data:image/png;base64,{}".format(base64.b64encode(png_data).decode('ascii'))


def view_background_lightness(view: sublime.View) -> float:
	style = view.style()
	if "background" not in style:
		return 0

	color = style["background"].lstrip('#')
	rgb = tuple(int(color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
	lum = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
	return lum

def reload_images():
	Image.cached = {}
	Images.shared = Images()

class Image:
	cached = {} #type: Dict[str, str]

	@staticmethod
	def named(name: str) -> 'Image':
		path = _path_for_image(name)
		return Image(path, path)

	@staticmethod
	def named_light_dark(name: str) -> 'Image':
		light = _path_for_image("light/" + name)
		dark = _path_for_image("dark/" + name)
		return Image(dark, light)

	def __init__(self, file_dark: str, file_light: str) -> None:
		self.file = file_light
		self.file_light = file_light
		self.file_dark = file_dark

	def data(self, layout: Layout) -> str:
		if layout.luminocity() < 0.5:
			file = self.file_light
		else:
			file = self.file_dark

		if file in Image.cached:
			return Image.cached[file]
		else:
			data = _b64_data_from_image_data(_image_to_data(file))
			Image.cached[file] = data
			return data


class Img (Inline):
	def __init__(self, image: Image) -> None:
		super().__init__()
		self.image = image

	def width(self, layout: Layout) -> float:
		return WIDTH

	def height(self, layout: Layout) -> float:
		return HEIGHT

	def html(self, layout: Layout) -> str:
		return '''<img class="{}" src="{}">'''.format(self.className, self.image.data(layout))


def _path_for_image(name): #type: (str) -> str
	return 'Packages/{}/images/{}'.format(core.current_package_name(), name)


class Images:
	shared = None #type: Images

	def __init__(self) -> None:
		self.dot = Image.named('breakpoint.png')
		self.dot_emtpy = Image.named('breakpoint-broken.png')
		self.dot_expr = Image.named('breakpoint-expr.png')
		self.dot_log = Image.named('breakpoint-log.png')
		self.dot_disabled = Image.named('breakpoint-disabled.png')
		self.resume = Image.named_light_dark('continue.png')
		self.play = Image.named_light_dark('play.png')
		self.stop = Image.named_light_dark('stop.png')
		self.settings = Image.named_light_dark('settings.png')
		self.pause = Image.named_light_dark('pause.png')

		self.clear = Image.named_light_dark('clear.png')

		self.stop_disable = Image.named_light_dark('stop_disabled.png')
		self.pause_disable = Image.named_light_dark('pause_disabled.png')

		self.up = Image.named_light_dark('up.png')
		self.down = Image.named_light_dark('step_over.png')
		self.left = Image.named_light_dark('step_out.png')
		self.right = Image.named_light_dark('step_into.png')

		self.down_disable = Image.named_light_dark('step_over_disabled.png')
		self.left_disable = Image.named_light_dark('step_out_disabled.png')
		self.right_disable = Image.named_light_dark('step_into_disabled.png')

		self.thread = Image.named_light_dark('thread_stopped.png')
		self.thread_running = Image.named_light_dark('thread_running.png')

		self.open = Image.named_light_dark('open.png')
		self.close = Image.named_light_dark('close.png')
