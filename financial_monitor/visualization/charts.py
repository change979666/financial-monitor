"""
图表可视化工具
"""
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

class ChartGenerator:
    """
    图表生成器类
    """
    
    def __init__(self, output_dir: str = "charts"):
        """
        初始化图表生成器
        
        @param {string} output_dir - 图表输出目录
        """
        self.output_dir = output_dir
        
        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # 设置中文字体支持
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        
    def plot_gold_price(self, data: List[Dict[str, Any]], 
                       title: str = "黄金价格走势图",
                       save_path: Optional[str] = None) -> str:
        """
        绘制黄金价格走势图
        
        @param {List[Dict]} data - 黄金价格数据列表
        @param {string} title - 图表标题
        @param {string} save_path - 保存路径，如果为None则自动生成
        @returns {string} 图表文件路径
        """
        # 提取数据
        dates = [datetime.fromisoformat(item['date'].replace('Z', '+00:00')) 
                if 'Z' in item['date'] else datetime.fromisoformat(item['date']) 
                for item in data]
        prices = [item['price'] for item in data]
        
        # 创建图表
        plt.figure(figsize=(12, 6))
        plt.plot(dates, prices, 'g-', linewidth=2)
        plt.title(title)
        plt.xlabel('日期')
        plt.ylabel('价格 (USD/oz)')
        plt.grid(True)
        
        # 设置x轴日期格式
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//10)))
        plt.gcf().autofmt_xdate()
        
        # 如果未提供保存路径，生成默认路径
        if save_path is None:
            save_path = os.path.join(self.output_dir, f"gold_price_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
        # 保存图表
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        
        return save_path
        
    def plot_usdx_index(self, data: List[Dict[str, Any]], 
                       title: str = "美元指数走势图",
                       save_path: Optional[str] = None) -> str:
        """
        绘制美元指数走势图
        
        @param {List[Dict]} data - 美元指数数据列表
        @param {string} title - 图表标题
        @param {string} save_path - 保存路径，如果为None则自动生成
        @returns {string} 图表文件路径
        """
        # 提取数据
        dates = [datetime.fromisoformat(item['date'].replace('Z', '+00:00')) 
                if 'Z' in item['date'] else datetime.fromisoformat(item['date']) 
                for item in data]
        values = [item['value'] for item in data]
        
        # 创建图表
        plt.figure(figsize=(12, 6))
        plt.plot(dates, values, 'b-', linewidth=2)
        plt.title(title)
        plt.xlabel('日期')
        plt.ylabel('美元指数')
        plt.grid(True)
        
        # 设置x轴日期格式
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//10)))
        plt.gcf().autofmt_xdate()
        
        # 如果未提供保存路径，生成默认路径
        if save_path is None:
            save_path = os.path.join(self.output_dir, f"usdx_index_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
        # 保存图表
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        
        return save_path
        
    def plot_exchange_rate(self, data: List[Dict[str, Any]], 
                         base_currency: str = "CNY", target_currency: str = "USD",
                         title: Optional[str] = None,
                         save_path: Optional[str] = None) -> str:
        """
        绘制汇率走势图
        
        @param {List[Dict]} data - 汇率数据列表
        @param {string} base_currency - 基础货币代码
        @param {string} target_currency - 目标货币代码
        @param {string} title - 图表标题
        @param {string} save_path - 保存路径，如果为None则自动生成
        @returns {string} 图表文件路径
        """
        # 提取数据
        dates = [datetime.fromisoformat(item['date'].replace('Z', '+00:00')) 
                if 'Z' in item['date'] else datetime.fromisoformat(item['date']) 
                for item in data]
        rates = [item['rate'] for item in data]
        
        # 设置标题
        if title is None:
            title = f"{base_currency}/{target_currency} 汇率走势图"
            
        # 创建图表
        plt.figure(figsize=(12, 6))
        plt.plot(dates, rates, 'r-', linewidth=2)
        plt.title(title)
        plt.xlabel('日期')
        plt.ylabel(f'汇率 ({base_currency}/{target_currency})')
        plt.grid(True)
        
        # 设置x轴日期格式
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//10)))
        plt.gcf().autofmt_xdate()
        
        # 如果未提供保存路径，生成默认路径
        if save_path is None:
            save_path = os.path.join(self.output_dir, f"{base_currency}_{target_currency}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
        # 保存图表
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        
        return save_path
        
    def plot_correlation(self, gold_data: List[Dict[str, Any]], usdx_data: List[Dict[str, Any]],
                        title: str = "黄金价格与美元指数相关性",
                        save_path: Optional[str] = None) -> Tuple[str, float]:
        """
        绘制黄金价格与美元指数相关性图
        
        @param {List[Dict]} gold_data - 黄金价格数据列表
        @param {List[Dict]} usdx_data - 美元指数数据列表
        @param {string} title - 图表标题
        @param {string} save_path - 保存路径，如果为None则自动生成
        @returns {Tuple[string, float]} 图表文件路径和相关系数
        """
        # 提取数据
        gold_prices = np.array([item['price'] for item in gold_data])
        usdx_values = np.array([item['value'] for item in usdx_data])
        
        # 计算相关系数
        correlation = np.corrcoef(gold_prices, usdx_values)[0, 1]
        
        # 创建图表
        plt.figure(figsize=(10, 8))
        plt.scatter(usdx_values, gold_prices, alpha=0.6)
        plt.title(f"{title} (相关系数: {correlation:.3f})")
        plt.xlabel('美元指数')
        plt.ylabel('黄金价格 (USD/oz)')
        plt.grid(True)
        
        # 添加趋势线
        z = np.polyfit(usdx_values, gold_prices, 1)
        p = np.poly1d(z)
        plt.plot(usdx_values, p(usdx_values), "r--", linewidth=2)
        
        # 如果未提供保存路径，生成默认路径
        if save_path is None:
            save_path = os.path.join(self.output_dir, f"correlation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
        # 保存图表
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        
        return save_path, correlation 