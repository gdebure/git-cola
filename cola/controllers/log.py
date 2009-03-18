"""This module provides the controller for the log display

"""

from cola import qtutils
from cola.model import Model
from cola.views import LogView
from cola.qobserver import QObserver

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def logger(parent):
    # TODO: subclass model
    model = Model()
    model.search_text = ''
    view = LogView(parent)
    ctl = LogController(model,view)
    return view

class LogController(QObserver):
    """The output log controller"""

    def __init__(self, model, view):
        QObserver.__init__(self, model, view)
        self.add_observables('search_text')
        self.add_actions(search_text = self.insta_search)
        self.add_callbacks(clear_button = self.clear,
                           next_button = self.next,
                           prev_button = self.prev)
        self.connect(self.view.output_text,
                     'cursorPositionChanged()',
                     self.cursor_position_changed)
        self.search_offset = 0

    def insta_search(self, *rest):
        self.search_offset = 0
        txt = self.model.get_search_text().lower()
        if len(txt.strip()):
            self.next()
        else:
            cursor = self.view.output_text.textCursor()
            cursor.clearSelection()
            self.view.output_text.setTextCursor(cursor)

    def clear(self):
        self.view.output_text.clear()
        self.search_offset = 0

    def next(self):
        text = self.model.get_search_text().lower().strip()
        if not text:
            return
        output = str(self.view.output_text.toPlainText())
        if self.search_offset + len(text) > len(output):
            title = unicode(self.tr('%s not found')) % text
            question = unicode(self.tr("Could not find '%s'.\n"
                                       'Search from the beginning?')) % text
            if qtutils.question(self.view, title, question, default=False):
                self.search_offset = 0
            else:
                return

        find_in = output[self.search_offset:].lower()
        try:
            index = find_in.index(text)
        except:
            self.search_offset = 0
            title = unicode(self.tr("%s not found")) % text
            question = unicode(self.tr("Could not find '%s'.\n"
                                       'Search from the beginning?')) % text
            if qtutils.question(self.view, title, default=False):
                self.next()
            return
        cursor = self.view.output_text.textCursor()
        offset = self.search_offset + index
        new_offset = offset + len(text)

        cursor.setPosition(offset)
        cursor.setPosition(new_offset, cursor.KeepAnchor)

        self.view.output_text.setTextCursor(cursor)
        self.search_offset = new_offset

    def prev(self):
        text = self.model.get_search_text().lower().strip()
        if not text:
            return
        output = str(self.view.output_text.toPlainText())
        if self.search_offset == 0:
            self.search_offset = len(output)

        find_in = output[:self.search_offset].lower()
        try:
            offset = find_in.rindex(text)
        except:
            self.search_offset = 0
            title = unicode(self.tr('%s not found')) % text
            question = unicode(self.tr("Could not find '%s'.\n"
                                       'Search from the end?')) % text
            if qtutils.question(self.view, title, question):
                self.prev()
            return
        cursor = self.view.output_text.textCursor()
        new_offset = offset + len(text)

        cursor.setPosition(offset)
        cursor.setPosition(new_offset, cursor.KeepAnchor)

        self.view.output_text.setTextCursor(cursor)
        self.search_offset = offset

    def cursor_position_changed(self):
        cursor = self.view.output_text.textCursor()
        self.search_offset = cursor.selectionStart()