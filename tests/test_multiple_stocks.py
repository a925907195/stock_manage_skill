#!/usr/bin/env python3
"""
测试多个股票的信息获取
"""

import os
import sys

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_info import StockInfoFetcher

# 测试获取多个股票的信息
def test_multiple_stocks():
    test_stocks = [
        {'code': '002594', 'name': '比亚迪（A股）'},
        {'code': '600519', 'name': '贵州茅台（A股）'},
        {'code': '000001', 'name': '平安银行（A股）'}
    ]
    
    fetcher = StockInfoFetcher()
    
    for stock in test_stocks:
        print(f"\n测试获取{stock['name']}的股票信息...")
        stock_info = fetcher.fetch_and_save_stock_info(stock['code'])
        if stock_info:
            print(f"{stock['name']}当前价格: {stock_info['current_price']}")
            print(f"{stock['name']}涨跌幅: {stock_info['price_change_percent']}%")
            print(f"数据来源: {stock_info.get('data_source', '未知')}")
            print(f"数据已保存到: data/stock_info/{stock_info['data_date']}/{stock_info['code']}.json")
        else:
            print(f"获取{stock['name']}股票信息失败")

if __name__ == "__main__":
    test_multiple_stocks()