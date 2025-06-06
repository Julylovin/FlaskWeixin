def smudge(a, b):
    try:
        # 类型检查确保 a 和 b 是字符串
        if not (isinstance(a, str) and isinstance(b, str)):
            raise TypeError("参数必须是字符串")

        # 安全地转换为浮点数并求和
        result = float(a) + float(b)

        # 构造表达式字符串用于输出
        expression = f"{a}+{b}"

        return expression, result

    except ValueError as ve:
        raise ValueError(f"无法将字符串转换为数字: {ve}")
    except Exception as e:
        raise RuntimeError(f"发生意外错误: {e}")
