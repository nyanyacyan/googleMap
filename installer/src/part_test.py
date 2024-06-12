# coding: utf-8
# ----------------------------------------------------------------------------------
# 2023/4/19 更新

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
import os
import const
from dotenv import load_dotenv
from method.base.B_googleMap import GoogleMapBase
from method.base.B_html_replace import HtmlReplaceBase
from method.get_gm_df import GetGMPlaceDf
from method.df_merge import DfProcessMerge
from method.base.utils import Logger

load_dotenv()

####################################################################################


class Test:
    def __init__(self, debug_mode=False):
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


####################################################################################
# ----------------------------------------------------------------------------------

    def test_main(self, query):
        key_df = self.get_gm_df.process(
            query=query,
        )


        # review
        add_review_df =self.df_merge.review_merge_process(
            key_df = key_df,  # 更新したDataFrameを入れる
            column = 'reviews',
            add_func = self.gm_geocoding._sort_reviews_to_df,
        )

        # review_html
        add_review_html_df = self.html_replace.df_to_row_process(
            df=add_review_df,
            template_dir='installer/src/method/input_data',
            file_name='review_format.html'
        )


        return add_review_html_df



# ----------------------------------------------------------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# テスト実施

if __name__ == '__main__':
    query='調布 工務店'
    test_process= Test()
    test_process.test_main(query=query)
