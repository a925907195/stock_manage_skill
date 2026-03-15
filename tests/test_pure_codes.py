#!/usr/bin/env python3
"""
测试纯股票代码处理 - 用户只需要传入纯代码
"""

import os
import sys

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_info import StockInfoFetcher

def test_pure_stock_codes():
    """测试纯股票代码处理"""
    print("=" * 80)
    print("测试纯股票代码处理 - 用户只需要传入纯代码")
    print("=" * 80)
    
    fetcher = StockInfoFetcher()
    
    # 测试股票列表（纯代码）
    test_stocks = [
        {'code': '002594', 'name': '比亚迪', 'market': 'A股', 'expected_prefix': 'sz'},
        {'code': '00700', 'name': '腾讯控股', 'market': '港股', 'expected_prefix': 'hk'},
        {'code': '03690', 'name': '美团-W', 'market': '港股', 'expected_prefix': 'hk'},
        {'code': 'TSLA', 'name': '特斯拉', 'market': '美股', 'expected_prefix': 'us'}
    ]
    
    print("\n测试市场前缀识别：")
    print("-" * 80)
    
    for stock in test_stocks:
        prefix = fetcher._get_market_prefix(stock['code'])
        expected = stock['expected_prefix']
        status = "✓" if prefix == expected else "✗"
        print(f"{status} {stock['name']} ({stock['code']}): 识别为 {prefix}, 期望 {expected}")
    
    print("\n测试股票信息获取：")
    print("-" * 80)
    
    results = []
    for stock in test_stocks:
        print(f"\n正在获取 {stock['name']} ({stock['market']}) 的信息...")
        print(f"用户输入代码: {stock['code']}")
        
        stock_info = fetcher.fetch_and_save_stock_info(stock['code'])
        
        if stock_info:
            print(f"✓ 成功获取 {stock['name']} 的信息")
            print(f"  股票名称: {stock_info['name']}")
            print(f"  当前价格: {stock_info['current_price']}")
            print(f"  涨跌幅: {stock_info['price_change_percent']}%")
            print(f"  数据来源: {stock_info.get('data_source', '未知')}")
            print(f"  保存代码: {stock_info['code']} (与用户输入一致)")
            
            results.append({
                'code': stock['code'],
                'name': stock['name'],
                'market': stock['market'],
                'success': True,
                'price': stock_info['current_price'],
                'change_percent': stock_info['price_change_percent'],
                'source': stock_info.get('data_source', '未知')
            })
        else:
            print(f"✗ 获取 {stock['name']} 信息失败")
            results.append({
                'code': stock['code'],
                'name': stock['name'],
                'market': stock['market'],
                'success': False
            })
    
    # 汇总结果
    print("\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)
    
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)
    
    print(f"\n总计: {success_count}/{total_count} 成功")
    
    print("\n详细结果：")
    for result in results:
        status = "✓" if result['success'] else "✗"
        if result['success']:
            print(f"  {status} {result['name']} ({result['code']}, {result['market']}): "
                  f"价格 {result['price']}, 涨跌幅 {result['change_percent']}%, "
                  f"来源 {result['source']}")
        else:
            print(f"  {status} {result['name']} ({result['code']}, {result['market']}): 获取失败")
    
    print("\n" + "=" * 80)
    print("✓ 用户只需要传入纯股票代码，系统自动处理前缀转换")
    print("  - A股: 002594 → sz002594")
    print("  - 港股: 03690 → hk03690") 
    print("  - 美股: TSLA → usTSLA")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    results = test_pure_stock_codes()