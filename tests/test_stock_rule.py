"""
测试股票交易规则管理功能
"""

import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_rule import StockRuleManager


def test_add_rule():
    """测试添加规则"""
    print("测试添加规则...")
    rule_manager = StockRuleManager()

    # 添加买入规则
    buy_conditions = [
        {"indicator": "price", "operator": "<", "value": "ma20"}
    ]
    buy_actions = [
        {"type": "buy", "quantity": 100}
    ]
    rule_id_1 = rule_manager.add_rule(
        rule_type="买入规则",
        rule_name="价格低于均线买入",
        rule_description="当价格低于20日均线时买入",
        conditions=buy_conditions,
        actions=buy_actions,
        stock_type="A股"
    )
    print(f"添加买入规则成功: {rule_id_1}")

    # 添加卖出规则
    sell_conditions = [
        {"indicator": "profit_percent", "operator": ">", "value": 10}
    ]
    sell_actions = [
        {"type": "sell", "quantity": "all"}
    ]
    rule_id_2 = rule_manager.add_rule(
        rule_type="卖出规则",
        rule_name="盈利超过10%卖出",
        rule_description="当盈利超过10%时卖出",
        conditions=sell_conditions,
        actions=sell_actions,
        stock_type="A股"
    )
    print(f"添加卖出规则成功: {rule_id_2}")

    # 添加特定股票的规则
    specific_conditions = [
        {"indicator": "price", "operator": ">", "value": 100}
    ]
    specific_actions = [
        {"type": "notification", "message": "价格超过100"}
    ]
    rule_id_3 = rule_manager.add_rule(
        rule_type="买入规则",
        rule_name="特定股票买入",
        rule_description="特定股票价格超过100时通知",
        conditions=specific_conditions,
        actions=specific_actions,
        stock_type="A股",
        stock_code="600000"
    )
    print(f"添加特定股票规则成功: {rule_id_3}")

    print("添加规则测试完成\n")
    return [rule_id_1, rule_id_2, rule_id_3]


def test_get_all_rules():
    """测试获取所有规则"""
    print("测试获取所有规则...")
    rule_manager = StockRuleManager()

    rules = rule_manager.get_all_rules()
    print(f"共找到 {len(rules)} 个规则:")
    for rule in rules:
        print(f"  - {rule['rule_id']}: {rule['rule_name']} ({rule['rule_type']})")

    print("获取所有规则测试完成\n")


def test_get_rule_by_id(rule_id):
    """测试根据ID获取规则"""
    print(f"测试获取规则详情: {rule_id}")
    rule_manager = StockRuleManager()

    rule = rule_manager.get_rule_by_id(rule_id)
    if rule:
        print(f"规则ID: {rule['rule_id']}")
        print(f"规则名称: {rule['rule_name']}")
        print(f"规则类型: {rule['rule_type']}")
        print(f"规则描述: {rule['rule_description']}")
        print(f"触发条件: {json.dumps(rule['conditions'], ensure_ascii=False)}")
        print(f"执行动作: {json.dumps(rule['actions'], ensure_ascii=False)}")
        print(f"股票类型: {rule.get('stock_type', '未指定')}")
        print(f"股票代码: {rule.get('stock_code', '未指定')}")
        print(f"启用状态: {rule.get('enabled', True)}")
    else:
        print(f"未找到规则: {rule_id}")

    print("获取规则详情测试完成\n")


def test_update_rule(rule_id):
    """测试更新规则"""
    print(f"测试更新规则: {rule_id}")
    rule_manager = StockRuleManager()

    # 更新规则名称和描述
    success = rule_manager.update_rule(
        rule_id,
        rule_name="更新后的规则名称",
        rule_description="更新后的规则描述"
    )
    if success:
        print(f"更新规则成功: {rule_id}")
        # 验证更新
        rule = rule_manager.get_rule_by_id(rule_id)
        print(f"新规则名称: {rule['rule_name']}")
        print(f"新规则描述: {rule['rule_description']}")
    else:
        print(f"更新规则失败: {rule_id}")

    print("更新规则测试完成\n")


def test_toggle_rule(rule_id):
    """测试切换规则状态"""
    print(f"测试切换规则状态: {rule_id}")
    rule_manager = StockRuleManager()

    # 获取当前状态
    rule = rule_manager.get_rule_by_id(rule_id)
    original_status = rule.get('enabled', True)
    print(f"原始状态: {'启用' if original_status else '禁用'}")

    # 切换状态
    success = rule_manager.toggle_rule(rule_id)
    if success:
        # 验证切换
        rule = rule_manager.get_rule_by_id(rule_id)
        new_status = rule.get('enabled', True)
        print(f"新状态: {'启用' if new_status else '禁用'}")
        print(f"切换规则状态成功")
    else:
        print(f"切换规则状态失败")

    print("切换规则状态测试完成\n")


