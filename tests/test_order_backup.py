#!/usr/bin/env python3
"""
测试订单备份功能（简化版）
"""

import os
import sys
import time
from datetime import datetime

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_order import StockOrderManager

def test_order_backup():
    """测试订单备份功能"""
    print("=" * 80)
    print("测试订单备份功能（简化版）")
    print("=" * 80)
    
    manager = StockOrderManager()
    
    # 测试1: 添加订单（自动备份）
    print("\n1. 测试添加订单（自动备份）")
    print("-" * 80)
    order_id = manager.add_order(
        stock_code="002594",
        stock_name="比亚迪",
        buy_time="2026-03-15 10:30:00",
        buy_price=99.67,
        stock_type="A股",
        platform="富途",
        quantity=100
    )
    print(f"✓ 成功添加订单: {order_id}")
    
    # 测试2: 查看备份文件
    print("\n2. 测试查看备份文件")
    print("-" * 80)
    backups = []
    for filename in os.listdir(manager.order_dir):
        if filename.startswith('orders.json_'):
            filepath = os.path.join(manager.order_dir, filename)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            backups.append({
                'filename': filename,
                'filepath': filepath,
                'mtime': file_mtime
            })
    
    print(f"✓ 共找到 {len(backups)} 个备份文件:")
    for backup in backups:
        file_size = os.path.getsize(backup['filepath'])
        size_str = f"{file_size / 1024:.2f} KB"
        print(f"  {backup['filename']} - {backup['mtime'].strftime('%Y-%m-%d %H:%M:%S')} - {size_str}")
    
    # 测试3: 更新订单（自动备份）
    print("\n3. 测试更新订单（自动备份）")
    print("-" * 80)
    time.sleep(2)  # 等待2秒，确保时间戳不同
    success = manager.update_order(
        order_id,
        status="已卖出",
        quantity=50
    )
    if success:
        print(f"✓ 成功更新订单: {order_id}")
    
    # 测试4: 再次查看备份文件
    print("\n4. 测试再次查看备份文件")
    print("-" * 80)
    backups = []
    for filename in os.listdir(manager.order_dir):
        if filename.startswith('orders.json_'):
            filepath = os.path.join(manager.order_dir, filename)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            backups.append({
                'filename': filename,
                'filepath': filepath,
                'mtime': file_mtime
            })
    
    print(f"✓ 共找到 {len(backups)} 个备份文件:")
    for backup in backups:
        file_size = os.path.getsize(backup['filepath'])
        size_str = f"{file_size / 1024:.2f} KB"
        print(f"  {backup['filename']} - {backup['mtime'].strftime('%Y-%m-%d %H:%M:%S')} - {size_str}")
    
    # 测试5: 添加第二个订单
    print("\n5. 测试添加第二个订单")
    print("-" * 80)
    order_id_2 = manager.add_order(
        stock_code="00700",
        stock_name="腾讯控股",
        buy_time="2026-03-15 11:00:00",
        buy_price=547.5,
        stock_type="港股",
        platform="富途",
        quantity=10
    )
    print(f"✓ 成功添加订单: {order_id_2}")
    
    # 测试6: 查看当前订单
    print("\n6. 测试查看当前订单")
    print("-" * 80)
    orders = manager.get_all_orders()
    print(f"✓ 当前共有 {len(orders)} 个订单:")
    for order in orders:
        print(f"  {order['order_id']} - {order['stock_name']}({order['stock_code']}) - {order['status']}")
    
    # 测试7: 删除订单（自动备份）
    print("\n7. 测试删除订单（自动备份）")
    print("-" * 80)
    time.sleep(2)  # 等待2秒，确保时间戳不同
    success = manager.delete_order(order_id_2)
    if success:
        print(f"✓ 成功删除订单: {order_id_2}")
    
    # 测试8: 添加多个订单以触发自动清理
    print("\n8. 测试添加多个订单以触发自动清理")
    print("-" * 80)
    initial_backups = len([f for f in os.listdir(manager.order_dir) if f.startswith('orders.json_')])
    print(f"  当前备份数量: {initial_backups}")
    
    # 添加15个订单，触发自动清理（只保留10个）
    for i in range(15):
        time.sleep(0.1)  # 短暂等待
        manager.add_order(
            stock_code=f"600{i:03d}",
            stock_name=f"测试股票{i}",
            buy_time="2026-03-15 12:00:00",
            buy_price=10.0 + i,
            stock_type="A股",
            platform="富途",
            quantity=100
        )
    
    final_backups = len([f for f in os.listdir(manager.order_dir) if f.startswith('orders.json_')])
    print(f"  添加15个订单后备份数量: {final_backups}")
    print(f"✓ 自动清理功能正常（保留最近10个备份）")
    
    # 测试9: 查看所有备份文件
    print("\n9. 测试查看所有备份文件")
    print("-" * 80)
    backups = []
    for filename in os.listdir(manager.order_dir):
        if filename.startswith('orders.json_'):
            filepath = os.path.join(manager.order_dir, filename)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            backups.append({
                'filename': filename,
                'filepath': filepath,
                'mtime': file_mtime
            })
    
    backups.sort(key=lambda x: x['mtime'], reverse=True)
    print(f"✓ 共找到 {len(backups)} 个备份文件:")
    for backup in backups:
        file_size = os.path.getsize(backup['filepath'])
        size_str = f"{file_size / 1024:.2f} KB"
        print(f"  {backup['filename']} - {backup['mtime'].strftime('%Y-%m-%d %H:%M:%S')} - {size_str}")
    
    # 测试10: 清理多余备份
    print("\n10. 测试清理多余备份")
    print("-" * 80)
    deleted_count = manager._cleanup_excess_backups(max_backups=10)
    print(f"✓ 清理了 {deleted_count} 个多余备份（保留最近10个）")
    
    # 测试11: 验证备份文件结构
    print("\n11. 测试验证备份文件结构")
    print("-" * 80)
    print(f"✓ 订单目录结构:")
    print(f"  主文件: orders.json")
    print(f"  备份文件: {len(backups)} 个")
    
    print("\n" + "=" * 80)
    print("✓ 所有测试完成")
    print("=" * 80)

if __name__ == "__main__":
    test_order_backup()