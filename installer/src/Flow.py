# coding: utf-8
# ----------------------------------------------------------------------------------
# 2023/6/13 更新

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
import os, sys
from tkinter import messagebox
from dotenv import load_dotenv
from method.base.B_googleMap import GoogleMapBase
from method.base.B_html_replace import HtmlReplaceBase
from method.get_gm_df import GetGMPlaceDf
from method.df_merge import DfProcessMerge
from method.base.utils import Logger


load_dotenv()

####################################################################################


class Flow:
    def __init__(self, query, debug_mode=False):

        self.query = query
        # logger
        self.setup_logger = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.setup_logger.setup_logger()

        # APIKEYを取得
        self.api_key = os.getenv('GOOGLE_MAP_API_KEY')

        # インスタンス
        self.get_gm_df = GetGMPlaceDf(api_key=self.api_key)
        self.df_merge = DfProcessMerge(api_key=self.api_key)
        self.gm_geocoding = GoogleMapBase(api_key=self.api_key)
        self.html_replace = HtmlReplaceBase()


        # full_pathインスタンス
        self.result_html_data_dir = self._get_file_path_in_result_output(file_name=self.query)
        self.method_dir = self._get_method_full_dir()


####################################################################################
# ----------------------------------------------------------------------------------

    def flow_main(self, input_word):

        self.logger.warning(f"query: {self.query}")
        self.logger.warning(f"input_word: {input_word}")

        key_df = self.get_gm_df.process(
            query=self.query,
        )

        # 住所
        add_japanese_address = self.df_merge.process(
            key_df = key_df,
            column = 'formatted_address',
            add_func = self.gm_geocoding._address_to_japanese,
            new_column = 'japanese_address'
        )

        # 営業時間
        add_business_hours =self.df_merge.process(
            key_df = add_japanese_address,  # 更新したDataFrameを入れる
            column = 'current_opening_hours.weekday_text',
            add_func = self.gm_geocoding.get_business_hours,
            new_column = 'business_hours'
        )

        # 定休日
        add_close_days_df =self.df_merge.process(
            key_df = add_business_hours,  # 更新したDataFrameを入れる
            column = 'current_opening_hours.weekday_text',
            add_func = self.gm_geocoding.get_close_day,
            new_column = 'close_days'
        )

        # 都道府県
        add_prefectures_df =self.df_merge.process(
            key_df = add_close_days_df,  # 更新したDataFrameを入れる
            column = 'address_components',
            add_func = self.gm_geocoding._get_prefectures,
            new_column = 'prefectures'
        )

        # 市区町村
        add_locality_df =self.df_merge.process(
            key_df = add_prefectures_df,  # 更新したDataFrameを入れる
            column = 'address_components',
            add_func = self.gm_geocoding._get_locality,
            new_column = 'locality'
        )


        # photo_url
        add_photo_url_df =self.df_merge.process(
            key_df = add_locality_df,  # 更新したDataFrameを入れる
            column = 'photos',
            add_func = self.gm_geocoding.generate_photo_url,
            new_column = 'photo_url'
        )

        # nave_position
        add_nave_position_df =self.df_merge.process2(
            key_df = add_photo_url_df,  # 更新したDataFrameを入れる
        )

        # review
        add_review_df =self.df_merge.review_merge_process(
            key_df = add_nave_position_df,  # 更新したDataFrameを入れる
            column = 'reviews',
            add_func = self.gm_geocoding._sort_reviews_to_df,
        )

        # review_html
        add_review_html_df = self.html_replace.df_to_row_process(
            df=add_review_df,
            template_dir=self.method_dir,
            file_name='review_format.html'
        )


        # 必要な情報に絞り込み
        sorted_df = self.gm_geocoding.df_sort(
            df=add_review_html_df,
            new_order=['name', 'photos', 'geometry.viewport.northeast.lat', 'geometry.viewport.northeast.lng', 'geometry.viewport.southwest.lat', 'geometry.viewport.southwest.lng', 'japanese_address', 'formatted_phone_number', 'business_hours', 'close_days', 'website', 'prefectures', 'locality', 'photo_url','center_lat', 'center_lng', 'review1_rating', 'review2_rating', 'review3_rating', 'review4_rating', 'review5_rating', 'review1_name', 'review2_name', 'review3_name', 'review4_name', 'review5_name', 'review1_text', 'review2_text', 'review3_text', 'review4_text', 'review5_text', 'review_html']
        )

        # 全てを置換
        self.html_replace.df_to_html(
            df=sorted_df,
            input_word=input_word,
            template_dir=self.method_dir,
            file_name='template.html',
            update_file_path=self.result_html_data_dir
        )

        self.logger.info(f"html生成完了: 「result_output」の中にある「result_html_data」をご確認ください")



# ----------------------------------------------------------------------------------
# installer/result_output/ までのフルパス
# インスタンス化させてから使う

    def _get_file_path_in_result_output(self, file_name):
        try:
            self.logger.info(f"******** _get_file_path_in_result_output start ********")

            self.logger.debug(f"file_name: {file_name}")

            flow_dir = (os.path.abspath(__file__))

            src_dir = os.path.dirname(flow_dir)

            installer_dir = os.path.dirname(src_dir)

            file_path = os.path.join(installer_dir, 'result_output', file_name)

            self.logger.warning(f"file_path: {file_path}")

            self.logger.info(f"******** _get_file_path_in_result_output end ********")

            return file_path

        except Exception as e:
            self.logger.error(f"_get_file_path_in_result_output 処理中にエラーが発生: {e}")
            messagebox.showerror("エラー", f"処理中にエラーが発生しました: {e}")
            sys.exit(1)


# ----------------------------------------------------------------------------------
# installer/result_output/ までのフルパス
# インスタンス化させてから使う

    def _get_method_full_dir(self):
        try:
            self.logger.info(f"******** _get_method_full_dir start ********")

            flow_dir = (os.path.abspath(__file__))

            src_dir = os.path.dirname(flow_dir)

            method_dir = os.path.join(src_dir, 'method')

            self.logger.warning(f"method_dir: {method_dir}")

            self.logger.info(f"******** _get_method_full_dir end ********")

            return method_dir

        except Exception as e:
            self.logger.error(f"_get_method_full_dir 処理中にエラーが発生: {e}")
            messagebox.showerror("エラー", f"処理中にエラーが発生しました: {e}")
            sys.exit(1)


# ----------------------------------------------------------------------------------

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# テスト実施

# if __name__ == '__main__':
#     query='調布 工務店'
#     input_word='正確性'
#     flow_process= Flow()
#     flow_process.flow_main(query=query, input_word=input_word)
