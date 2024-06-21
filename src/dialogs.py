# dialogs.py

from gi.repository import Adw, Gtk, Gdk, GLib, GtkSource, Gio, GdkPixbuf
from .available_models import available_models

# CLEAR CHAT | WORKS

def clear_chat_response(self, dialog, task):
    if dialog.choose_finish(task) == "clear":
        self.clear_chat()

def clear_chat(self):
    if self.bot_message is not None:
        self.show_toast("info", 1, self.main_overlay)
        return
    dialog = Adw.AlertDialog(
        heading=_("Clear Chat"),
        body=_("Are you sure you want to clear the chat?"),
        close_response="cancel"
    )
    dialog.add_response("cancel", _("Cancel"))
    dialog.add_response("clear", _("Clear"))
    dialog.set_response_appearance("clear", Adw.ResponseAppearance.DESTRUCTIVE)
    dialog.choose(
        parent = self,
        cancellable = None,
        callback = lambda dialog, task: clear_chat_response(self, dialog, task)
    )

# DELETE CHAT | WORKS

def delete_chat_response(self, dialog, task, chat_name):
    if dialog.choose_finish(task) == "delete":
        self.delete_chat(chat_name)

def delete_chat(self, chat_name):
    dialog = Adw.AlertDialog(
        heading=_("Delete Chat"),
        body=_("Are you sure you want to delete '{}'?").format(chat_name),
        close_response="cancel"
    )
    dialog.add_response("cancel", _("Cancel"))
    dialog.add_response("delete", _("Delete"))
    dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
    dialog.choose(
        parent = self,
        cancellable = None,
        callback = lambda dialog, task, chat_name=chat_name: delete_chat_response(self, dialog, task, chat_name)
    )

# RENAME CHAT | WORKS

def rename_chat_response(self, dialog, task, old_chat_name, entry, label_element):
    if not entry: return
    new_chat_name = entry.get_text()
    if old_chat_name == new_chat_name: return
    if new_chat_name and (task is None or dialog.choose_finish(task) == "rename"):
        self.rename_chat(old_chat_name, new_chat_name, label_element)

def rename_chat(self, label_element):
    chat_name = label_element.get_parent().get_name()
    entry = Gtk.Entry()
    dialog = Adw.AlertDialog(
        heading=_("Rename Chat"),
        body=_("Renaming '{}'").format(chat_name),
        extra_child=entry,
        close_response="cancel"
    )
    entry.connect("activate", lambda dialog, old_chat_name=chat_name, entry=entry, label_element=label_element: rename_chat_response(self, dialog, None, old_chat_name, entry, label_element))
    dialog.add_response("cancel", _("Cancel"))
    dialog.add_response("rename", _("Rename"))
    dialog.set_response_appearance("rename", Adw.ResponseAppearance.SUGGESTED)
    dialog.choose(
        parent = self,
        cancellable = None,
        callback = lambda dialog, task, old_chat_name=chat_name, entry=entry, label_element=label_element: rename_chat_response(self, dialog, task, old_chat_name, entry, label_element)
    )

# NEW CHAT | WORKS | UNUSED REASON: The 'Add Chat' button now creates a chat without a name AKA "New Chat"

def new_chat_response(self, dialog, task, entry):
    chat_name = _("New Chat")
    if entry is not None and entry.get_text() != "": chat_name = entry.get_text()
    if chat_name and (task is None or dialog.choose_finish(task) == "create"):
        self.new_chat(chat_name)


def new_chat(self):
    entry = Gtk.Entry()
    dialog = Adw.AlertDialog(
        heading=_("Create Chat"),
        body=_("Enter name for new chat"),
        extra_child=entry,
        close_response="cancel"
    )
    entry.connect("activate", lambda dialog, entry: new_chat_response(self, dialog, None, entry))
    dialog.add_response("cancel", _("Cancel"))
    dialog.add_response("create", _("Create"))
    dialog.set_response_appearance("create", Adw.ResponseAppearance.SUGGESTED)
    dialog.choose(
        parent = self,
        cancellable = None,
        callback = lambda dialog, task, entry=entry: new_chat_response(self, dialog, task, entry)
    )

# STOP PULL MODEL | WORKS

def stop_pull_model_response(self, dialog, task, model_name):
    if dialog.choose_finish(task) == "stop":
        self.stop_pull_model(model_name)

def stop_pull_model(self, model_name):
    dialog = Adw.AlertDialog(
        heading=_("Stop Model"),
        body=_("Are you sure you want to stop pulling '{}'?").format(model_name),
        close_response="cancel"
    )
    dialog.add_response("cancel", _("Cancel"))
    dialog.add_response("stop", _("Stop"))
    dialog.set_response_appearance("stop", Adw.ResponseAppearance.DESTRUCTIVE)
    dialog.choose(
        parent = self.manage_models_dialog,
        cancellable = None,
        callback = lambda dialog, task, model_name = model_name: stop_pull_model_response(self, dialog, task, model_name)
    )

# DELETE MODEL | WORKS

def delete_model_response(self, dialog, task, model_name):
    if dialog.choose_finish(task) == "delete":
        self.delete_model(model_name)

def delete_model(self, model_name):
    dialog = Adw.AlertDialog(
        heading=_("Delete Model"),
        body=_("Are you sure you want to delete '{}'?").format(model_name),
        close_response="cancel"
    )
    dialog.add_response("cancel", _("Cancel"))
    dialog.add_response("delete", _("Delete"))
    dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
    dialog.choose(
        parent = self.manage_models_dialog,
        cancellable = None,
        callback = lambda dialog, task, model_name = model_name: delete_model_response(self, dialog, task, model_name)
    )

