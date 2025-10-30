import inventory
import sales
import file_handler


def main():
    """主程序入口"""
    print("=" * 48)
    print("        欢迎使用美丽花卉管理系统")
    print("=" * 48)
    # 加载数据
    try:
        file_handler.load_products()
        file_handler.load_addons()
    except:
        pass

    # 主菜单循环
    while True:
        print("\n@@@@ 美丽花卉管理系统 @@@@")
        print("1. 库存管理")
        print("2. 销售管理")
        print("3. 退出系统")
        option = input("请输入选项：").strip()

        if option == "1":
            inventory.inventory_menu()
        elif option == "2":
            sales.sales_menu()
        elif option == "3":
            print("bye~ 欢迎下次使用！")
            exit()  
        else:
            print("无效选项，请重试")


if __name__ == "__main__":
    main()