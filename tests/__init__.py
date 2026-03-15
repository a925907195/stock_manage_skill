"""
测试模块
"""

import os
import sys
import json
import unittest
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_order import StockOrderManager


class TestStockOrderManager(unittest.TestCase):
    """测试股票订单管理器"""

    def setUp(self):
        """测试前准备"""
        self.order_manager = StockOrderManager()

    def test_add_order(self):
        """测试添加订单"""
        print("\n测试添加订单...")
        order_id = self.order_manager.add_order(
            stock_code="600000",
            stock_name="浦发银行",
            buy_time="2026-03-14 10:00:00",
            buy_price=8.50,
            stock_type="A股"
        )
        print(f"成功添加订单: {order_id}")
        self.assertIsNotNone(order_id)

    def test_get_all_orders(self):
        """测试获取所有订单"""
        print("\n测试获取所有订单...")
        orders = self.order_manager.get_all_orders()
        print(f"获取到 {len(orders)} 个订单")
        self.assertIsInstance(orders, list)

    def test_get_order_by_id(self):
        """测试根据ID获取订单"""
        print("\n测试根据ID获取订单...")
        order_id = self.order_manager.add_order(
            stock_code="600000",
            stock_name="浦发银行",
            buy_time="2026-03-14 10:00:00",
            buy_price=8.50,
            stock_type="A股"
        )
        order = self.order_manager.get_order_by_id(order_id)
        print(f"成功获取订单: {order['order_id']} - {order['stock_name']}")
        self.assertIsNotNone(order)

    def test_update_order_status(self):
        """测试更新订单状态"""
        print("\n测试更新订单状态...")
        order_id = self.order_manager.add_order(
            stock_code="600000",
            stock_name="浦发银行",
            buy_time="2026-03-14 10:00:00",
            buy_price=8.50,
            stock_type="A股"
        )
        success = self.order_manager.update_order_status(order_id, "已卖出")
        print(f"更新订单状态: {'成功' if success else '失败'}")
        self.assertTrue(success)

    def test_delete_order(self):
        """测试删除订单"""
        print("\n测试删除订单...")
        order_id = self.order_manager.add_order(
            stock_code="600000",
            stock_name="浦发银行",
            buy_time="2026-03-14 10:00:00",
            buy_price=8.50,
            stock_type="A股"
        )
        success = self.order_manager.delete_order(order_id)
        print(f"删除订单: {'成功' if success else '失败'}")
        self.assertTrue(success)

    def test_filter_orders_by_type(self):
        """测试按股票类型筛选订单"""
        print("\n测试按股票类型筛选订单...")
        # 清空现有订单
        for order in self.order_manager.get_all_orders():
            self.order_manager.delete_order(order['order_id'])
        # 添加不同类型的订单
        self.order_manager.add_order(
            stock_code="600000",
            stock_name="浦发银行",
            buy_time="2026-03-14 10:00:00",
            buy_price=8.50,
            stock_type="A股"
        )
        self.order_manager.add_order(
            stock_code="AAPL",
            stock_name="苹果公司",
            buy_time="2026-03-14 10:00:00",
            buy_price=150.00,
            stock_type="美股"
        )
        # 筛选A股订单
        a_stocks = self.order_manager.get_orders_by_stock_type("A股")
        print(f"筛选出 {len(a_stocks)} 个A股订单")
        self.assertEqual(len(a_stocks), 1)

    def test_filter_orders_by_status(self):
        """测试按状态筛选订单"""
        print("\n测试按状态筛选订单...")
        # 清空现有订单
        for order in self.order_manager.get_all_orders():
            self.order_manager.delete_order(order['order_id'])
        # 添加不同状态的订单
        order_id = self.order_manager.add_order(
            stock_code="600000",
            stock_name="浦发银行",
            buy_time="2026-03-14 10:00:00",
            buy_price=8.50,
            stock_type="A股"
        )
        self.order_manager.update_order_status(order_id, "已卖出")
        # 筛选已卖出订单
        sold_orders = self.order_manager.get_orders_by_status("已卖出")
        print(f"筛选出 {len(sold_orders)} 个已卖出订单")
        self.assertEqual(len(sold_orders), 1)


def run_all_tests():
    """运行所有测试"""
    print("=" * 80)
    print("开始运行股票订单管理 Skill 测试")
    print("=" * 80)

    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加测试用例
    suite.addTests(loader.loadTestsFromTestCase(TestStockOrderManager))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 打印测试总结
    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)
    print(f"测试用例总数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("=" * 80)

    return result.wasSuccessful()


if __name__ == "__main__":
    # 运行所有测试
    success = run_all_tests()
    sys.exit(0 if success else 1)