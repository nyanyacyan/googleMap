# coding: utf-8
#* htmlの置換を行う
# ----------------------------------------------------------------------------------
# 2023/5/30更新

# ----------------------------------------------------------------------------------
import time

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


    def _html_file_write(self, update_file_path, all_update_html_code):
        return super()._html_file_write(update_file_path, all_update_html_code)


    def _partial_match_replace(self, mark_pattern, new_data, html_code, filed_name):
        return super()._partial_match_replace(mark_pattern, new_data, html_code, filed_name)

# ----------------------------------------------------------------------------------
# htmlを置換する

    def html_replace_process(self, input_html_file_path, update_file_path):
        '''
        input_html_file_path  ベースとなるhtmlファイルpath
        update_file_path  アップデートされたhtml_codeのファイル出力
        mark_pattern  マークをしてるパターンを入力(.*?)が間に入れて部分一致にしてる
        new_data  置換する新しいデータ
        html_code  アップデートされたhtml_code
        filed_name  置換してる箇所の名称
        '''
        try:
            self.logger.info(f"******** html_replace_process start ********")

            # htmlファイルの読み込み
            base_html_code = self._html_file_read(input_html_file_path)


            # 店舗名
            shop_name_update = self._partial_match_replace(
                mark_pattern="r'<!-- 住所:置換 start -->(.*?)<!-- 住所:置換 end -->'",
                new_data='',
                html_code=base_html_code,
                filed_name='shop_name_update'
            )
            time.sleep(2)

            # 写真
            address_update = self._partial_match_replace(
                mark_pattern="r'<!-- 住所:置換 start -->(.*?)<!-- 住所:置換 end -->'",
                new_data='',
                html_code=shop_name_update,
                filed_name='address_update'
            )
            time.sleep(2)

            # 市区町村
            city_address_update = self._partial_match_replace(
                mark_pattern="r'<!-- 住所:置換 start -->(.*?)<!-- 住所:置換 end -->'",
                new_data='',
                html_code=address_update,
                filed_name='city_address_update'
            )
            time.sleep(2)

            # 住所を置換
            full_address_update = self._partial_match_replace(
                mark_pattern="r'<!-- 住所:置換 start -->(.*?)<!-- 住所:置換 end -->'",
                new_data='',
                html_code=city_address_update,
                filed_name='full_address_update'
            )
            time.sleep(2)

            # 電話番号
            tel_num_update = self._partial_match_replace(
                mark_pattern="r'<!-- 住所:置換 start -->(.*?)<!-- 住所:置換 end -->'",
                new_data='',
                html_code=full_address_update,
                filed_name='tel_num_update'
            )
            time.sleep(2)

            # 営業時間
            hours_update = self._partial_match_replace(
                mark_pattern="r'<!-- 住所:置換 start -->(.*?)<!-- 住所:置換 end -->'",
                new_data='',
                html_code=tel_num_update,
                filed_name='hours_update'
            )
            time.sleep(2)

            # 定休日
            closed_day_update = self._partial_match_replace(
                mark_pattern="r'<!-- 住所:置換 start -->(.*?)<!-- 住所:置換 end -->'",
                new_data='',
                html_code=hours_update,
                filed_name='closed_day_update'
            )
            time.sleep(2)

            # 公式サイト
            url_update = self._partial_match_replace(
                mark_pattern="r'<!-- 住所:置換 start -->(.*?)<!-- 住所:置換 end -->'",
                new_data='',
                html_code=closed_day_update,
                filed_name='url_update'
            )
            time.sleep(2)

            # 口コミ
            review_update = self._partial_match_replace(
                mark_pattern="r'<!-- 住所:置換 start -->(.*?)<!-- 住所:置換 end -->'",
                new_data='',
                html_code=url_update,
                filed_name='review_update'
            )
            time.sleep(2)

            # ジャンル
            genre_update = self._partial_match_replace(
                mark_pattern="r'<!-- 住所:置換 start -->(.*?)<!-- 住所:置換 end -->'",
                new_data='',
                html_code=review_update,
                filed_name='genre_update'
            )
            time.sleep(2)

            # 料金ランク
            price_rank_update = self._partial_match_replace(
                mark_pattern="r'<!-- 住所:置換 start -->(.*?)<!-- 住所:置換 end -->'",
                new_data='',
                html_code=genre_update,
                filed_name='price_rank_update'
            )
            time.sleep(2)

            # 全てのデータがここに集約
            all_update_html_code= price_rank_update

            self.logger.warning(f"all_update_html_code: \n{all_update_html_code[:100]}")

            self._html_file_write(update_file_path, update_file_path=all_update_html_code)


            self.logger.info(f"********  html_replace_process end ********")


        except Exception as e:
            self.logger.error(f"html_replace_process 処理中にエラーが発生: {e}")


# ----------------------------------------------------------------------------------