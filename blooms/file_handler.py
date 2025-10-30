def load_products():
    """加载Products.txt数据到内存"""
    products = []
    try:
        with open("Products.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                code, name, category, price, status = parts[0], parts[1], parts[2], parts[3], parts[4]
                products.append({
                    "code": code.strip(),
                    "name": name.strip(),
                    "category": category.strip(),
                    "price": price.strip(),  
                    "status": status.strip()
                })
    except FileNotFoundError:
        with open("Products.txt", "w", encoding="utf-8") as f:
            pass
    if len(products) > 0:
        products.pop()
    return products


def save_products(products):
    """保存产品列表到文件"""
    with open("Products.txt", "w", encoding="utf-8") as f:
        for product in products:
            line = f"{product['code']},{product['name']},{product['category']},{product['price']},{product['status']}\n"
            f.write(line)


def load_addons():
    """加载Addons.txt数据"""
    addons = []
    try:
        with open("Addons.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                code, name = line.split(",")
                price = 10  
                addons.append({
                    "code": code.strip(),
                    "name": name.strip(),
                    "price": price,
                    "status": "Available"
                })
    except FileNotFoundError:
        with open("Addons.txt", "w", encoding="utf-8") as f:
            pass
    return addons


def save_addons(addons):
    """保存附加项到文件"""
    with open("Addons.txt", "w", encoding="utf-8") as f:
        for addon in addons:
            line = f"{addon['code']},{addon['name']}\n"
            f.write(line)


def load_orders():
    """加载订单数据"""
    orders = []
    try:
        with open("Orders.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split("|")
                orders.append({
                    "order_id": fields[0],
                    "产品信息": {
                        "code": fields[1],
                        "name": fields[2],
                        "price": fields[3]  
                    },
                    "addon_info": {
                        "code": fields[4],
                        "name": fields[5],
                        "price": fields[6]
                    },
                    "客户信息": {
                        "name": fields[7],
                        "recipient": fields[8],
                        "message": fields[9]
                    },
                    "配送信息": {
                        "type": fields[10],
                        "address": fields[11],
                        "date": fields[12],
                        "same_day": fields[13],
                        "fee": fields[14]
                    },
                    "总金额": fields[15],
                    "status": fields[16]
                })
    except FileNotFoundError:
        with open("Orders.txt", "w", encoding="utf-8") as f:
            pass
    return orders


def save_order(order):
    """保存新订单"""
    with open("Orders.txt", "a", encoding="utf-8") as f:
        addon_code = order["addon_info"]["code"] if order["addon_info"]["code"] != "0" else "0"
        addon_name = order["addon_info"]["name"] if addon_code != "0" else "无"
        addon_price = order["addon_info"]["price"] if addon_code != "0" else 0
        line = (f"{order['order_id']}|{order['产品信息']['code']}|{order['产品信息']['name']}|{order['产品信息']['price']}|"
                f"{addon_code}|{addon_name}|{addon_price}|{order['客户信息']['name']}|{order['客户信息']['recipient']}|"
                f"{order['配送信息']['type']}|{order['配送信息']['address']}|{order['配送信息']['date']}|"
                f"{order['配送信息']['fee']}|{order['总金额']}|{order['status']}\n")
        f.write(line)


def get_next_order_id():
    """生成下一个订单ID（有重复风险）"""
    orders = load_orders()
    if not orders:
        return "BBO-23-0001"
    first_id = orders[0]["order_id"]
    last_num = int(first_id.split("-")[-1])
    next_num = last_num + 1
    return f"BBO-23-{next_num}"