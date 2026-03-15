# 股票管理 Skill - 项目总结

## 项目概述

股票管理Skill是一个基于本地文本存储的股票管理系统，支持股票订单管理和股票信息获取，支持A股、港股、美股等多种股票类型。

## 功能特性

### 1. 股票订单管理
- 支持添加股票买入订单
- 记录买入时间、价格、股票类型（A股、美股、港股等）
- 支持交易平台字段（富途、平安等）
- 支持购买数量字段
- 支持订单状态管理（持有、已卖出、已止损等）
- 支持按股票类型、状态、交易平台筛选订单
- 自动备份机制：每次修改订单时自动备份orders.json
- 备份管理：自动保留最近10个备份文件

### 2. 股票信息获取
- 支持A股、港股、美股多市场股票信息获取
- 优先使用腾讯证券API获取实时数据
- 支持多数据源备用机制（akshare、yfinance、Yahoo Finance API）
- 自动识别股票代码市场类型
- 每日JSON文件存储：每天一个JSON文件记录所有股票信息
- 自动清理30天前的旧数据
- 无需API Key，直接使用公开API

### 3. 日志管理
- 自动清理7天前的旧日志文件
- 支持查看日志文件列表
- 支持查看日志目录大小
- 支持删除指定日志文件

## 项目结构

```
stock_predict_skill/
├── config.py              # 配置文件
├── __init__.py            # 包初始化
├── main.py                # 主入口
├── stock_order.py         # 股票订单管理模块
├── stock_info.py          # 股票信息获取模块
├── log_manager.py         # 日志管理模块
├── command_parser.py      # 命令解析脚本
├── openclaw_entry.py     # OpenClaw入口脚本
├── requirements.txt      # 依赖包列表
├── SKILL.md             # Skill配置文档（OpenClaw使用）
├── data/                # 数据存储目录
│   ├── orders/          # 订单信息
│   │   ├── orders.json
│   │   └── orders.json_*  # 历史备份（保留最近10个）
│   ├── stock_info/     # 股票信息（按日期分目录）
│   │   └── 20260315/
│   │       └── stock_info_20260315.json  # 每日JSON文件
│   └── logs/           # 日志文件
│       ├── stock_order_20260315.log
│       ├── stock_info_20260315.log
│       └── log_manager_20260315.log
├── docs/                # 文档目录
│   ├── PROJECT_SUMMARY.md
│   └── README.md
└── tests/               # 测试目录
    ├── test_stock_order.py
    ├── test_stock_info.py
    ├── test_pure_codes.py
    ├── test_shanghai_stock.py
    ├── test_optimized_fetch.py
    ├── test_all_markets.py
    ├── test_single_stock.py
    ├── test_multiple_stocks.py
    ├── test_order_platform.py
    ├── test_order_quantity.py
    ├── test_stock_info_timestamp.py
    ├── test_log_auto_cleanup.py
    └── test_order_backup.py
```

## 核心模块说明

### 1. stock_order.py - 股票订单管理
- StockOrderManager 类：管理股票订单的CRUD操作
- 支持订单的添加、删除、更新、查询
- 支持按状态、类型、平台筛选订单
- 自动备份机制，保留最近10个备份

### 2. stock_info.py - 股票信息获取
- StockInfoFetcher 类：获取股票信息
- 支持多数据源：腾讯证券API（优先）、akshare、yfinance、Yahoo Finance API
- 自动识别股票代码市场类型
- 每日JSON文件存储，自动清理旧数据

### 3. log_manager.py - 日志管理
- LogManager 类：管理日志文件
- 支持列出日志文件、查看大小、删除日志
- 自动清理7天前的旧日志

### 4. main.py - 命令行接口
- 提供完整的命令行接口
- 支持订单管理、股票信息获取、日志管理

### 5. openclaw_entry.py - OpenClaw集成
- 处理OpenClaw的请求
- 调用相应的功能模块

## 测试

所有核心功能都有对应的测试文件：

