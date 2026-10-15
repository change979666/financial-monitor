"""
金融数据监控系统主程序
"""
import os
import sys
import argparse
import logging
from datetime import datetime, timedelta

from financial_monitor.models.financial_monitor import FinancialMonitor
from financial_monitor.utils.logger import setup_logger
from financial_monitor.utils.config import Config
from financial_monitor.visualization.charts import ChartGenerator

def parse_args():
    """
    解析命令行参数
    
    @returns {Namespace} 解析后的参数
    """
    parser = argparse.ArgumentParser(description="金融数据实时监控系统")
    
    # 基本参数
    parser.add_argument("-c", "--config", help="配置文件路径")
    parser.add_argument("-k", "--api-key", help="API密钥")
    parser.add_argument("-i", "--interval", type=int, default=60, help="监控间隔（秒）")
    parser.add_argument("-l", "--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="日志级别")
    parser.add_argument("-o", "--output-dir", default="output", help="输出目录")
    
    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # monitor命令
    monitor_parser = subparsers.add_parser("monitor", help="实时监控金融数据")
    monitor_parser.add_argument("-t", "--time", type=int, default=0, help="监控时长（分钟），0表示持续监控")
    
    # fetch命令
    fetch_parser = subparsers.add_parser("fetch", help="获取金融数据")
    fetch_parser.add_argument("--gold", action="store_true", help="获取黄金价格")
    fetch_parser.add_argument("--usdx", action="store_true", help="获取美元指数")
    fetch_parser.add_argument("--forex", action="store_true", help="获取汇率")
    fetch_parser.add_argument("--all", action="store_true", help="获取所有数据")
    
    # chart命令
    chart_parser = subparsers.add_parser("chart", help="生成数据图表")
    chart_parser.add_argument("--type", choices=["gold", "usdx", "forex", "correlation"], required=True, help="图表类型")
    chart_parser.add_argument("--days", type=int, default=30, help="历史数据天数")
    chart_parser.add_argument("--title", help="图表标题")
    chart_parser.add_argument("--output", help="输出文件路径")
    
    return parser.parse_args()

def main():
    """
    主函数
    """
    # 解析命令行参数
    args = parse_args()
    
    # 设置日志
    log_level = getattr(logging, args.log_level)
    logger = setup_logger("financial_monitor", log_level)
    
    # 确保输出目录存在
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    try:
        # 初始化金融监控器
        monitor = FinancialMonitor(api_key=args.api_key, config_path=args.config)
        
        # 根据命令执行相应操作
        if args.command == "monitor":
            # 实时监控
            logger.info("开始实时监控金融数据...")
            if args.time > 0:
                # 限时监控
                import time
                end_time = datetime.now() + timedelta(minutes=args.time)
                logger.info(f"将监控 {args.time} 分钟，直到 {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                try:
                    while datetime.now() < end_time:
                        data = monitor.get_all_data()
                        logger.info(f"金价: {data['gold_price'].get('price', 'N/A')} USD/oz, "
                                  f"美元指数: {data['usdx_index'].get('value', 'N/A')}, "
                                  f"美元/人民币: {data['rmb_usd_rate'].get('rate', 'N/A')}")
                        time.sleep(args.interval)
                except KeyboardInterrupt:
                    logger.info("监控已停止")
            else:
                # 持续监控
                monitor.monitor(interval=args.interval)
                
        elif args.command == "fetch":
            # 获取数据
            if args.all or (not args.gold and not args.usdx and not args.forex):
                # 获取所有数据
                data = monitor.get_all_data()
                print(f"金价: {data['gold_price'].get('price', 'N/A')} USD/oz")
                print(f"美元指数: {data['usdx_index'].get('value', 'N/A')}")
                print(f"美元/人民币汇率: {data['rmb_usd_rate'].get('rate', 'N/A')}")
                print(f"欧元/人民币汇率: {data['rmb_eur_rate'].get('rate', 'N/A')}")
            else:
                # 获取指定数据
                if args.gold:
                    gold_data = monitor.get_gold_price()
                    print(f"金价: {gold_data.get('price', 'N/A')} USD/oz")
                    
                if args.usdx:
                    usdx_data = monitor.get_usdx_index()
                    print(f"美元指数: {usdx_data.get('value', 'N/A')}")
                    
                if args.forex:
                    usd_rate = monitor.get_rmb_exchange_rate("USD")
                    eur_rate = monitor.get_rmb_exchange_rate("EUR")
                    print(f"美元/人民币汇率: {usd_rate.get('rate', 'N/A')}")
                    print(f"欧元/人民币汇率: {eur_rate.get('rate', 'N/A')}")
                    
        elif args.command == "chart":
            # 生成图表
            chart_generator = ChartGenerator(output_dir=args.output_dir)
            
            # 获取历史数据
            start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
            end_date = datetime.now().strftime("%Y-%m-%d")
            
            if args.type == "gold":
                # 绘制黄金价格图表
                gold_data = monitor.gold_api.get_historical_prices(start_date, end_date)
                title = args.title or "黄金价格走势图"
                chart_path = chart_generator.plot_gold_price(gold_data, title=title, save_path=args.output)
                print(f"图表已保存至: {chart_path}")
                
            elif args.type == "usdx":
                # 绘制美元指数图表
                usdx_data = monitor.usdx_api.get_historical_index(start_date, end_date)
                title = args.title or "美元指数走势图"
                chart_path = chart_generator.plot_usdx_index(usdx_data, title=title, save_path=args.output)
                print(f"图表已保存至: {chart_path}")
                
            elif args.type == "forex":
                # 绘制汇率图表
                forex_data = monitor.forex_api.get_historical_rates("CNY", "USD", start_date, end_date)
                title = args.title or "人民币/美元汇率走势图"
                chart_path = chart_generator.plot_exchange_rate(forex_data, "CNY", "USD", title=title, save_path=args.output)
                print(f"图表已保存至: {chart_path}")
                
            elif args.type == "correlation":
                # 绘制相关性图表
                gold_data = monitor.gold_api.get_historical_prices(start_date, end_date)
                usdx_data = monitor.usdx_api.get_historical_index(start_date, end_date)
                title = args.title or "黄金价格与美元指数相关性"
                chart_path, correlation = chart_generator.plot_correlation(gold_data, usdx_data, title=title, save_path=args.output)
                print(f"图表已保存至: {chart_path}")
                print(f"相关系数: {correlation:.3f}")
        else:
            # 默认显示帮助信息
            print("请指定命令。使用 --help 查看帮助信息。")
            
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main()) 