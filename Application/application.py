import flet as ft
import pandas as pd
import os
import json
from pathlib import Path
from CreateSchedule import Scheduling

# デフォルトの設定JSON（サンプル）
ROOT_PATH = Path(__file__).resolve().parent.parent
DEFAULT_SCHEDULE_PATH = os.path.join(ROOT_PATH, "Datas/production_create_description.json")
DEFAULT_PERSONNEL_PATH = os.path.join(ROOT_PATH, "Datas/personnel_limit.json")  # 人数計算の設定ファイル
with open(DEFAULT_SCHEDULE_PATH, 'r', encoding='utf-8') as file:
    DEFAULT_SCHEDULE_CONFIG = json.load(file)
with open(DEFAULT_PERSONNEL_PATH, 'r', encoding='utf-8') as file:
    DEFAULT_PERSONNEL_CONFIG = json.load(file)


class ConfirmDialog(ft.AlertDialog):
    def __init__(self, title, content, on_ok, on_cancel):
        super().__init__(
            modal=True,
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.TextButton("キャンセル", on_click=on_cancel),
                ft.TextButton("OK", on_click=on_ok),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )


class ScheduleConfigView(ft.View):
    def __init__(self, route, config, update_config_callback):
        super().__init__(route)
        self.config = config
        self.update_config_callback = update_config_callback
        self.data_tables = {}  # 各項目のDataTableを格納する辞書
        self.new_key_field = ft.TextField(label="新しいキー", width=200)  # TextFieldをインスタンス変数として定義
        self.snack_bar = None  # SnackBarをインスタンス変数として定義

        # ConfirmDialog をインスタンス化
        self.confirm_dialog = ConfirmDialog(
            title="", content="", on_ok=None, on_cancel=None)

        # 新規キー入力用のコントロール
        self.new_processing_rows = ft.TextField(label="Processing (例: [[1,0],[0,1]])", multiline=True, width=400)
        self.new_description_json = ft.TextField(label="Description (例: {\"項目1\":[1,0], \"項目2\":[0,1]})", multiline=True, width=400)
        self.new_color_field = ft.TextField(label="色 (例: cc0000)", width=200)
        self.add_item_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("新しい設定項目"),
            content=ft.Column([
                self.new_key_field,
                self.new_processing_rows,
                self.new_description_json,
                self.new_color_field,
            ], tight=True),
            actions=[
                ft.TextButton("キャンセル", on_click=self.close_add_item_dialog),
                ft.TextButton("追加", on_click=self.add_new_config_item),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        # AlertDialogをpageに追加
        # self.page.overlay.append(self.add_item_dialog) # ここから移動
        self.build_data_tables()

    def build_data_tables(self):
        """
        設定に基づいてDataTableを構築する
        """
        self.data_tables = {}  # リフレッシュ
        for key, value in self.config.items():
            self.data_tables[key] = {
                "processing": self.create_data_table(key, "processing", value["processing"]),
                "description": self.create_data_table(key, "description", value["description"]),
                "color": ft.TextField(label="色 (例: cc0000)", value=value["color"], width=200),
            }

    def create_data_table(self, main_key, sub_key, data):
        """
        DataTableを作成する
        """
        if isinstance(data, list):  # processing の場合 (2次元配列)
            # dataが空でないリストで、かつ最初の要素がリストであることを確認
            if data and isinstance(data[0], list):
                columns = [ft.DataColumn(ft.Text(f"列{i + 1}")) for i in range(len(data[0]))]  # 列の動的な生成
            else:
                # dataが空リストか、最初の要素がリストでない場合は、列がないDataTableを作成
                columns = []
            rows = []
            for i, row_data in enumerate(data):
                # row_data がリストであることを確認
                if isinstance(row_data, list):
                    cells = [ft.DataCell(ft.TextField(value=str(cell_value), width=70)) for cell_value in row_data]
                    # セルの数が列の数より少ない場合に空のセルを追加
                    while len(cells) < len(columns):
                        cells.append(ft.DataCell(ft.TextField(value="", width=70)))
                else:
                    # row_data がリストでない場合は、エラーメッセージを表示するセルを作成
                    cells = [ft.DataCell(ft.Text(f"Error: Invalid data format - {type(row_data)}"))]
                rows.append(ft.DataRow(cells=cells))

            return ft.DataTable(
                columns=columns,
                rows=rows,
                width=500,
                show_bottom_border=True,
                heading_row_color=ft.Colors.GREY_200,
            )
        elif isinstance(data, dict):  # description の場合 (辞書)
            # 列を動的に生成
            # descriptionのvalueの中で最も要素数が多いリストの要素数に合わせて列を作成
            max_len = 0
            for item_key, item_value in data.items():
                if isinstance(item_value, list):
                    max_len = max(max_len, len(item_value))

            columns = [ft.DataColumn(ft.Text(f"列{i + 1}")) for i in range(max_len)]  # 列数をリストの最大長にする
            columns.insert(0, ft.DataColumn(ft.Text("項目")))  # 最初の列に「項目」を追加

            rows = []
            for item_key, item_value in data.items():
                cells = [ft.DataCell(ft.Text(item_key))]  # 最初のセルに項目名を追加
                if isinstance(item_value, list):
                    for v in item_value:
                        cells.append(ft.DataCell(ft.TextField(value=str(v), width=70)))
                    # リストの要素数が足りない場合に空のセルを追加
                    while len(cells) < len(columns):
                        cells.append(ft.DataCell(ft.TextField(value="", width=70)))
                else:
                    cells.append(ft.DataCell(ft.TextField(value=str(item_value), width=70)))  # リストでない場合はそのまま表示
                rows.append(ft.DataRow(cells=cells))

            return ft.DataTable(
                columns=columns,
                rows=rows,
                width=800,  # DataTableの幅を調整
                show_bottom_border=True,
                heading_row_color=ft.Colors.GREY_200,
            )
        else:
            return ft.Text(f"データ形式が不正です: {type(data)}")  # エラー処理

    def show_message(self, message):
        """
        SnackBarを表示する
        """
        self.snack_bar = ft.SnackBar(ft.Text(message), open=True)
        if self.snack_bar not in self.page.overlay:
            self.page.overlay.append(self.snack_bar)
        self.page.update()

    def open_confirm_dialog(self, key):
        """確認ダイアログを開く"""

        def yes_click(e):
            self.delete_config_item(key)
            self.confirm_dialog.open = False
            self.page.update()

        def no_click(e):
            self.confirm_dialog.open = False
            self.page.update()

        self.confirm_dialog.title = ft.Text("削除確認")
        self.confirm_dialog.content = ft.Text(f"'{key}' を本当に削除しますか？")
        self.confirm_dialog.actions = [
            ft.TextButton("キャンセル", on_click=no_click),
            ft.TextButton("OK", on_click=yes_click),
        ]
        self.confirm_dialog.actions_alignment = ft.MainAxisAlignment.END
        self.page.dialog = self.confirm_dialog
        # ダイアログを表示する前に page.overlay に追加
        if self.confirm_dialog not in self.page.overlay:
            self.page.overlay.append(self.confirm_dialog)
        self.confirm_dialog.open = True
        self.page.update()

    def delete_config_item(self, key):
        """
        設定項目を削除する
        """
        if key in self.config:  # キーが存在するか確認 (削除処理の直前にもう一度確認)
            del self.config[key]
            self.build_data_tables()  # DataTableを再構築

            self.show_message(f"キー '{key}' を削除しました。")

            # 画面を最新のデータで更新
            self.controls.clear()
            self.controls.extend(self.build().controls)  # build()でcontrolsを再生成
            self.page.update()
        else:
            self.show_message(f"キー '{key}' はすでに削除されています。")
            print(f"キー '{key}' はすでに削除されています。")  # デバッグ用
            self.page.update()  # 削除に失敗した場合もUIを更新

    def add_config_item(self, e):
        """
        新しい設定項目を追加する
        """
        self.new_key_field.value = ""  # 初期化
        self.new_processing_rows.value = ""  # 初期化
        self.new_description_json.value = ""  # 初期化
        self.new_color_field.value = ""  # 初期化
        self.page.dialog = self.add_item_dialog
        self.add_item_dialog.open = True
        self.page.update()

    def close_add_item_dialog(self, e):
        self.add_item_dialog.open = False
        self.build_data_tables()  # DataTableを再構築
        self.page.update()

    def add_new_config_item(self, e):
        """
        ダイアログから入力された情報に基づいて新しい設定項目を追加する
        """
        new_key = self.new_key_field.value.strip()
        if not new_key or new_key in self.config:
            self.show_message("無効なキーです")
            return

        try:
            processing_data = json.loads(self.new_processing_rows.value)
            description_data = json.loads(self.new_description_json.value)

            # processing_data の形式を検証
            if not isinstance(processing_data, list) or not all(isinstance(row, list) for row in processing_data):
                self.show_message("Processing の形式が無効です。リストのリストである必要があります。")
                return

            # description_data の形式を検証
            if not isinstance(description_data, dict):
                self.show_message("Description の形式が無効です。辞書である必要があります。")
                return

            # description_data のすべての値がリストであることを検証
            if not all(isinstance(value, list) for value in description_data.values()):
                self.show_message("Description の値はすべてリストである必要があります。")
                return

            color_value = self.new_color_field.value

            self.config[new_key] = {
                "processing": processing_data,
                "description": description_data,
                "color": color_value
            }
            self.build_data_tables()  # DataTableを再構築
            self.show_message(f"キー '{new_key}' を追加しました。")

            # ダイアログを閉じる
            self.add_item_dialog.open = False

            # 画面を最新のデータで更新
            self.controls.clear()
            self.controls.extend(self.build().controls)  # build()でcontrolsを再生成

        except json.JSONDecodeError as err:
            self.show_message(f"JSON形式が無効です: {err}")
            return
        except Exception as ex:
            self.show_message(f"エラーが発生しました: {str(ex)}")
            return
        finally:
            self.page.update()

    def save_config(self, e):
        """
        DataTableのデータをJSON形式に変換して保存する
        """
        new_config = {}
        try:
            for key, value in self.data_tables.items():
                new_config[key] = {}

                # processing
                processing_table = value["processing"]
                processing_data = []
                for row in processing_table.rows:
                    row_data = []
                    for cell in row.cells:
                        try:
                            row_data.append(int(cell.content.value))  # 数値に変換
                        except ValueError:
                            self.show_message(f"数値以外の値が入力されています: {key} - processing")
                            return  # 保存を中断
                    processing_data.append(row_data)
                new_config[key]["processing"] = processing_data

                # description
                description_table = value["description"]
                description_data = {}
                for row in description_table.rows:
                    item_key = row.cells[0].content.value  # 項目名を取得
                    item_value_list = []
                    for cell in row.cells[1:]:  # 2列目以降の値を取得
                        try:
                            item_value_list.append(int(cell.content.value))  # 値をintに変換
                        except ValueError:
                            self.show_message(f"数値以外の値が入力されています: {key} - description - {item_key}")
                            return  # 保存を中断
                    description_data[item_key] = item_value_list
                new_config[key]["description"] = description_data

                # color
                new_config[key]["color"] = value["color"].value

            self.update_config_callback(new_config)
            self.page.go("/")
        except Exception as ex:
            print(ex)  # デバッグ用
            self.show_message(f"保存中にエラーが発生しました: {str(ex)}")
        self.page.update()

    def build(self):
        self.appbar = ft.AppBar(
            title=ft.Text("スケジュール作成詳細設定"),
            bgcolor=ft.Colors.ON_SURFACE_VARIANT,
        )

        controls = []
        for key, value in self.data_tables.items():

            def delete_clicked(e, key=key):
                self.open_confirm_dialog(key)

            controls.extend([
                ft.Row([
                    ft.Text(f"**{key}**", size=18),
                    ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_clicked,
                                  icon_color=ft.Colors.RED_500)  # ゴミ箱アイコン
                ]),
                ft.Text("Processing:", size=14),
                value["processing"],
                ft.Text("Description:", size=14),
                ft.Column(controls=[value["description"]], scroll=ft.ScrollMode.AUTO,
                          height=200),  # DataTable を Column で囲み、スクロール可能にする
                ft.Row([ft.Text("Color:", size=14), value["color"]]),
                ft.Divider(),
            ])

        # 新しい設定項目を追加するためのUI
        controls.extend([
            ft.ElevatedButton("新しい項目を追加", on_click=self.add_config_item)
        ])

        controls.append(ft.ElevatedButton("保存", on_click=self.save_config))

        self.controls = [
            ft.ListView(controls=controls, expand=True, auto_scroll=True)  # ListViewでラップ
        ]
        return self


