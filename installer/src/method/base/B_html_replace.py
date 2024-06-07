# coding: utf-8
#* htmlの置換を行う基底クラス
# ----------------------------------------------------------------------------------
# 2023/5/30更新

# ----------------------------------------------------------------------------------
import re
from jinja2 import Environment, FileSystemLoader


# 自作モジュール
from .utils import Logger, NoneChecker

# ----------------------------------------------------------------------------------
###############################################################
# htmlを置換するクラス

class HtmlReplaceBase:
    def __init__(self, debug_mode=False):

        # logger
        self.setup_logger = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.setup_logger.setup_logger()

        # noneチェック
        self.none = NoneChecker()


###############################################################
# ----------------------------------------------------------------------------------
# htmlファイルの読み込み

    def _html_file_read(self, input_html_file_path):
        try:
            self.logger.info(f"******** _html_file_read start ********")

            # htmlファイルを読み込む
            with open(input_html_file_path, 'r', encoding='utf-8') as file:
                html_code = file.read()

            self.logger.debug(f"html_code: \n{html_code[:30]}")

            self.logger.info(f"********  _html_file_read end ********")

            return html_code


        except FileNotFoundError as e:
            self.logger.error(f"{input_html_file_path} が見つかりません。pathを確認してください: {e}")
            raise

        except Exception as e:
            self.logger.error(f"{input_html_file_path}  読込中にエラーが発生: {e}")
            raise


# ----------------------------------------------------------------------------------
# 部分一致での置換

    def _partial_match_replace(self, mark_pattern, new_data, html_code, filed_name):
        try:
            self.logger.info(f"******** {filed_name} _replace_base start ********")

            self.logger.debug(f"{filed_name} mark_pattern: {mark_pattern}")
            self.logger.debug(f"{filed_name} new_data: {new_data}")
            self.logger.debug(f"{filed_name} html_code: {html_code[:30]}")

            # パターンを定義する（マークを定義）
            # re.compileは部分一致させることができる
            # →マークの間に「(.*?)」任意の文字列を最短一致でマッチさせる（非貪欲マッチ）
            pattern = re.compile(mark_pattern, re.DOTALL)

            # パターンを元に新しいデータに置換する
            # 第１の位置引数にパターン、第二引数に新しいデータ、第三引数に置換する全体のcode
            update_html_code = re.sub(pattern, new_data, html_code)

            self.logger.debug(f"{filed_name} update_html_code: \n{update_html_code[:100]}")

            self.logger.info(f"******** {filed_name}  _replace_base end ********")

            return update_html_code

        except Exception as e:
            self.logger.error(f"{filed_name} _replace_base 処理中にエラーが発生: {e}")


# ----------------------------------------------------------------------------------
# htmlファイルを出力する

    def _html_file_write(self, update_file_path, all_update_html_code):
        try:
            self.logger.info(f"******** html_replace start ********")

            with open(update_file_path, 'w', encoding='utf-8') as file:
                new_html_file = file.write(all_update_html_code)

            self.logger.debug(f"new_html_file:\n {new_html_file[:100]}")

            self.logger.info(f"********  html_replace end ********")

            return new_html_file

        except FileNotFoundError as e:
            self.logger.error(f"{update_file_path} が見つかりません。pathを確認してください: {e}")
            raise

        except Exception as e:
            self.logger.error(f"{update_file_path} 書き込み中にエラーが発生: {e}")
            raise


# ----------------------------------------------------------------------------------
# jinja2を使った置換

    def jinja2_replace_html(self, html_file_dir, html_file, store_data_list):
        try:
            self.logger.info(f"******** jinja2_replace_html start ********")

            self.logger.debug(f"html_file_dir: {html_file_dir}, html_file: {html_file}")
            self.logger.debug(f"store_data_list:\n{store_data_list[:100]}")


            # template.htmlが格納されてるディレクトリを示す
            file_dir = Environment(loader=FileSystemLoader(html_file_dir))

            # template_htmlのファイル名を指定して読み込む
            template_html = file_dir.get_template(html_file)
            self.logger.debug(f"template_html:\n{template_html[:100]}")

            # テンプレートに沿ってデータをレンダリング（書き込んでいく）
            output_html = template_html.render(stores_data=store_data_list)
            self.logger.debug(f"output_html:\n{output_html[:100]}")

            self.logger.info(f"******** jinja2_replace_html end ********")

            return output_html

        except Exception as e:
            self.logger.error(f"jinja2_replace_html 処理中にエラーが発生: {e}")


# ----------------------------------------------------------------------------------



#! 置換するものリスト

# TODO 地図（緯度、経度）
# TODO 店舗名
# TODO 写真
# TODO 電話番号
# TODO レビュー（ランク、名前、テキスト）
# TODO 営業時間
# TODO 定休日
# TODO サイトURL