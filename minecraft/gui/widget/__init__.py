# Minecraft-in-python, a sandbox game
# Copyright (C) 2020-2023  Minecraft-in-python team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from minecraft.utils.utils import *
from pyglet.event import EventDispatcher
from pyglet.sprite import Sprite as PygletSprite


class Widget(EventDispatcher):
    """窗口中所有可交互（当然, 也可以不提供交互功能）的小部件的基类。"""

    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def position(self):
        return self._x, self._y

    @position.setter
    def position(self, value):
        self._x, self._y = value[0], get_size()[1] - value[1]
        self._update()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self._update()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        self._update()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width
        self._update()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
        self._update()

    def _update(self):
        pass

    def draw(self):
        pass

    def check_hit(self, x, y):
        return (self._x < x < self._x + self._width) and (self._y < y < self._y + self._height)

    def on_focus(self):
        pass

    def on_unfocus(self):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_press(self, x, y, buttons, modifiers):
        pass

    def on_mouse_release(self, x, y, buttons, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_scroll(self, x, y, mouse, direction):
        pass

    def on_resize(self, width, height):
        pass

    def on_text(self, text):
        pass

    def on_text_motion(self, motion):
        pass

    def on_text_motion_select(self, motion):
        pass


Widget.register_event_type("on_unfocus")
Widget.register_event_type("on_focus")
Widget.register_event_type("on_key_press")
Widget.register_event_type("on_key_release")
Widget.register_event_type("on_mouse_press")
Widget.register_event_type("on_mouse_release")
Widget.register_event_type("on_mouse_motion")
Widget.register_event_type("on_mouse_drag")
Widget.register_event_type("on_mouse_scroll")
Widget.register_event_type("on_text")
Widget.register_event_type("on_text_motion")
Widget.register_event_type("on_text_motion_select")


class InputWidget(Widget):
    """提供输入功能的部件。

    继承了该类的部件被认为是可以取得焦点的，即`on_focus`和`on_unfocus`方法有效。

    最早向`Frame`中添加的`InputWidget`会在调用了`Frame.enable()`后自动获取焦点。
    """
    pass


class Sprite():
    """即使缩放也不会失真的精灵图片。

    为了代码简洁，只将贴图分成了5块，应在横纵坐标缩放率不一致时才使用，类似于九宫格。
    """

    def __init__(self, img, x=0, y=0, border=1, border_width=1):
        """初始化图片精灵，类似于直接使用`pyglet.sprite.Sprite`。"""
        self._image = img
        self._x, self._y = x, y
        self._border, self._border_width = border, border_width
        self._scale = (0, 0)
        self._split_img()
        self._update()

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image
        self._split_img()
        self._update()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._update()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._update()

    @property
    def position(self):
        return self._x, self._y

    @position.setter
    def position(self, value):
        self._x, self._y = value
        self._update()

    @property
    def scale_x(self):
        return self._scale[0]

    @scale_x.setter
    def scale_x(self, value):
        self._scale = (value, self._scale[1])
        self._update()

    @property
    def scale_y(self):
        return self._scale[1]

    @scale_y.setter
    def scale_y(self, value):
        self._scale = (self._scale[0], value)
        self._update()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = (value, value)
        self._update()

    def _split_img(self):
        b, w, h = self._border, self._image.width, self._image.height
        self._top = PygletSprite(self._image.get_region(0, h - b, w, b))
        self._center_left = PygletSprite(
            self._image.get_region(0, b, b, h - 2 * b))
        self._center_center = PygletSprite(
            self._image.get_region(b, b, w - 2 * b, h - 2 * b))
        self._center_right = PygletSprite(
            self._image.get_region(w - b, b, b, h - 2 * b))
        self._bottom = PygletSprite(self._image.get_region(0, 0, w, b))

    def _update(self):
        w, h = self._image.width * \
            self._scale[0], self._image.height * self._scale[1]
        self._top.position = (self._x, self._y + h - self._border_width)
        self._top.scale_x = w / self._top.image.width
        self._top.scale_y = self._border_width / self._top.image.height
        self._center_left.position = (self._x, self._y + self._border_width)
        self._center_left.scale_x = self._border_width / self._center_left.image.width
        self._center_left.scale_y = (
            h - 2 * self._border_width) / self._center_left.image.height
        self._center_center.position = (
            self._x + self._border_width, self._y + self._border_width)
        self._center_center.scale_x = (
            w - 2 * self._border_width) / self._center_center.image.width
        self._center_center.scale_y = (
            h - 2 * self._border_width) / self._center_center.image.height
        self._center_right.position = (
            self._x + w - self._border_width, self._y + self._border_width)
        self._center_right.scale_x = self._border_width / self._center_right.image.width
        self._center_right.scale_y = (
            h - 2 * self._border_width) / self._center_right.image.height
        self._bottom.position = (self.x, self.y + self._border_width)
        self._bottom.scale_x = w / self._bottom.image.width
        self._bottom.scale_y = self._border_width / self._bottom.image.height

    def draw(self):
        self._top.draw()
        self._center_left.draw()
        self._center_center.draw()
        self._center_right.draw()
        self._bottom.draw()
