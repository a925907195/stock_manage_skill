#!/usr/bin/env python3
"""
测试优化后的股票信息获取 - 优先使用腾讯证券API
"""

import os
import sys

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_info import StockInfoFetcher
import json
import os

def test_optimized_fetch():
    """测试优化后的股票信息获取"""
    print("=" * 80)
    print("测试优化后的股票信息获取 - 优先使用腾讯证券API")
    print("=" * 80)
    
    fetcher = StockInfoFetcher()
    
    # 测试股票列表
    test_stocks = [
        {'code': '002594', 'name': '比亚迪', 'market': 'A股'},
        {'code': '00700', 'name': '腾讯控股', 'market': '港股'},
        {'code': '03690', 'name': '美团-W', 'market': '港股'},
        {'code': 'TSLA', 'name': '特斯拉', 'market': '美股'}
    ]
    
    results = []
    
    for stock in test_stocks:
        print(f"\n正在获取 {stock['name']} ({stock['market']}) 的信息...")
        print(f"股票代码: {stock['code']}")
        print("-" * 80)
        
        stock_info = fetcher.fetch_and_save_stock_info(stock['code'])
        
        if stock_info:
            print(f"✓ 成功获取 {stock['name']} 的信息")
            print(f"  股票名称: {stock_info['name']}")
            print(f"  当前价格: {stock_info['current_price']}")
            print(f"  涨跌幅: {stock_info['price_change_percent']}%")
            print(f"  数据来源: {stock_info.get('data_source', '未知')}")
            print(f"  文件路径: data/stock_info/{stock_info['data_date']}/{stock_info['code']}.json")
            
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
    
    # 按市场分类统计
    print("\n按市场分类统计：")
    markets = {}
    for result in results:
        market = result['market']
        if market not in markets:
            markets[market] = {'total': 0, 'success': 0}
        markets[market]['total'] += 1
        if result['success']:
            markets[market]['success'] += 1
    
    for market, stats in markets.items():
        print(f"  {market}: {stats['success']}/{stats['total']} 成功")
    
    print("\n" + "=" * 80)
    
    return results

if __name__ == "__main__":
    results = test_optimized_fetch()