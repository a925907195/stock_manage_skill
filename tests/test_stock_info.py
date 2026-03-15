#!/usr/bin/env python3
"""
测试股票信息获取功能
"""

import os
import sys

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_info import StockInfoFetcher

if __name__ == "__main__":
    # 创建股票信息获取器
    fetcher = StockInfoFetcher()
    
    # 测试获取比亚迪（A股）的股票信息
    print("测试获取比亚迪（A股）的股票信息...")
    stock_info = fetcher.fetch_and_save_stock_info("002594")
    if stock_info:
        print(f"比亚迪（A股）当前价格: {stock_info['current_price']}")
        print(f"比亚迪（A股）涨跌幅: {stock_info['price_change_percent']}%")
        print(f"数据已保存到: {fetcher._get_file_path(stock_info['data_date'])}")
    else:
        print("获取比亚迪股票信息失败")
    
    # 测试获取美团（港股）的股票信息
    print("\n测试获取美团（港股）的股票信息...")
    stock_info = fetcher.fetch_and_save_stock_info("03690")
    if stock_info:
        print(f"美团（港股）当前价格: {stock_info['current_price']}")
        print(f"美团（港股）涨跌幅: {stock_info['price_change_percent']}%")
        print(f"数据已保存到: {fetcher._get_file_path(stock_info['data_date'])}")
    else:
        print("获取美团股票信息失败")
    
    # 测试获取特斯拉（美股）的股票信息
    print("\n测试获取特斯拉（美股）的股票信息...")
    stock_info = fetcher.fetch_and_save_stock_info("TSLA")
    if stock_info:
        print(f"特斯拉（美股）当前价格: {stock_info['current_price']}")
        print(f"特斯拉（美股）涨跌幅: {stock_info['price_change_percent']}%")
        print(f"数据已保存到: {fetcher._get_file_path(stock_info['data_date'])}")
    else:
        print("获取特斯拉股票信息失败")
    
    # 检查生成的文件
    print("\n检查生成的文件:")
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "stock_info")
    if os.path.exists(data_dir):
        # 获取最新日期目录
        dates = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
        if dates:
            latest_date = sorted(dates)[-1]
            date_dir = os.path.join(data_dir, latest_date)
            print(f"最新日期目录: {date_dir}")
            # 列出该目录下的文件
            files = os.listdir(date_dir)
            print(f"该目录下的文件: {files}")
        else:
            print("未找到日期目录")
    else:
        print("data/stock_info 目录不存在")