class PersonnelConfigView(ft.View):  # ft.View を継承するように修正
    def __init__(self, route, config, update_config_callback):
        super().__init__(route)
        self.config = config
        self.update_config_callback = update_config_callback
        self.data_table = None  # DataTableを格納
        self.new_key_field = ft.TextField(label="新しいキー", width=200)
        self.new_value_field = ft.TextField(label="1人あたりの日産数", width=200, keyboard_type=ft.KeyboardType.NUMBER)
        self.snack_bar = None

        # ConfirmDialog をインスタンス化
        self.confirm_dialog = ConfirmDialog(
            title="", content="", on_ok=None, on_cancel=None)

        # 新規キー入力用のコントロール
        self.add_item_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("新しい設定項目"),
            content=ft.Column([
                self.new_key_field,
                self.new_value_field,
            ], tight=True),
            actions=[
                ft.TextButton("キャンセル", on_click=self.close_add_item_dialog),
                ft.TextButton("追加", on_click=self.add_new_config_item),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        # AlertDialogをpageに追加
        # self.page.overlay.append(self.add_item_dialog) # ここから移動
        self.build_data_table()

    def build_data_table(self):
        """
        設定に基づいてDataTableを構築する
        """
        columns = [
            ft.DataColumn(ft.Text("項目")),
            ft.DataColumn(ft.Text("1人あたりの日産数")),
            ft.DataColumn(ft.Text("")),  # 削除ボタン用の空の列
        ]
        rows = []
        for key, value in self.config.items():
            def delete_clicked(e, key=key):
                self.open_confirm_dialog(key)

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(key)),
                        ft.DataCell(ft.TextField(value=str(value), width=100,
                                                  keyboard_type=ft.KeyboardType.NUMBER)),
                        ft.DataCell(
                            ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_clicked,
                                          icon_color=ft.Colors.RED_500),
                        ),
                    ],
                )
            )

        self.data_table = ft.DataTable(
            columns=columns,
            rows=rows,
            width=700,  # 幅を調整
            show_bottom_border=True,
            heading_row_color=ft.Colors.GREY_200,
        )

    def show_message(self, message):
        """
        SnackBarを表示する
        """
        self.snack_bar = ft.SnackBar(ft.Text(message), open=True)
        if self.snack_bar not in self.page.overlay:
            self.page.overlay.append(self.snack_bar)
        self.page.update()

    def open_confirm_dialog(self, key):
        """確認ダイアログを開く"""

        def yes_click(e):
            self.delete_config_item(key)
            self.confirm_dialog.open = False
            self.page.update()

        def no_click(e):
            self.confirm_dialog.open = False
            self.page.update()

        self.confirm_dialog.title = ft.Text("削除確認")
        self.confirm_dialog.content = ft.Text(f"'{key}' を本当に削除しますか？")
        self.confirm_dialog.actions = [
            ft.TextButton("キャンセル", on_click=no_click),
            ft.TextButton("OK", on_click=yes_click),
        ]
        self.confirm_dialog.actions_alignment = ft.MainAxisAlignment.END
        self.page.dialog = self.confirm_dialog
        # ダイアログを表示する前に page.overlay に追加
        if self.confirm_dialog not in self.page.overlay:
            self.page.overlay.append(self.confirm_dialog)
        self.confirm_dialog.open = True
        self.page.update()

    def delete_config_item(self, key):
        """
        設定項目を削除する
        """
        if key in self.config:
            del self.config[key]
            self.build_data_table()

            self.show_message(f"キー '{key}' を削除しました。")

            # 画面を最新のデータで更新
            self.controls.clear()
            self.controls.extend(self.build().controls)  # build()でcontrolsを再生成
            self.page.update()
        else:
            self.show_message(f"キー '{key}' はすでに削除されています。")
            print(f"キー '{key}' はすでに削除されています。")  # デバッグ用
            self.page.update()  # 削除に失敗した場合もUIを更新

    def add_config_item(self, e):
        """
        新しい設定項目を追加する
        """
        self.new_key_field.value = ""  # 初期化
        self.new_value_field.value = ""  # 初期化
        self.page.dialog = self.add_item_dialog
        self.add_item_dialog.open = True
        self.page.update()

    def close_add_item_dialog(self, e):
        self.add_item_dialog.open = False
        self.build_data_table()
        self.page.update()

    def add_new_config_item(self, e):
        """
        ダイアログから入力された情報に基づいて新しい設定項目を追加する
        """
        new_key = self.new_key_field.value.strip()
        new_value = self.new_value_field.value.strip()
        if not new_key or new_key in self.config or not new_value:
            self.show_message("無効なキーまたは値です")
            return

        try:
            new_value = int(new_value)  # 値を整数に変換
        except ValueError:
            self.show_message("値は整数である必要があります")
            return

        self.config[new_key] = new_value
        self.build_data_table()
        self.show_message(f"キー '{new_key}' を追加しました。")

        # ダイアログを閉じる
        self.add_item_dialog.open = False

        # 画面を最新のデータで更新
        self.controls.clear()
        self.controls.extend(self.build().controls)  # build()でcontrolsを再生成

        self.page.update()

    def save_config(self, e):
        """
        DataTableのデータをJSON形式に変換して保存する
        """
        new_config = {}
        try:
            for row in self.data_table.rows:
                key = row.cells[0].content.value
                value = row.cells[1].content.value
                try:
                    new_config[key] = int(value)
                except ValueError:
                    self.show_message(f"数値以外の値が入力されています: {key}")
                    return  # 保存を中断

            self.update_config_callback(new_config)
            self.page.go("/")
        except Exception as ex:
            print(ex)  # デバッグ用
            self.show_message(f"保存中にエラーが発生しました: {str(ex)}")
        self.page.update()

    def build(self):
        self.appbar = ft.AppBar(
            title=ft.Text("人数計算詳細設定"),
            bgcolor=ft.Colors.ON_SURFACE_VARIANT,
        )

        controls = []
        controls.extend([self.data_table])

        # 新しい設定項目を追加するためのUI
        controls.extend([
            ft.ElevatedButton("新しい項目を追加", on_click=self.add_config_item)
        ])

        controls.append(ft.ElevatedButton("保存", on_click=self.save_config))

        self.controls = [
            ft.ListView(controls=controls, expand=True, auto_scroll=True)  # ListViewでラップ
        ]
        return self


