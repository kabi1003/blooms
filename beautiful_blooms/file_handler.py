def load_products():
    """加载Products.txt数据到内存，返回产品列表（列表嵌套字典）"""
    products = []
    try:
        with open("Products.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()  # 去除换行符/空格
                if not line:
                    continue  # 跳过空行
                code, name, category, price, status = line.split(",")
                # 数据类型转换（价格转浮点数，状态去空格）
                products.append({
                    "code": code.strip(),
                    "name": name.strip(),
                    "category": category.strip(),
                    "price": float(price.strip()),
                    "status": status.strip()
                })
    except FileNotFoundError:
        # 首次运行无文件时，创建空文件并返回空列表
        with open("Products.txt", "w", encoding="utf-8") as f:
            pass
    return products


def save_products(products):
    """将内存中的产品列表同步到Products.txt"""
    with open("Products.txt", "w", encoding="utf-8") as f:
        for product in products:
            # 按附录A格式写入：code,name,category,price,status
            line = f"{product['code']},{product['name']},{product['category']},{product['price']},{product['status']}\n"
            f.write(line)


def load_addons():
    """加载Addons.txt数据到内存，返回附加项列表（补充status字段）"""
    addons = []
    try:
        with open("Addons.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # 附录B格式：code,name，补充price（作业未给，默认示例值）和status
                code, name = line.split(",")
                # 实际使用时可修改price为用户输入值，此处暂设为示例价格
                price = 8 if code.strip() == "ADD001" else 12 if code.strip() == "ADD002" else 16
                addons.append({
                    "code": code.strip(),
                    "name": name.strip(),
                    "price": float(price),
                    "status": "Available"
                })
    except FileNotFoundError:
        with open("Addons.txt", "w", encoding="utf-8") as f:
            pass
    return addons


def save_addons(addons):
    """将内存中的附加项列表同步到Addons.txt"""
    with open("Addons.txt", "w", encoding="utf-8") as f:
        for addon in addons:
            # 按附录B格式写入：code,name（price在内存中维护，文件仅存基础信息）
            line = f"{addon['code']},{addon['name']}\n"
            f.write(line)


def load_orders():
    """加载Orders.txt数据到内存，返回订单列表"""
    orders = []
    try:
        with open("Orders.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # 自定义订单格式：order_id|product_code|product_name|product_price|addon_code|addon_name|addon_price|customer_name|recipient_name|message|delivery_type|delivery_address|delivery_date|same_day|delivery_fee|total_amount|status
                fields = line.split("|")
                orders.append({
                    "order_id": fields[0],
                    "product_info": {
                        "code": fields[1],
                        "name": fields[2],
                        "price": float(fields[3])
                    },
                    "addon_info": {
                        "code": fields[4],
                        "name": fields[5],
                        "price": float(fields[6]) if fields[4] != "0" else 0
                    },
                    "customer_info": {
                        "name": fields[7],
                        "recipient": fields[8],
                        "message": fields[9]
                    },
                    "delivery_info": {
                        "type": fields[10],
                        "address": fields[11],
                        "date": fields[12],
                        "same_day": fields[13],
                        "fee": float(fields[14])
                    },
                    "total_amount": float(fields[15]),
                    "status": fields[16]
                })
    except FileNotFoundError:
        with open("Orders.txt", "w", encoding="utf-8") as f:
            pass
    return orders


def save_order(order):
    """将新订单追加到Orders.txt（订单创建时调用）"""
    with open("Orders.txt", "a", encoding="utf-8") as f:
        # 按自定义格式写入，确保字段完整
        addon_code = order["addon_info"]["code"] if order["addon_info"]["code"] != "0" else "0"
        addon_name = order["addon_info"]["name"] if addon_code != "0" else "None"
        addon_price = order["addon_info"]["price"] if addon_code != "0" else 0
        line = (f"{order['order_id']}|{order['product_info']['code']}|{order['product_info']['name']}|{order['product_info']['price']}|"
                f"{addon_code}|{addon_name}|{addon_price}|{order['customer_info']['name']}|{order['customer_info']['recipient']}|"
                f"{order['customer_info']['message']}|{order['delivery_info']['type']}|{order['delivery_info']['address']}|"
                f"{order['delivery_info']['date']}|{order['delivery_info']['same_day']}|{order['delivery_info']['fee']}|"
                f"{order['total_amount']}|{order['status']}\n")
        f.write(line)


def get_next_order_id():
    """生成下一个订单ID（格式BBO-23-XXXX，XXXX从0001递增）"""
    orders = load_orders()
    if not orders:
        return "BBO-23-0001"
    # 提取最后一个订单的ID，截取XXXX部分并加1
    last_id = orders[-1]["order_id"]
    last_num = int(last_id.split("-")[-1])
    next_num = last_num + 1
    return f"BBO-23-{next_num:04d}"  # 格式化为4位，不足补0