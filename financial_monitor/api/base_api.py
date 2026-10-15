"""
API基类
"""
import logging
import requests
from typing import Dict, Any, Optional

class BaseAPI:
    """
    API基类，提供基本的HTTP请求功能
    """
    
    def __init__(self, api_key: str = "", base_url: str = ""):
        """
        初始化API基类
        
        @param {string} api_key - API密钥
        @param {string} base_url - API基础URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.logger = logging.getLogger("financial_monitor.api")
        
    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        发送GET请求
        
        @param {string} endpoint - API端点
        @param {Dict} params - 请求参数
        @returns {Dict} 响应数据
        """
        if params is None:
            params = {}
            
        # 如果有API密钥，添加到请求参数中
        if self.api_key:
            params["apikey"] = self.api_key
            
        url = f"{self.base_url}{endpoint}"
        self.logger.debug(f"GET请求: {url}, 参数: {params}")
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()  # 如果HTTP错误，抛出异常
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API请求失败: {str(e)}")
            raise
            
    def _post(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        发送POST请求
        
        @param {string} endpoint - API端点
        @param {Dict} data - 请求数据
        @param {Dict} params - 请求参数
        @returns {Dict} 响应数据
        """
        if params is None:
            params = {}
            
        # 如果有API密钥，添加到请求参数中
        if self.api_key:
            params["apikey"] = self.api_key
            
        url = f"{self.base_url}{endpoint}"
        self.logger.debug(f"POST请求: {url}, 参数: {params}, 数据: {data}")
        
        try:
            response = requests.post(url, json=data, params=params, timeout=10)
            response.raise_for_status()  # 如果HTTP错误，抛出异常
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API请求失败: {str(e)}")
            raise 