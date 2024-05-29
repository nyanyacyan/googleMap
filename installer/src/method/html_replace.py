# coding: utf-8
#* htmlの置換を行う
# ----------------------------------------------------------------------------------
# 2023/5/30更新

# ----------------------------------------------------------------------------------

# 自作モジュール
from .base.utils import Logger, NoneChecker
from .base.B_html_replace import HtmlReplaceBase

###############################################################


class HtmlReplace(HtmlReplaceBase):
    def __init__(self, debug_mode=False):

        # logger
        self.setup_logger = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.setup_logger.setup_logger()

        # noneチェック
        self.none = NoneChecker()

        # インスタンス化
        HtmlReplaceBase()


###############################################################
# ----------------------------------------------------------------------------------

    def _html_file_read(self, input_html_file_path):
        return super()._html_file_read(input_html_file_path)


    def _html_file_write(self, update_file_path):
        return super()._html_file_write(update_file_path)


    def _partial_match_replace(self, mark_pattern, new_data, html_code, filed_name):
        return super()._partial_match_replace(mark_pattern, new_data, html_code, filed_name)

# ----------------------------------------------------------------------------------
# htmlを置換する

    def html_replace_process(self, html_file):
        '''
        input_html_file_path
        update_file_path
        mark_pattern
        new_data, html_code
        filed_name
        '''
        try:
            self.logger.info(f"******** html_replace_process start ********")

            # htmlファイルの読み込み
            html_code = self._html_file_read(html_file)


            self.logger.info(f"********  html_replace_process end ********")

        except Exception as e:
            self.logger.error(f"html_replace_process 処理中にエラーが発生: {e}")


# ----------------------------------------------------------------------------------