def main(page: ft.Page):
    page.title = "生産スケジュール管理アプリ"
    page.bgcolor = "#f4f4f4"
    page.padding = 20
    
    # 初期ウィンドウサイズ(縦)を800に設定
    page.window.height = 800

    selected_file_schedule = ft.Text("ファイル未選択", size=14, color="gray")
    sheet_name_input_schedule = ft.TextField(label="シート名を入力してください", width=300)
    selected_file_personnel = ft.Text("ファイル未選択", size=14, color="gray")
    sheet_name_input_personnel = ft.TextField(label="シート名を入力してください", width=300)
    status = ft.Text("", size=16, weight="bold", color="green")

    # 設定の保持
    schedule_config = DEFAULT_SCHEDULE_CONFIG.copy()
    personnel_config = DEFAULT_PERSONNEL_CONFIG.copy()

    def update_schedule_config(new_config):
        nonlocal schedule_config
        schedule_config = new_config
        with open(DEFAULT_SCHEDULE_PATH, 'w', encoding='utf-8') as file:
            json.dump(schedule_config, file, ensure_ascii=False, indent=4)
        print("スケジュール設定更新:", schedule_config)

    def update_personnel_config(new_config):
        nonlocal personnel_config
        personnel_config = new_config
        with open(DEFAULT_PERSONNEL_PATH, 'w', encoding='utf-8') as file:
            json.dump(personnel_config, file, ensure_ascii=False, indent=4)
        print("人数計算設定更新:", personnel_config)

    # ファイルピッカーの設定
    def on_file_selected_schedule(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file_schedule.value = e.files[0].path
            page.update()

    def on_file_selected_personnel(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file_personnel.value = e.files[0].path
            page.update()

    # FilePickerインスタンスを生成
    file_picker_schedule = ft.FilePicker(on_result=on_file_selected_schedule)
    file_picker_personnel = ft.FilePicker(on_result=on_file_selected_personnel)
    file_picker_save = ft.FilePicker()

    # FilePickerインスタンスをpageの属性として追加
    page.file_picker_schedule = file_picker_schedule
    page.file_picker_personnel = file_picker_personnel
    page.file_picker_save = file_picker_save

    page.overlay.extend([file_picker_schedule, file_picker_personnel, file_picker_save])

    # スケジュール作成
    def generate_schedule(e):
        file_path = selected_file_schedule.value
        sheet_name = sheet_name_input_schedule.value.strip()
        if not file_path or not os.path.exists(file_path):
            status.value = "スケジュール作成用のファイルを選択してください"
        elif not sheet_name:
            status.value = "スケジュール作成用のシート名を入力してください"
        else:
            page.add(ft.Text("保存先を選択してください"))  # ファイルピッカーが表示されることを確認するためのテキスト

            filename = os.path.basename(file_path).replace(".xlsx", "")
            # ファイル保存ダイアログを表示
            page.file_picker_save.on_result = lambda e: generate_schedule_with_path(e, file_path, sheet_name)
            page.file_picker_save.save_file(
                file_name=f"{filename}_{sheet_name}_schedule.xlsx",
                allowed_extensions=["xlsx"]
            )

        page.update()

    def generate_schedule_with_path(e, file_path, sheet_name):
        """
        ファイル保存ダイアログで選択されたパスを使ってスケジュールを生成する
        """
        if e.path:
            output_path = e.path
            try:
                ps = Scheduling(order_data_path=file_path, save_data_path=output_path, sheet_name=sheet_name)
                miss_datas = ps.create()
                status.value = f"スケジュールを生成しました: {output_path}"
                if miss_datas:
                    miss_message = "\n".join([f"製品名：{miss_data[0]}、名称2：{miss_data[1]}" for miss_data in miss_datas])
                    status.value += f"\n名称2が見つからない製品がありました↓\n{miss_message}"
            except Exception as ex:
                status.value = f"エラーが発生しました（スケジュール作成）: {str(ex)}"
        else:
            status.value = "保存先が選択されませんでした"
        page.update()

    def calculate_personnel(e):
        file_path = selected_file_personnel.value
        sheet_name = sheet_name_input_personnel.value.strip()
        if not file_path or not os.path.exists(file_path):
            status.value = "人数計算用のファイルを選択してください"
        elif not sheet_name:
            status.value = "人数計算用のシート名を入力してください"
        else:
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                # 仮の計算: "生産量"列が存在しない場合はデフォルト値1で計算
                # 設定ファイルから係数を取得
                for task, coefficient in personnel_config.items():
                    if task in df.columns:
                        df["必要人数_" + task] = df[task] / coefficient
                # 必要に応じて合計を計算
                df["必要人数"] = df[[col for col in df.columns if "必要人数_" in col]].sum(axis=1)
                df.to_excel(file_path, index=False)
                status.value = f"人数計算を完了しました: {file_path}"
            except Exception as ex:
                status.value = f"エラーが発生しました（人数計算）: {str(ex)}"
        page.update()

    # 使い方PDFを開く処理
    def open_usage_instructions(e):
        pdf_path = "usage_instructions.pdf"  # PDFファイルのパス。環境に合わせて調整してください
        page.launch_url(pdf_path)

    # 設定画面への遷移
    def go_to_schedule_config(e):
        page.go("/schedule_config")

    def go_to_personnel_config(e):
        page.go("/personnel_config")

    # タイトルと使い方ボタンを同じRowに配置し、タイトルを中央に表示する
    header_row = ft.Row(
        controls=[
            # 左側の空のコンテナ（右側の使い方ボタンと同じ幅）
            ft.Container(width=120),
            # 中央のタイトルコンテナ（expandで幅を拡大し、中央寄せ）
            ft.Container(
                content=ft.Text("生産スケジュール管理", size=24, weight="bold"),
                expand=True,
                alignment=ft.alignment.center,
            ),
            # 右側の使い方ボタンを入れたコンテナ
            ft.Container(
                content=ft.ElevatedButton("使い方", icon=ft.Icons.INFO, on_click=open_usage_instructions),
                width=120,
                alignment=ft.alignment.center,
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def main_view():
        return ft.View(
            "/",
            controls=[
                ft.Column(  # Columnで囲む
                    controls=[
                        header_row,
                        ft.Divider(),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("📅 スケジュール作成", size=20, weight="bold"),
                                    selected_file_schedule,
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton("ファイル選択", icon=ft.Icons.UPLOAD_FILE, on_click=lambda e: page.file_picker_schedule.pick_files(allow_multiple=False)),
                                            sheet_name_input_schedule,
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    ft.ElevatedButton("詳細設定", icon=ft.Icons.SETTINGS, on_click=go_to_schedule_config),
                                    ft.ElevatedButton("スケジュール生成", icon=ft.Icons.CALENDAR_MONTH, on_click=generate_schedule),
                                ],
                                spacing=10,
                            ),
                            padding=15,
                            bgcolor="white",
                            border_radius=10,
                                                            shadow=ft.BoxShadow(blur_radius=5, spread_radius=2, color=ft.Colors.GREY_400),
                        ),
                        ft.Divider(),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("👥 人数計算", size=20, weight="bold"),
                                    selected_file_personnel,
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton("ファイル選択", icon=ft.Icons.UPLOAD_FILE, on_click=lambda e: page.file_picker_personnel.pick_files(allow_multiple=False)),
                                            sheet_name_input_personnel,
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    ft.ElevatedButton("詳細設定", icon=ft.Icons.SETTINGS, on_click=go_to_personnel_config),
                                    ft.ElevatedButton("人数計算", icon=ft.Icons.CALCULATE, on_click=calculate_personnel),
                                ],
                                spacing=10,
                            ),
                            padding=15,
                            bgcolor="white",
                            border_radius=10,
                            shadow=ft.BoxShadow(blur_radius=5, spread_radius=2, color=ft.Colors.GREY_400),
                        ),
                        ft.Divider(),
                        ft.Container(
                            content=ft.Column(
                                controls=[status],
                                scroll=ft.ScrollMode.AUTO,  # 垂直スクロールを指定
                                height=100,  # 必要に応じて高さを調整
                            ),
                            width=float('inf'),  # 必要に応じて幅を調整
                            padding=10,  # 必要に応じてpaddingを調整
                        ),
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,  # Column の alignment を指定
                )
            ]
        )

    def route_change(e):
        page.views.clear()
        page.views.append(
            main_view()
        )

        if page.route == "/schedule_config":
            config_view = ScheduleConfigView(page.route, schedule_config, update_schedule_config)
            page.views.append(config_view)
            if config_view.confirm_dialog not in page.overlay:
                page.overlay.append(config_view.confirm_dialog)
            if config_view.add_item_dialog not in page.overlay:
                page.overlay.append(config_view.add_item_dialog)

        if page.route == "/personnel_config":
            config_view = PersonnelConfigView(page.route, personnel_config, update_personnel_config)
            page.views.append(config_view)
            if config_view.confirm_dialog not in page.overlay:
                page.overlay.append(config_view.confirm_dialog)
            if config_view.add_item_dialog not in page.overlay:
                page.overlay.append(config_view.add_item_dialog)

        page.update()

    def view_pop(e):
        page.views.pop()
        page.go("/")  # 元の画面に戻る
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)

# ft.app(target=main, view=ft.WEB_BROWSER)