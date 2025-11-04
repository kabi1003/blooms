import inventory  # 导入库存管理模块
import sales      # 导入销售管理模块
import file_handler  # 导入文件操作模块


def main():
    """主程序：启动并显示主菜单"""
    print("=" * 48)
    print("        欢迎使用美丽花卉管理系统")
    print("=" * 48)

    # 程序启动时加载数据（验证文件是否正常）
    print("\n正在加载数据...")
    try:
        file_handler.load_products()
        file_handler.load_addons()
        file_handler.load_orders()
        print("所有数据加载成功！")
    except Exception as e:
        print(f"警告：数据加载错误 - {str(e)}。请检查文件格式。")

    # 主菜单循环
    while True:
        print("\n@@@@ 美丽花卉管理系统 @@@@")
        print("1. 库存管理")
        print("2. 销售管理")
        print("3. 退出系统")
        option = input("请输入选项：").strip()

        if option == "1":
            # 进入库存管理子菜单
            inventory.inventory_menu()
        elif option == "2":
            # 进入销售管理子菜单
            sales.sales_menu()
        elif option == "3":
            # 退出程序
            print("\n感谢使用美丽花卉管理系统，再见！")
            break
        else:
            # 无效输入处理
            print("错误：无效的选项。请输入 1、2 或 3。")


if __name__ == "__main__":
    main()