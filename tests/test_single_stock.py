#!/usr/bin/env python3
"""
测试单个股票的信息获取
"""

import os
import sys

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_info import StockInfoFetcher

# 测试获取单个股票的信息
def test_single_stock(stock_code, stock_name):
    print(f"测试获取{stock_name}的股票信息...")
    fetcher = StockInfoFetcher()
    stock_info = fetcher.fetch_and_save_stock_info(stock_code)
    if stock_info:
        print(f"{stock_name}当前价格: {stock_info['current_price']}")
        print(f"{stock_name}涨跌幅: {stock_info['price_change_percent']}%")
        print(f"数据已保存到: data/stock_info/{stock_info['data_date']}/{stock_info['code']}.json")
        return True
    else:
        print(f"获取{stock_name}股票信息失败")
        return False

if __name__ == "__main__":
    # 只测试比亚迪（A股）
    test_single_stock('002594', '比亚迪（A股）')