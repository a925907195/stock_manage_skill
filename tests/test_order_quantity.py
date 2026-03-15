#!/usr/bin/env python3
"""
测试股票订单管理功能 - 包含购买数量字段
"""

import os
import sys

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_order import StockOrderManager

def test_order_with_quantity():
    """测试带购买数量的订单管理"""
    print("=" * 80)
    print("测试股票订单管理功能 - 包含购买数量字段")
    print("=" * 80)
    
    manager = StockOrderManager()
    
    # 测试1: 添加订单（带购买数量）
    print("\n1. 测试添加订单（带购买数量）")
    print("-" * 80)
    
    order_id_1 = manager.add_order(
        stock_code="002594",
        stock_name="比亚迪",
        buy_time="2026-03-15 10:30:00",
        buy_price=99.67,
        stock_type="A股",
        platform="富途",
        quantity=100
    )
    print(f"✓ 成功添加订单: {order_id_1}")
    
    order_id_2 = manager.add_order(
        stock_code="00700",
        stock_name="腾讯控股",
        buy_time="2026-03-15 11:00:00",
        buy_price=547.5,
        stock_type="港股",
        platform="平安",
        quantity=50
    )
    print(f"✓ 成功添加订单: {order_id_2}")
    
    order_id_3 = manager.add_order(
        stock_code="TSLA",
        stock_name="特斯拉",
        buy_time="2026-03-15 14:30:00",
        buy_price=391.2,
        stock_type="美股"
    )
    print(f"✓ 成功添加订单: {order_id_3} (无购买数量)")
    
    # 测试2: 查询所有订单
    print("\n2. 测试查询所有订单")
    print("-" * 80)
    orders = manager.get_all_orders()
    print(f"✓ 共找到 {len(orders)} 个订单")
    for order in orders[-3:]:  # 只显示最后3个
        quantity = order.get('quantity', '无') or '无'
        print(f"  {order['order_id']}: {order['stock_name']}({order['stock_code']}) - 数量: {quantity}")
    
    # 测试3: 查询订单详情
    print("\n3. 测试查询订单详情")
    print("-" * 80)
    order = manager.get_order_by_id(order_id_1)
    if order:
        print(f"✓ 订单详情:")
        print(f"  订单ID: {order['order_id']}")
        print(f"  股票: {order['stock_name']}({order['stock_code']})")
        print(f"  买入价格: {order['buy_price']}")
        print(f"  购买数量: {order.get('quantity', '无')} 股")
        print(f"  股票类型: {order['stock_type']}")
        print(f"  交易平台: {order.get('platform', '无')}")
        print(f"  状态: {order['status']}")
    
    # 测试4: 更新订单信息（添加购买数量）
    print("\n4. 测试更新订单信息（添加购买数量）")
    print("-" * 80)
    success = manager.update_order(
        order_id_3,
        quantity=10,
        platform="富途"
    )
    if success:
        print(f"✓ 成功更新订单: {order_id_3}")
        order = manager.get_order_by_id(order_id_3)
        print(f"  新购买数量: {order.get('quantity', '无')} 股")
        print(f"  新交易平台: {order.get('platform', '无')}")
    
    # 测试5: 更新订单状态
    print("\n5. 测试更新订单状态")
    print("-" * 80)
    success = manager.update_order_status(order_id_2, "已卖出")
    if success:
        print(f"✓ 成功更新订单状态: {order_id_2} -> 已卖出")
        order = manager.get_order_by_id(order_id_2)
        print(f"  当前状态: {order['status']}")
    
    # 测试6: 按状态筛选订单
    print("\n6. 测试按状态筛选订单")
    print("-" * 80)
    orders = manager.get_orders_by_status("持有")
    print(f"✓ 持有状态的订单: {len(orders)} 个")
    for order in orders[-3:]:
        quantity = order.get('quantity', '无') or '无'
        print(f"  {order['order_id']}: {order['stock_name']} - 数量: {quantity}")
    
    # 测试7: 按股票类型筛选订单
    print("\n7. 测试按股票类型筛选订单")
    print("-" * 80)
    orders = manager.get_orders_by_stock_type("A股")
    print(f"✓ A股订单: {len(orders)} 个")
    for order in orders[-2:]:
        quantity = order.get('quantity', '无') or '无'
        print(f"  {order['order_id']}: {order['stock_name']} - 数量: {quantity}")
    
    # 测试8: 按交易平台筛选订单
    print("\n8. 测试按交易平台筛选订单")
    print("-" * 80)
    orders = manager.get_orders_by_platform("富途")
    print(f"✓ 富途平台订单: {len(orders)} 个")
    for order in orders[-3:]:
        quantity = order.get('quantity', '无') or '无'
        print(f"  {order['order_id']}: {order['stock_name']}({order['stock_code']}) - 数量: {quantity}")
    
    # 测试9: 删除订单
    print("\n9. 测试删除订单")
    print("-" * 80)
    success = manager.delete_order(order_id_1)
    if success:
        print(f"✓ 成功删除订单: {order_id_1}")
        orders = manager.get_all_orders()
        print(f"  剩余订单: {len(orders)} 个")
    
    # 测试10: 验证删除后的订单列表
    print("\n10. 验证删除后的订单列表")
    print("-" * 80)
    orders = manager.get_all_orders()
    print(f"✓ 当前订单列表（最后3个）:")
    for order in orders[-3:]:
        quantity = order.get('quantity', '无') or '无'
        platform = order.get('platform', '无') or '无'
        print(f"  {order['order_id']}: {order['stock_name']}({order['stock_code']}) - 数量: {quantity} - 平台: {platform} - 状态: {order['status']}")
    
    print("\n" + "=" * 80)
    print("✓ 所有测试完成")
    print("=" * 80)

if __name__ == "__main__":
    test_order_with_quantity()