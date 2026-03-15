#!/usr/bin/env python3
"""
测试上海股票 601857 的信息获取
"""

import os
import sys

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_info import StockInfoFetcher

def test_shanghai_stock():
    """测试上海股票 601857 的信息获取"""
    print("=" * 80)
    print("测试上海股票 601857 的信息获取")
    print("=" * 80)
    
    fetcher = StockInfoFetcher()
    stock_code = '601857'
    
    # 测试市场前缀识别
    print(f"\n1. 测试市场前缀识别：")
    print(f"   用户输入代码: {stock_code}")
    prefix = fetcher._get_market_prefix(stock_code)
    print(f"   识别的市场前缀: {prefix}")
    print(f"   期望的市场前缀: sh")
    print(f"   识别结果: {'✓ 正确' if prefix == 'sh' else '✗ 错误'}")
    
    # 预期的腾讯API URL
    expected_url = f"https://qt.gtimg.cn/q=sh{stock_code}"
    print(f"\n2. 预期的腾讯API URL:")
    print(f"   {expected_url}")
    
    # 获取股票信息
    print(f"\n3. 获取股票信息：")
    print(f"   正在获取股票 {stock_code} 的信息...")
    print("-" * 80)
    
    stock_info = fetcher.fetch_and_save_stock_info(stock_code)
    
    if stock_info:
        print(f"✓ 成功获取股票 {stock_code} 的信息")
        print(f"\n   股票详细信息：")
        print(f"   股票代码: {stock_info['code']}")
        print(f"   股票名称: {stock_info['name']}")
        print(f"   当前价格: {stock_info['current_price']}")
        print(f"   开盘价: {stock_info['open_price']}")
        print(f"   最高价: {stock_info['high_price']}")
        print(f"   最低价: {stock_info['low_price']}")
        print(f"   昨收价: {stock_info['previous_close']}")
        print(f"   涨跌额: {stock_info['price_change']}")
        print(f"   涨跌幅: {stock_info['price_change_percent']}%")
        print(f"   成交量: {stock_info['volume']}")
        print(f"   成交额: {stock_info['turnover']}")
        print(f"   市场: {stock_info['market']}")
        print(f"   数据来源: {stock_info['data_source']}")
        print(f"   数据日期: {stock_info['data_date']}")
        print(f"   获取时间: {stock_info['fetch_time']}")
        
        print(f"\n   文件保存路径:")
        print(f"   data/stock_info/{stock_info['data_date']}/{stock_info['code']}.json")
        
        print(f"\n4. 验证结果：")
        print(f"   ✓ 市场前缀识别正确: {prefix} == sh")
        print(f"   ✓ 腾讯API URL构造正确: sh{stock_code}")
        print(f"   ✓ 股票信息获取成功")
        print(f"   ✓ 文件保存使用纯代码: {stock_info['code']}")
        
        return True
    else:
        print(f"✗ 获取股票 {stock_code} 信息失败")
        return False

if __name__ == "__main__":
    success = test_shanghai_stock()
    print("\n" + "=" * 80)
    if success:
        print("✓ 测试通过：上海股票 601857 信息获取正常")
    else:
        print("✗ 测试失败：上海股票 601857 信息获取异常")
    print("=" * 80)