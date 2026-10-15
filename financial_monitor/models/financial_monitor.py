"""
金融数据监控主类
"""
import os
import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

import requests

from financial_monitor.api.gold_api import GoldPriceAPI
from financial_monitor.api.usdx_api import USDXIndexAPI
from financial_monitor.api.forex_api import ForexAPI
from financial_monitor.utils.logger import setup_logger
from financial_monitor.utils.config import Config

class FinancialMonitor:
    """
    金融数据监控主类，用于获取和处理各种金融数据
    """
    
    def __init__(self, api_key: Optional[str] = None, config_path: Optional[str] = None):
        """
        初始化金融监控器
        
        @param {string} api_key - API密钥，如果不提供则从环境变量或配置文件读取
        @param {string} config_path - 配置文件路径
        """
        self.logger = setup_logger("financial_monitor")
        self.config = Config(config_path)
        
        # 如果提供了API密钥，优先使用提供的密钥
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = self.config.get("api_key", os.getenv("FINANCIAL_API_KEY", ""))
        
        # 初始化各API客户端
        self.gold_api = GoldPriceAPI(self.api_key)
        self.usdx_api = USDXIndexAPI(self.api_key)
        self.forex_api = ForexAPI(self.api_key)
        
        self.logger.info("金融监控系统初始化完成")
    
    def get_gold_price(self) -> Dict[str, Any]:
        """
        获取最新黄金价格
        
        @returns {Dict} 包含金价信息的字典
        """
        try:
            return self.gold_api.get_latest_price()
        except Exception as e:
            self.logger.error(f"获取金价失败: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def get_usdx_index(self) -> Dict[str, Any]:
        """
        获取美元指数数据
        
        @returns {Dict} 包含美元指数信息的字典
        """
        try:
            return self.usdx_api.get_latest_index()
        except Exception as e:
            self.logger.error(f"获取美元指数失败: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def get_rmb_exchange_rate(self, target_currency: str = "USD") -> Dict[str, Any]:
        """
        获取人民币汇率
        
        @param {string} target_currency - 目标货币代码，默认为USD
        @returns {Dict} 包含汇率信息的字典
        """
        try:
            return self.forex_api.get_exchange_rate("CNY", target_currency)
        except Exception as e:
            self.logger.error(f"获取汇率失败: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def get_all_data(self) -> Dict[str, Any]:
        """
        获取所有金融数据
        
        @returns {Dict} 包含所有金融数据的字典
        """
        return {
            "gold_price": self.get_gold_price(),
            "usdx_index": self.get_usdx_index(),
            "rmb_usd_rate": self.get_rmb_exchange_rate("USD"),
            "rmb_eur_rate": self.get_rmb_exchange_rate("EUR"),
            "timestamp": datetime.now().isoformat()
        }
    
    def monitor(self, interval: int = 60) -> None:
        """
        持续监控金融数据
        
        @param {int} interval - 监控间隔，单位为秒
        """
        self.logger.info(f"开始监控金融数据，间隔 {interval} 秒")
        try:
            while True:
                data = self.get_all_data()
                self.logger.info(f"金价: {data['gold_price'].get('price', 'N/A')} USD/oz, "
                                f"美元指数: {data['usdx_index'].get('value', 'N/A')}, "
                                f"美元/人民币: {data['rmb_usd_rate'].get('rate', 'N/A')}")
                time.sleep(interval)
        except KeyboardInterrupt:
            self.logger.info("监控已停止")
        except Exception as e:
            self.logger.error(f"监控过程中出错: {str(e)}") 