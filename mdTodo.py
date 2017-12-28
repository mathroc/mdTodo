from datetime import datetime

import sublime
import sublime_plugin

ALLOWED_FILETYPES = ('.md', '.markdown', '.mdown')


class MdTodoBase(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = self.view.file_name()
        # list of allowed filetypes
        if not (filename or filename.endswith(ALLOWED_FILETYPES)):
            return False
        self.run(edit)


class MdTodoNewCommand(MdTodoBase):
    def run(self, edit):
        for region in self.view.sel():
            lines = self.view.lines(region)
            lines.reverse()
            for line in lines:
                # don't add a newline when creating new item with cursor is at an empty line
                if not line:
                    line_contents = '* [ ] '
                    self.view.insert(edit, line.begin(), line_contents)
                # add a newline when creating new item when cursor is at another line
                else:
                    line_contents = self.view.substr(line) + '\n* [ ] '
                    self.view.replace(edit, line, line_contents)


class MdTodoDoneCommand(MdTodoBase):
    def run(self, edit):
        for region in self.view.sel():
            lines = self.view.lines(region)
            lines.reverse()
            for line in lines:
                line_contents = self.view.substr(line).strip()
                # prepend @done if item is ongoing
                if line_contents.startswith('* [ ] '):
                    self.view.insert(edit,
                                     line.end(), " @done (%s)" %
                                     datetime.now().strftime("%Y-%m-%d %H:%M"))
                    self.view.replace(edit, "* [ ] , "* [x] ")
                # undo @todo
                elif line_contents.startswith('* [x] '):
                    subfix = self.view.find('(\s)*@done(.)+\)$', line.begin())
                    self.view.erase(edit, subfix)
                    self.view.replace(edit, "* [x] ", "* [ ] ")
