from typing import Any, Dict


def success_response(data: Dict[str, Any] = None, message: str = "Success") -> Dict[str, Any]:
    """
    创建一个标准的成功响应格式
    
    :param data: 返回的数据
    :param message: 响应消息
    :return: 标准响应格式
    """
    return {
        "code": 200,
        "message": message,
        "data": data or {}
    }


def error_response(code: int, message: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    创建一个标准的错误响应格式
    
    :param code: 错误代码
    :param message: 错误消息
    :param data: 返回的数据
    :return: 标准响应格式
    """
    return {
        "code": code,
        "message": message,
        "data": data or {}
    }