# PULL MODEL | WORKS

def pull_model_response(self, dialog, task, model_name, tag_drop_down):
    if dialog.choose_finish(task) == "pull":
        model = f"{model_name}:{tag_drop_down.get_selected_item().get_string().split(' | ')[0]}"
        self.pull_model(model)

def pull_model(self, model_name):
    tag_list = Gtk.StringList()
    for tag in available_models[model_name]['tags']:
        tag_list.append(f"{tag[0]} | {tag[1]}")
    tag_drop_down = Gtk.DropDown(
        enable_search=True,
        model=tag_list
    )
    dialog = Adw.AlertDialog(
        heading=_("Pull Model"),
        body=_("Please select a tag to pull '{}'").format(model_name),
        extra_child=tag_drop_down,
        close_response="cancel"
    )
    dialog.add_response("cancel", _("Cancel"))
    dialog.add_response("pull", _("Pull"))
    dialog.set_response_appearance("pull", Adw.ResponseAppearance.SUGGESTED)
    dialog.choose(
        parent = self.manage_models_dialog,
        cancellable = None,
        callback = lambda dialog, task, model_name = model_name, tag_drop_down = tag_drop_down: pull_model_response(self, dialog, task, model_name, tag_drop_down)
    )

# REMOVE IMAGE | WORKS

def remove_attached_file_response(self, dialog, task, button):
    if dialog.choose_finish(task) == 'remove':
        self.remove_attached_file(button)

def remove_attached_file(self, button):
    dialog = Adw.AlertDialog(
        heading=_("Remove File"),
        body=_("Are you sure you want to remove file?"),
        close_response="cancel"
    )
    dialog.add_response("cancel", _("Cancel"))
    dialog.add_response("remove", _("Remove"))
    dialog.set_response_appearance("remove", Adw.ResponseAppearance.DESTRUCTIVE)
    dialog.choose(
        parent = self,
        cancellable = None,
        callback = lambda dialog, task, button=button: remove_attached_file_response(self, dialog, task, button)
    )

# RECONNECT REMOTE | WORKS

def reconnect_remote_response(self, dialog, task, entry):
    response = dialog.choose_finish(task)
    if not task or response == "remote":
        self.connect_remote(entry.get_text())
    elif response == "local":
        self.connect_local()
    elif response == "close":
        self.destroy()

def reconnect_remote(self, current_url):
    entry = Gtk.Entry(
        css_classes = ["error"],
        text = current_url
    )
    dialog = Adw.AlertDialog(
        heading=_("Connection Error"),
        body=_("The remote instance has disconnected"),
        extra_child=entry
    )
    entry.connect("activate", lambda entry, dialog: reconnect_remote_response(self, dialog, None, entry))
    dialog.add_response("close", _("Close Alpaca"))
    dialog.add_response("local", _("Use local instance"))
    dialog.add_response("remote", _("Connect"))
    dialog.set_response_appearance("remote", Adw.ResponseAppearance.SUGGESTED)
    dialog.choose(
        parent = self,
        cancellable = None,
        callback = lambda dialog, task, entry=entry: reconnect_remote_response(self, dialog, task, entry)
    )

# CREATE MODEL | WORKS

def create_model_from_existing_response(self, dialog, task, dropdown):
    model = dropdown.get_selected_item().get_string()
    if dialog.choose_finish(task) == 'accept' and model:
        self.create_model(model, False)

def create_model_from_existing(self):
    string_list = Gtk.StringList()
    for model in self.local_models:
        string_list.append(model)

    dropdown = Gtk.DropDown()
    dropdown.set_model(string_list)
    dialog = Adw.AlertDialog(
        heading=_("Select Model"),
        body=_("This model will be used as the base for the new model"),
        extra_child=dropdown
    )
    dialog.add_response("cancel", _("Cancel"))
    dialog.add_response("accept", _("Accept"))
    dialog.set_response_appearance("accept", Adw.ResponseAppearance.SUGGESTED)
    dialog.choose(
        parent = self,
        cancellable = None,
        callback = lambda dialog, task, dropdown=dropdown: create_model_from_existing_response(self, dialog, task, dropdown)
    )

def create_model_from_file_response(self, file_dialog, result):
    try: file = file_dialog.open_finish(result)
    except: return
    try:
        self.create_model(file.get_path(), True)
    except Exception as e:
        self.show_toast("error", 5, self.main_overlay) ##TODO NEW ERROR MESSAGE

def create_model_from_file(self):
    file_dialog = Gtk.FileDialog(default_filter=self.file_filter_gguf)
    file_dialog.open(self, None, lambda file_dialog, result: create_model_from_file_response(self, file_dialog, result))

# FILE CHOOSER | WORKS

def attach_file_response(self, file_dialog, result):
    file_types = {
        "plain_text": ["txt", "md", "html", "css", "js", "py", "java", "json", "xml"],
        "image": ["png", "jpeg", "jpg", "webp", "gif"],
        "pdf": ["pdf"],
        "docx": ["docx"]
    }
    try: file = file_dialog.open_finish(result)
    except: return
    extension = file.get_path().split(".")[-1]
    file_type = next(key for key, value in file_types.items() if extension in value)
    if not file_type: return
    if file_type == 'image' and not self.verify_if_image_can_be_used():
        self.show_toast('error', 8, self.main_overlay)
        return
    self.attach_file(file.get_path(), file_type)


def attach_file(self, filter):
    file_dialog = Gtk.FileDialog(default_filter=filter)
    file_dialog.open(self, None, lambda file_dialog, result: attach_file_response(self, file_dialog, result))
