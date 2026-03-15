#!/usr/bin/env python3
"""
测试日志自动清理功能
"""

import os
import sys

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from log_manager import LogManager

def test_log_auto_cleanup():
    """测试日志自动清理功能"""
    print("=" * 80)
    print("测试日志自动清理功能")
    print("=" * 80)
    
    log_manager = LogManager()
    
    # 测试1: 列出所有日志文件
    print("\n1. 列出所有日志文件")
    print("-" * 80)
    log_files = log_manager.list_log_files()
    print(f"✓ 共找到 {len(log_files)} 个日志文件:")
    for log_file in log_files[:5]:  # 只显示前5个
        print(f"  {log_file['filename']} - {log_manager.format_size(log_file['size'])}")
    if len(log_files) > 5:
        print(f"  ... 还有 {len(log_files) - 5} 个文件")
    
    # 测试2: 查看日志目录大小
    print("\n2. 查看日志目录大小")
    print("-" * 80)
    log_size = log_manager.get_log_size()
    print(f"✓ 日志目录总大小: {log_manager.format_size(log_size)}")
    
    # 测试3: 清理7天前的旧日志
    print("\n3. 清理7天前的旧日志")
    print("-" * 80)
    deleted_count = log_manager.delete_old_logs(days=7)
    print(f"✓ 清理了 {deleted_count} 个旧日志文件")
    
    # 测试4: 再次查看日志文件
    print("\n4. 再次查看日志文件")
    print("-" * 80)
    log_files = log_manager.list_log_files()
    print(f"✓ 清理后剩余 {len(log_files)} 个日志文件:")
    for log_file in log_files[:5]:  # 只显示前5个
        print(f"  {log_file['filename']} - {log_manager.format_size(log_file['size'])}")
    if len(log_files) > 5:
        print(f"  ... 还有 {len(log_files) - 5} 个文件")
    
    # 测试5: 再次查看日志目录大小
    print("\n5. 再次查看日志目录大小")
    print("-" * 80)
    log_size = log_manager.get_log_size()
    print(f"✓ 清理后日志目录总大小: {log_manager.format_size(log_size)}")
    
    # 测试6: 测试清理30天前的旧日志
    print("\n6. 测试清理30天前的旧日志")
    print("-" * 80)
    deleted_count = log_manager.delete_old_logs(days=30)
    print(f"✓ 清理了 {deleted_count} 个旧日志文件")
    
    # 测试7: 验证清理功能
    print("\n7. 验证清理功能")
    print("-" * 80)
    log_files = log_manager.list_log_files()
    print(f"✓ 最终剩余 {len(log_files)} 个日志文件")
    print(f"  总大小: {log_manager.format_size(log_manager.get_log_size())}")
    
    print("\n" + "=" * 80)
    print("✓ 所有测试完成")
    print("=" * 80)

if __name__ == "__main__":
    test_log_auto_cleanup()