| 测试文件 | 功能 |
|---------|------|
| test_stock_order.py | 股票订单管理CRUD |
| test_stock_info.py | 股票信息获取核心功能 |
| test_pure_codes.py | 纯股票代码处理 |
| test_shanghai_stock.py | 上海股票sh前缀识别 |
| test_optimized_fetch.py | 优化后的股票信息获取 |
| test_all_markets.py | 全市场股票信息获取 |
| test_single_stock.py | 单个股票信息获取 |
| test_multiple_stocks.py | 批量股票信息获取 |
| test_order_platform.py | 交易平台字段 |
| test_order_quantity.py | 购买数量字段 |
| test_stock_info_timestamp.py | 每日JSON文件格式 |
| test_log_auto_cleanup.py | 日志自动清理 |
| test_order_backup.py | 订单备份系统 |

所有测试均通过（13/13）。

## 使用示例

### 订单管理
```bash
# 添加订单
python main.py order add --code 600000 --name 浦发银行 --buy-time "2026-03-14 10:00:00" --buy-price 8.50 --type A股 --platform 富途 --quantity 100

# 列出所有订单
python main.py order list

# 按状态筛选订单
python main.py order list --status 持有

# 按股票类型筛选订单
python main.py order list --type 美股

# 按交易平台筛选订单
python main.py order list --platform 富途

# 获取订单详情
python main.py order get --id ORDER_20260314123456_1

# 更新订单状态
python main.py order update --id ORDER_20260314123456_1 --status 已卖出

# 删除订单
python main.py order delete --id ORDER_20260314123456_1

# 查看备份文件
python main.py order backup list

# 清理多余备份（保留最近10个）
python main.py order backup cleanup
```

### 股票信息获取
```bash
# 获取单个股票信息
python main.py stock get --code 002594

# 批量获取多个股票信息
python main.py stock get --code 002594,00700,03690,TSLA

# 获取指定日期的股票信息
python main.py stock get --code 002594 --date 20260315

# 列出所有已获取的股票信息
python main.py stock list

# 查看股票信息详情
python main.py stock show --code 002594

# 清理旧数据（30天前）
python main.py stock cleanup --days 30
```

### 日志管理
```bash
# 列出所有日志文件
python main.py log list

# 查看日志目录大小
python main.py log size

# 清理7天前的旧日志
python main.py log cleanup

# 删除指定日志文件
python main.py log delete --filename stock_info_20260315.log
```

## 数据存储

### 订单数据
- 存储位置：`data/orders/orders.json`
- 备份机制：每次修改自动备份为 `orders.json_YYYYMMDDHHMMSS`
- 备份管理：自动保留最近10个备份

### 股票信息
- 存储位置：`data/stock_info/YYYYMMDD/stock_info_YYYYMMDD.json`
- 存储格式：每天一个JSON文件，包含所有股票信息
- 自动清理：30天前的旧数据

### 日志文件
- 存储位置：`data/logs/`
- 自动清理：7天前的旧日志

## 依赖包

```
requests
akshare
pandas
yfinance
```

## OpenClaw 集成

通过 `openclaw_entry.py` 和 `command_parser.py` 与 OpenClaw 集成，支持自然语言命令调用。

详细集成说明请参考 [SKILL.md](../SKILL.md)。

## 注意事项

1. **数据存储**：所有数据存储在本地文本文件中，无网络依赖
2. **订单管理**：订单信息存储在本地文件中，每次修改自动备份，保留最近10个备份
3. **股票信息**：股票信息按日期分目录存储，每天一个JSON文件记录所有股票信息
4. **API依赖**：股票信息获取需要网络连接，优先使用腾讯证券API
5. **日志管理**：日志文件自动清理7天前的旧数据

## 更新历史

### 2026-03-15
- 添加交易平台字段支持
- 添加购买数量字段支持
- 实现日志自动清理功能
- 简化订单备份系统，只保留最近10个备份
- 简化股票信息存储，改为每日JSON文件格式
- 删除冗余的测试文件和文档
- 更新 SKILL.md 文档