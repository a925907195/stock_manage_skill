#!/usr/bin/env python3
"""
测试股票信息管理 - 每日JSON文件格式
"""

import os
import sys
import json

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_info import StockInfoFetcher

def test_stock_info_daily_file():
    """测试每日JSON文件格式的股票信息管理"""
    print("=" * 80)
    print("测试股票信息管理 - 每日JSON文件格式")
    print("=" * 80)
    
    fetcher = StockInfoFetcher()
    
    # 测试1: 获取股票信息（保存到每日JSON文件）
    print("\n1. 测试获取股票信息（保存到每日JSON文件）")
    print("-" * 80)
    stock_info = fetcher.fetch_and_save_stock_info("002594")
    if stock_info:
        print(f"✓ 成功获取比亚迪信息")
        print(f"  当前价格: {stock_info['current_price']}")
        print(f"  获取时间: {stock_info['fetch_time']}")
        print(f"  文件路径: {fetcher._get_file_path(stock_info['data_date'])}")
    
    # 测试2: 再次获取同一股票（更新每日JSON文件）
    print("\n2. 测试再次获取同一股票（更新每日JSON文件）")
    print("-" * 80)
    import time
    time.sleep(2)  # 等待2秒，确保时间戳不同
    stock_info = fetcher.fetch_and_save_stock_info("002594")
    if stock_info:
        print(f"✓ 成功获取比亚迪信息（第二次）")
        print(f"  当前价格: {stock_info['current_price']}")
        print(f"  获取时间: {stock_info['fetch_time']}")
    
    # 测试3: 获取其他股票信息
    print("\n3. 测试获取其他股票信息")
    print("-" * 80)
    stock_info = fetcher.fetch_and_save_stock_info("00700")
    if stock_info:
        print(f"✓ 成功获取腾讯控股信息")
        print(f"  当前价格: {stock_info['current_price']}")
        print(f"  获取时间: {stock_info['fetch_time']}")
    
    stock_info = fetcher.fetch_and_save_stock_info("TSLA")
    if stock_info:
        print(f"✓ 成功获取特斯拉信息")
        print(f"  当前价格: {stock_info['current_price']}")
        print(f"  获取时间: {stock_info['fetch_time']}")
    
    # 测试4: 查看每日JSON文件内容
    print("\n4. 查看每日JSON文件内容")
    print("-" * 80)
    file_path = fetcher._get_file_path("20260315")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ 每日JSON文件包含 {len(data)} 个股票:")
        for code, info in data.items():
            print(f"  {code} - {info['name']} - {info['current_price']} - {info['fetch_time']}")
    
    # 测试5: 测试清理旧数据（30天前）
    print("\n5. 测试清理旧数据（30天前）")
    print("-" * 80)
    deleted_count = fetcher._cleanup_old_data(days=30)
    print(f"✓ 清理了 {deleted_count} 个旧数据目录")
    
    # 测试6: 验证文件结构
    print("\n6. 验证文件结构")
    print("-" * 80)
    date_dir = os.path.join(fetcher.stock_info_dir, "20260315")
    if os.path.exists(date_dir):
        files = sorted(os.listdir(date_dir))
        print(f"✓ 当前日期目录下的文件:")
        print(f"  总数: {len(files)}")
        daily_file = [f for f in files if f.startswith('stock_info_')]
        print(f"  每日JSON文件: {len(daily_file)}")
        if daily_file:
            print(f"  文件名: {daily_file[0]}")
    
    print("\n" + "=" * 80)
    print("✓ 所有测试完成")
    print("=" * 80)

if __name__ == "__main__":
    test_stock_info_daily_file()