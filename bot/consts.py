"""
Stores consts names for easier JSON file access
"""

EMAIL = "email"
PASSWORD = "password"
THREAD_ID = "thread_id"
IS_THREAD_USER = "is_thread_user"
ADMIN_FBID_LIST = "admin_fbid_list"
USERS = "users"
MESSAGES = "messages"

COMMANDS = "commands"


class Msgs:
    ON_LOGGED_IN = "on_logged_in"
    CMD_ERROR_NOT_FOUND = "command_error_not_found"
    CMD_ERROR_NOT_ADMIN = "command_error_not_admin"
    CMD_ERROR_EXEC = "command_error_execution"


class Cmd:
    NAME = "cmd_name"
    ALT_NAME = "cmd_alt_name"
    INFO = "info"
    IS_ADMIN = "is_admin"
    ENTRY_METHOD = "entry_method"
    ARGS = "args"
    TXT_EXECUTED = "txt_executed"
    TXT_FORMAT = "txt_format"
    TXT_ARG_ERROR = "txt_arg_error"
    TXT_ERROR = "txt_error"


class User:
    ID = "id"
    NAME = "name"
    FULL_NAME = "full_name"
    GENDER = "gender"
    THUMB_SRC = "thumb_src"
    URL = "url"
    NICKNAMES = "nicknames"
    IN_CHAT = "in_chat"
    IS_FRIEND = "is_friend"
    ADDRESSING_NAMES = "addressing_names"
