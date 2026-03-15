"""
股票订单管理测试
"""

import os
import sys
import json
import unittest
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_order import StockOrderManager
from config import DATA_DIR


class TestStockOrderManager(unittest.TestCase):
    """测试股票订单管理器"""

    def setUp(self):
        """设置测试环境"""
        self.order_manager = StockOrderManager()
        # 备份原始订单文件
        self.order_file = os.path.join(DATA_DIR, "orders", "orders.json")
        self.backup_file = os.path.join(DATA_DIR, "orders", "orders_backup.json")
        if os.path.exists(self.order_file):
            os.rename(self.order_file, self.backup_file)
        # 确保订单文件存在且为空
        os.makedirs(os.path.dirname(self.order_file), exist_ok=True)
        with open(self.order_file, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    def tearDown(self):
        """清理测试环境"""
        # 恢复原始订单文件
        if os.path.exists(self.backup_file):
            os.rename(self.backup_file, self.order_file)
        elif os.path.exists(self.order_file):
            os.remove(self.order_file)

    def test_add_order(self):
        """测试添加订单"""
        order_id = self.order_manager.add_order(
            stock_code="600000",
            stock_name="浦发银行",
            buy_time="2026-03-14 10:00:00",
            buy_price=8.50,
            stock_type="A股"
        )
        self.assertIsNotNone(order_id)
        self.assertTrue(order_id.startswith("ORDER_"))

        # 验证订单是否添加成功
        orders = self.order_manager.get_all_orders()
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]["stock_code"], "600000")
        self.assertEqual(orders[0]["stock_name"], "浦发银行")
        self.assertEqual(orders[0]["buy_time"], "2026-03-14 10:00:00")
        self.assertEqual(orders[0]["buy_price"], 8.50)
        self.assertEqual(orders[0]["stock_type"], "A股")
        self.assertEqual(orders[0]["status"], "持有")

    def test_get_all_orders(self):
        """测试获取所有订单"""
        # 添加两个订单
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
            buy_time="2026-03-14 11:00:00",
            buy_price=180.50,
            stock_type="美股"
        )

        orders = self.order_manager.get_all_orders()
        self.assertEqual(len(orders), 2)

    def test_get_order_by_id(self):
        """测试根据ID获取订单"""
        # 添加订单
        order_id = self.order_manager.add_order(
            stock_code="600000",
            stock_name="浦发银行",
            buy_time="2026-03-14 10:00:00",
            buy_price=8.50,
            stock_type="A股"
        )

        # 获取订单
        order = self.order_manager.get_order_by_id(order_id)
        self.assertIsNotNone(order)
        self.assertEqual(order["order_id"], order_id)
        self.assertEqual(order["stock_code"], "600000")

        # 获取不存在的订单
        non_existent_order = self.order_manager.get_order_by_id("ORDER_9999999999")
        self.assertIsNone(non_existent_order)

    def test_update_order_status(self):
        """测试更新订单状态"""
        # 添加订单
        order_id = self.order_manager.add_order(
            stock_code="600000",
            stock_name="浦发银行",
            buy_time="2026-03-14 10:00:00",
            buy_price=8.50,
            stock_type="A股"
        )

        # 更新状态
        success = self.order_manager.update_order_status(order_id, "已卖出")
        self.assertTrue(success)

        # 验证状态是否更新
        order = self.order_manager.get_order_by_id(order_id)
        self.assertEqual(order["status"], "已卖出")
        self.assertIn("update_time", order)

        # 更新不存在的订单
        success = self.order_manager.update_order_status("ORDER_9999999999", "已卖出")
        self.assertFalse(success)

    def test_delete_order(self):
        """测试删除订单"""
        # 添加订单
        order_id = self.order_manager.add_order(
            stock_code="600000",
            stock_name="浦发银行",
            buy_time="2026-03-14 10:00:00",
            buy_price=8.50,
            stock_type="A股"
        )

        # 删除订单
        success = self.order_manager.delete_order(order_id)
        self.assertTrue(success)

        # 验证订单是否删除
        orders = self.order_manager.get_all_orders()
        self.assertEqual(len(orders), 0)

        # 删除不存在的订单
        success = self.order_manager.delete_order("ORDER_9999999999")
        self.assertFalse(success)

    def test_get_orders_by_stock_type(self):
        """测试根据股票类型获取订单"""
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
            buy_time="2026-03-14 11:00:00",
            buy_price=180.50,
            stock_type="美股"
        )
        self.order_manager.add_order(
            stock_code="0700",
            stock_name="腾讯控股",
            buy_time="2026-03-14 12:00:00",
            buy_price=380.00,
            stock_type="港股"
        )

        # 获取A股订单
        a_stocks = self.order_manager.get_orders_by_stock_type("A股")
        self.assertEqual(len(a_stocks), 1)
        self.assertEqual(a_stocks[0]["stock_type"], "A股")

        # 获取美股订单
        us_stocks = self.order_manager.get_orders_by_stock_type("美股")
        self.assertEqual(len(us_stocks), 1)
        self.assertEqual(us_stocks[0]["stock_type"], "美股")

        # 获取港股订单
        hk_stocks = self.order_manager.get_orders_by_stock_type("港股")
        self.assertEqual(len(hk_stocks), 1)
        self.assertEqual(hk_stocks[0]["stock_type"], "港股")

    def test_get_orders_by_status(self):
        """测试根据状态获取订单"""
        # 添加不同状态的订单
        order_id1 = self.order_manager.add_order(
            stock_code="600000",
            stock_name="浦发银行",
            buy_time="2026-03-14 10:00:00",
            buy_price=8.50,
            stock_type="A股"
        )
        order_id2 = self.order_manager.add_order(
            stock_code="AAPL",
            stock_name="苹果公司",
            buy_time="2026-03-14 11:00:00",
            buy_price=180.50,
            stock_type="美股"
        )

        # 更新一个订单的状态
        self.order_manager.update_order_status(order_id2, "已卖出")

        # 获取持有状态的订单
        holding_orders = self.order_manager.get_orders_by_status("持有")
        self.assertEqual(len(holding_orders), 1)
        self.assertEqual(holding_orders[0]["status"], "持有")

        # 获取已卖出状态的订单
        sold_orders = self.order_manager.get_orders_by_status("已卖出")
        self.assertEqual(len(sold_orders), 1)
        self.assertEqual(sold_orders[0]["status"], "已卖出")


if __name__ == '__main__':
    unittest.main()