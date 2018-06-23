import random
import string
import io
import hashlib
import hmac
import yaml

from httprunner import exception, logger


SECRET_KEY = "DebugTalk"


def get_random_string(str_len):
    return ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(str_len))


def gen_md5(*str_args):
    return hashlib.md5("".join(str_args).encode('utf-8')).hexdigest()


def get_sign(*args):
    content = ''.join(args).encode('ascii')
    sign_key = SECRET_KEY.encode('ascii')
    sign = hmac.new(sign_key, content, hashlib.sha1).hexdigest() #hmac是什么鬼
    return sign


def remove_prefix(text, prefix):
    """remove prefix from text"""
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

class FileUtils(object):

    @staticmethod
    def _check_format(file_path, content):
        """ check testcase fromat if valid
        """
        if not content:
            # testcase file content is empty
            err_msg = u"Testcase file conetent is empty: {}".format(file_path)
            logger.log_error(err_msg)
            raise exception.FileFormatError(err_msg)

    @staticmethod
    def _load_yaml_file(yaml_file):
        """load yaml file and check file content format"""
        with io.open(yaml_file, 'r', encoding='utf-8') as stream:
            yaml_content = yaml.load(stream)
            FileUtils._check_format(yaml_file, yaml_content)
