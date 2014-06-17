import sublime, sublime_plugin, re, posixpath, os.path, json

class NodeModuleJumpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        pos = self.view.sel()[0].begin()
        curr_line = self.view.line(pos)
        line_cnt = self.view.substr(curr_line)
        matches = re.search(r'require\([\'\"](.+?)[\'\"]\)', line_cnt, re.I|re.X)

        if matches:
            #get the current file path
            curr_path = self.view.file_name()
            location = curr_path[:(curr_path.rfind('/')+1)] 
            new_path = posixpath.normpath(location + matches.group(1))

            # check for file
            if os.path.isfile(new_path + 'package.json'):
                json_data = open(new_path + 'package.json')
                data = json.load(json_data)
                new_path = new_path + data['main']
                json_data.close()
            elif os.path.isfile(new_path + '/index.js'):
                new_path = new_path + '/index.js'
            else:
                new_path = new_path + '.js'


            # open the file in the current window
            sublime.active_window().open_file(new_path)
