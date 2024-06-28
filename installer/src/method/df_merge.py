# coding: utf-8
# ----------------------------------------------------------------------------------
# 2023/6/4更新

# ----------------------------------------------------------------------------------
import time, sys
import pandas as pd
from tkinter import messagebox


# 自作モジュール
from .base.B_googleMap import GoogleMapBase
from .base.utils import Logger

###############################################################


class DfProcessMerge(GoogleMapBase):
    def __init__(self, api_key, debug_mode=False):
        self.api_key = api_key

        # logger
        self.setup_logger = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.setup_logger.setup_logger()


###############################################################
# ----------------------------------------------------------------------------------
# Override

    # DataFrameからcolumnデータを抽出
    def _get_column_data(self, key_df, column):
        return super()._get_column_data(key_df, column)

    # 処理
    def add_process_value_in_list(self, list_data, add_func):
        return super().add_process_value_in_list(list_data, add_func)

    def _get_navi_position(self, df):
        return super()._get_navi_position(df)


    def get_reviews(self, list_data):
        return super().get_reviews(list_data)


    # DataFrameにする
    def _to_df(self, list_data, new_column):
        return super()._to_df(list_data, new_column)


    # 既存のDataFrameに結合させる
    def _df_marge(self, key_df, add_df):
        return super()._df_marge(key_df, add_df)


    def review_add_process_value_in_list(self, list_data, add_func):
        return super().review_add_process_value_in_list(list_data, add_func)


# ----------------------------------------------------------------------------------
# 既存のDataFrameから指定のcolumnの値を取得
# →各値に処理を加える→SeriesをDataFrameにして結合

    def process(self, key_df, column, add_func, new_column):
        try:
            self.logger.info(f"******** DfProcessMerge 開始 ********")

            # 特定のcolumnのデータを取得
            list_data =self._get_column_data(key_df, column)
            self.logger.debug(f"list_data: {list_data}")
            time.sleep(2)

            # columnの値、それぞれに処理を加えてリストにする
            fixed_data = self.add_process_value_in_list(list_data=list_data, add_func=add_func)
            time.sleep(2)

            # リストをDataFrameにする
            add_df = self._to_df(fixed_data, new_column=new_column)
            time.sleep(2)

            # DataFrameを結合させる
            new_df = self._df_marge(key_df=key_df, add_df=add_df)
            time.sleep(2)

            self.logger.info(f"******** DfProcessMerge 終了 ********")

            # new_df.to_csv('installer/result_output/merge_df.csv')

            return new_df

        except Exception as e:
            self.logger.error(f"DfProcessMerge 処理中にエラーが発生: {e}")
            messagebox.showerror("エラー", f"処理中にエラーが発生しました: {e}")
            sys.exit(1)

# ----------------------------------------------------------------------------------
# DataFrameから直接結合

    def process2(self, key_df):
        try:
            self.logger.info(f"******** DfProcessMerge 開始 ********")

            # 特定のcolumnのデータを取得
            add_df =self._get_navi_position(df=key_df)
            time.sleep(2)

            # DataFrameを結合させる
            new_df = self._df_marge(key_df=key_df, add_df=add_df)
            time.sleep(2)

            self.logger.info(f"******** DfProcessMerge 終了 ********")

            # new_df.to_csv('installer/result_output/merge_df.csv')

            return new_df

        except Exception as e:
            self.logger.error(f"DfProcessMerge 処理中にエラーが発生: {e}")
            messagebox.showerror("エラー", f"処理中にエラーが発生しました: {e}")
            sys.exit(1)

# ----------------------------------------------------------------------------------


    def review_merge_process(self, key_df, column, add_func):
        try:
            self.logger.info(f"******** review_merge_process 開始 ********")

            # 特定のcolumnのデータを取得
            list_data =self._get_column_data(key_df, column)
            self.logger.debug(f"list_data: {list_data}")
            time.sleep(2)

            # columnの値、それぞれに処理を加えてリストにする
            list_data = self.review_add_process_value_in_list(list_data=list_data, add_func=add_func)
            time.sleep(2)

            add_df = pd.DataFrame(list_data)

            # DataFrameを結合させる
            new_df = self._df_marge(key_df=key_df, add_df=add_df)
            time.sleep(2)

            self.logger.info(f"******** review_merge_process 終了 ********")

            # new_df.to_csv('installer/result_output/merge_df.csv')

            return new_df

        except Exception as e:
            self.logger.error(f"review_merge_process 処理中にエラーが発生: {e}")
            messagebox.showerror("エラー", f"処理中にエラーが発生しました: {e}")
            sys.exit(1)

# ----------------------------------------------------------------------------------
# reviewのhtmlをmergeさせる

    def review_html_merge_process(self, key_df, column, add_func, new_column):
        try:
            self.logger.info(f"******** review_html_merge_process 開始 ********")

            # 特定のcolumnのデータを取得
            list_data =self._get_column_data(key_df, column)
            self.logger.debug(f"list_data: {list_data}")
            time.sleep(2)

            # columnの値、それぞれに処理を加えてリストにする
            fixed_data = self.add_process_value_in_list(list_data=list_data, add_func=add_func)
            time.sleep(2)

            # リストをDataFrameにする
            add_df = self._to_df(fixed_data, new_column=new_column)
            time.sleep(2)

            # DataFrameを結合させる
            new_df = self._df_marge(key_df=key_df, add_df=add_df)
            time.sleep(2)

            self.logger.info(f"******** review_html_merge_process 終了 ********")

            # new_df.to_csv('installer/result_output/merge_df.csv')

            return new_df

        except Exception as e:
            self.logger.error(f"review_html_merge_process 処理中にエラーが発生: {e}")
            messagebox.showerror("エラー", f"処理中にエラーが発生しました: {e}")
            sys.exit(1)

# ----------------------------------------------------------------------------------