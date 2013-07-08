#  gcompris - decryption.py
#
# Copyright (C) 2003, 2008 Bruno Coudoin
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# decryption activity.
import gtk
import gtk.gdk
import gcompris
import gcompris.utils
import gcompris.skin
import goocanvas
import pango
from key_value import *
from gcompris import gcompris_gettext as _

#
# The name of the class is important. It must start with the prefix
# 'Gcompris_' and the last part 'decryption' here is the name of
# the activity and of the file in which you put this code. The name of
# the activity must be used in your menu.xml file to reference this
# class like this: type="python:decryption"
#
class Gcompris_decryption:
  """Empty gcompris Python class"""


  def __init__(self, gcomprisBoard):
    print "decryption init"

    # Save the gcomprisBoard, it defines everything we need
    # to know from the core
    self.gcomprisBoard = gcomprisBoard
    self.gcomprisBoard.level = 1
    self.gcomprisBoard.maxlevel = 3
    self.gcomprisBoard.sublevel = 1
    self.gcomprisBoard.number_of_sublevel = 3

    # Parameters for different sublevels
    self.NUMBERS = 1
    self.SYMBOLS = 2
    self.ALPHABETS = 3
    self.VALUE = None

    # Needed to get key_press
    gcomprisBoard.disable_im_context = True

  def start(self):
    print "decryption start"

    self.wordlist = None

    try:
      self.language = gcompris.gcompris_gettext( gcompris.get_locale_name(gcompris.get_locale()) )
      self.wordlist = gcompris.get_wordlist("decryption/default-$LOCALE.xml")
    except:
      pass
    # Fallback to wordsgame list
    if not self.wordlist:
      try:
        self.language = gcompris.gcompris_gettext( gcompris.get_locale_name(gcompris.get_locale()) )
        self.wordlist = gcompris.get_wordlist("wordsgame/default-$LOCALE.xml")
      except:
        pass
    # Fallback to english
    if not self.wordlist:
      try:
        self.wordlist = gcompris.get_wordlist("decryption/default-en.xml")
        self.language = _("English")
      except:
        pass
    # Fallback to English wordsgame list
    if not self.wordlist:
      self.wordlist = gcompris.get_wordlist("wordsgame/default-en.xml")
      self.language = _("English")

    if not self.wordlist:
      gcompris.utils.dialog(_("Could not find the list of words."),
                            stop_board)
      return;


    # self.wordlist = gcompris.get_wordlist("wordsgame/default-en.xml")
    # print unicode(gcompris.get_random_word(self.wordlist, 1), encoding="utf8")



    # Create our rootitem. We put each canvas item in it so at the end we
    # only have to kill it. The canvas deletes all the items it contains
    # automaticaly.
    self.rootitem = goocanvas.Group(parent =
                                   self.gcomprisBoard.canvas.get_root_item())

    self.next_level()

    ''' 
    key_value(self.rootitem,26)
    goocanvas.Text(parent=self.rootitem,
                                 x = 280,
                                 y = gcompris.BOARD_HEIGHT/2,
                                 fill_color = "white",
                                 font = gcompris.skin.get_font("gcompris/title"),
                                 anchor = gtk.ANCHOR_CENTER,
                                 text = _("Decode the encrypted text given below  "))
    self.display_arrow()

    # TUX svghandle
    svghandle = gcompris.utils.load_svg("decryption/tux.svg")
    self.tuxitem = goocanvas.Svg(
                                     parent = self.rootitem,
                                     svg_handle = svghandle,
                                     svg_id = "#TUX",
                                     tooltip = _("click on me to check whether you have decrypted rightly")
                                     )
    self.tuxitem.translate(560,340)
    self.tuxitem.connect("button_press_event", self.next_level)
    gcompris.utils.item_focus_init(self.tuxitem, None)

    '''


  def end(self):
    print "decryption end"
    # Remove the root item removes all the others inside it
    self.rootitem.remove()


  def ok(self):
    print("decryption ok.")

  def repeat(self):
    print("decryption repeat.")


  #mandatory but unused yet
  def config_stop(self):
    pass

  # Configuration function.
  def config_start(self, profile):
    print("decryption config_start.")

  def key_press(self, keyval, commit_str, preedit_str):
    utf8char = gtk.gdk.keyval_to_unicode(keyval)
    strn = u'%c' % utf8char

    print("Gcompris_decryption key press keyval=%i %s" % (keyval, strn))

  def pause(self, pause):
    print("decryption pause. %i" % pause)


  def set_level(self, level):
    print("decryption set level. %i" % level)

  def display_arrow(self):
    x_init = 40
    n = 26
    for i in range (0,n/2):
      goocanvas.Image(parent = self.rootitem,
                    pixbuf = gcompris.utils.load_pixmap("decryption/arrow.png"),
                    x = x_init,
                    y = 65,
                    )
      goocanvas.Image(parent = self.rootitem,
                    pixbuf = gcompris.utils.load_pixmap("decryption/arrow.png"),
                    x = x_init,
                    y = 155,
                    )
      x_init = x_init + 58
  
  def set_level(self, level):
    print("encryption set level. %i" % level)
    self.gcomprisBoard.level = level
    self.gcomprisBoard.sublevel = 1
    self.next_level()


  def increment_level(self):
    self.gcomprisBoard.sublevel += 1

    if(self.gcomprisBoard.sublevel > self.gcomprisBoard.number_of_sublevel):
      self.gcomprisBoard.sublevel = 1
      self.gcomprisBoard.level += 1
      if(self.gcomprisBoard.level > self.gcomprisBoard.maxlevel):
        self.gcomprisBoard.level = 1

    return 1

  # Place background image and control bar
  def base_setup(self):
    gcompris.set_background(self.gcomprisBoard.canvas.get_root_item(), "decryption/background.png")
    gcompris.bar_set(gcompris.BAR_LEVEL)
    gcompris.bar_set_level(self.gcomprisBoard)
    gcompris.bar_set(gcompris.BAR_LEVEL|gcompris.BAR_REPEAT_ICON)
    gcompris.bar_location(630, -1, 0.5)
    p = key_value(self.rootitem, self.VALUE)
    self.display_arrow()
    self.display_images(p.get_pair())


  def next_level(self):

    self.rootitem.remove()

    if (self.gcomprisBoard.sublevel == 1):
      self.VALUE = self.NUMBERS
    elif (self.gcomprisBoard.sublevel == 2):
      self.VALUE = self.SYMBOLS
    elif (self.gcomprisBoard.sublevel == 3):
      self.VALUE = self.ALPHABETS

    gcompris.bar_set_level(self.gcomprisBoard)
    self.rootitem = goocanvas.Group(parent = \
      self.gcomprisBoard.canvas.get_root_item())

    self.base_setup()

  def display_images(self, pair):
    self.pair = pair
    self.word = gcompris.get_random_word(
                          self.wordlist,
                          self.gcomprisBoard.level + 2
                          )
    self.letters = list(self.word)
    self.letters = map(lambda x: x.upper(), self.letters)
    print self.letters

    self.values = map(lambda x: self.pair[x], self.letters)
    print self.values

    self.ciphertext = ""
    for i in self.values:
      self.ciphertext += str(i) + "   "

    goocanvas.Rect(parent = self.rootitem,
                   x = 50,
                   y = 350,
                   width = 350,
                   height = 100,
                   stroke_color = "black",
                   fill_color = "green",
                   line_width = 1.0
                   )

    goocanvas.Text(parent = self.rootitem,
                   x = 220,
                   y = 400,
                   fill_color = "black",
                   font = gcompris.skin.get_font("gcompris/subtitle"),
                   anchor = gtk.ANCHOR_CENTER,
                   text = self.ciphertext
                   )
