# coding: utf-8
# ----------------------------------------------------------------------------------
# 2023/4/19 更新

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
import os
import const
from dotenv import load_dotenv
from method.base.B_googleMap import GoogleMapBase
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


####################################################################################
# ----------------------------------------------------------------------------------

    def test_main(self, query):
        key_df = self.get_gm_df.process(
            query=query,
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
            column = 'opening_hours.periods',
            add_func = self.gm_geocoding.get_business_hour,
            new_column = 'business_hours'
        )

        # 定休日
        add_close_days_df =self.df_merge.process(
            key_df = add_business_hours,  # 更新したDataFrameを入れる
            column = 'opening_hours.periods',
            add_func = self.gm_geocoding.get_close_days,
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

        # 町名
        add_sublocality_df =self.df_merge.process(
            key_df = add_locality_df,  # 更新したDataFrameを入れる
            column = 'address_components',
            add_func = self.gm_geocoding._get_sublocality,
            new_column = 'sublocality'
        )


        # 必要な情報に絞り込み
        # sorted_df = self.gm_geocoding.df_sort(
        #     df=Last_df,
        #     new_order=['name', 'photos', 'geometry.viewport.northeast.lat', 'geometry.viewport.northeast.lng', 'geometry.viewport.southwest.lat', 'geometry.viewport.southwest.lng', 'japanese_address', 'formatted_phone_number', 'business_hours', 'close_days', 'url', 'reviews']
        # )


        return add_sublocality_df



# TODO DataFrameに追加するもの
# TODO 都道府県を追加
# TODO 市区町村を追加
# TODO 町名を追加
# TODO  写真のリンク先
# TODO  レビューを追加（1から5までの3項目）



# ----------------------------------------------------------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# テスト実施

if __name__ == '__main__':
    query='調布 工務店'
    test_process= Test()
    test_process.test_main(query=query)