def test_get_rules_by_type():
    """测试根据类型获取规则"""
    print("测试根据类型获取规则...")
    rule_manager = StockRuleManager()

    # 获取买入规则
    buy_rules = rule_manager.get_rules_by_type("买入规则")
    print(f"买入规则数量: {len(buy_rules)}")
    for rule in buy_rules:
        print(f"  - {rule['rule_id']}: {rule['rule_name']}")

    # 获取卖出规则
    sell_rules = rule_manager.get_rules_by_type("卖出规则")
    print(f"卖出规则数量: {len(sell_rules)}")
    for rule in sell_rules:
        print(f"  - {rule['rule_id']}: {rule['rule_name']}")

    print("根据类型获取规则测试完成\n")


def test_get_rules_by_stock_type():
    """测试根据股票类型获取规则"""
    print("测试根据股票类型获取规则...")
    rule_manager = StockRuleManager()

    # 获取A股规则
    a_share_rules = rule_manager.get_rules_by_stock_type("A股")
    print(f"A股规则数量: {len(a_share_rules)}")
    for rule in a_share_rules:
        print(f"  - {rule['rule_id']}: {rule['rule_name']}")

    print("根据股票类型获取规则测试完成\n")


def test_get_rules_by_stock_code():
    """测试根据股票代码获取规则"""
    print("测试根据股票代码获取规则...")
    rule_manager = StockRuleManager()

    # 获取特定股票的规则
    stock_rules = rule_manager.get_rules_by_stock_code("600000")
    print(f"股票600000的规则数量: {len(stock_rules)}")
    for rule in stock_rules:
        print(f"  - {rule['rule_id']}: {rule['rule_name']}")

    print("根据股票代码获取规则测试完成\n")


def test_get_enabled_rules():
    """测试获取启用的规则"""
    print("测试获取启用的规则...")
    rule_manager = StockRuleManager()

    enabled_rules = rule_manager.get_enabled_rules()
    print(f"启用的规则数量: {len(enabled_rules)}")
    for rule in enabled_rules:
        print(f"  - {rule['rule_id']}: {rule['rule_name']}")

    print("获取启用规则测试完成\n")


def test_delete_rule(rule_id):
    """测试删除规则"""
    print(f"测试删除规则: {rule_id}")
    rule_manager = StockRuleManager()

    success = rule_manager.delete_rule(rule_id)
    if success:
        print(f"删除规则成功: {rule_id}")
        # 验证删除
        rule = rule_manager.get_rule_by_id(rule_id)
        if rule is None:
            print("验证删除成功: 规则已不存在")
        else:
            print("验证删除失败: 规则仍然存在")
    else:
        print(f"删除规则失败: {rule_id}")

    print("删除规则测试完成\n")


def test_backup():
    """测试备份功能"""
    print("测试备份功能...")
    rule_manager = StockRuleManager()

    # 查看备份文件
    import os
    backup_files = []
    for filename in os.listdir(rule_manager.rule_dir):
        if filename.startswith('rules.json_'):
            backup_files.append(filename)

    print(f"当前备份文件数量: {len(backup_files)}")
    for filename in backup_files:
        print(f"  - {filename}")

    # 测试清理多余备份
    deleted_count = rule_manager._cleanup_excess_backups(max_backups=10)
    print(f"清理了 {deleted_count} 个多余备份")

    print("备份功能测试完成\n")


def main():
    """主测试函数"""
    print("=" * 60)
    print("开始测试股票交易规则管理功能")
    print("=" * 60 + "\n")

    try:
        # 测试添加规则
        rule_ids = test_add_rule()

        # 测试获取所有规则
        test_get_all_rules()

        # 测试根据ID获取规则
        if rule_ids:
            test_get_rule_by_id(rule_ids[0])

        # 测试更新规则
        if rule_ids:
            test_update_rule(rule_ids[0])

        # 测试切换规则状态
        if rule_ids:
            test_toggle_rule(rule_ids[0])

        # 测试根据类型获取规则
        test_get_rules_by_type()

        # 测试根据股票类型获取规则
        test_get_rules_by_stock_type()

        # 测试根据股票代码获取规则
        test_get_rules_by_stock_code()

        # 测试获取启用的规则
        test_get_enabled_rules()

        # 测试备份功能
        test_backup()

        # 测试删除规则
        if rule_ids:
            test_delete_rule(rule_ids[2])

        print("=" * 60)
        print("所有测试完成")
        print("=" * 60)

    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()