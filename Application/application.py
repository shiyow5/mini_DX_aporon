import flet as ft
import pandas as pd
import os
import json

# デフォルトの設定JSON（サンプル）
DEFAULT_SCHEDULE_CONFIG = {
    "外観検査": {
        "processing": [
            [1]
        ],
        "description": {
            "外観検査日": [1]
        },
        "color": "cc0000"
    },

    "組立・スパウト嵌め・ロック・パイプ嵌め・外観検査": {
        "processing": [
            [1, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ],
        "description": {
            "ネジ嵌合・スパウト嵌め日": [1, 0, 0],
            "ロック日": [1, 0, 0],
            "パイプ嵌め日": [0, 1, 0],
            "外観検査日": [0, 0, 1]
        },
        "color": "999900"
    },
    
    "Z-155コアセット組立": {
        "processing": [
            [1]
        ],
        "description": {
            "組立日": [1]
        },
        "color": "ff99ff"
    }
}

class ScheduleConfigView(ft.View):
    def __init__(self, route, config, update_config_callback):
        super().__init__(route)
        self.config = config
        self.update_config_callback = update_config_callback
        self.data_tables = {}  # 各項目のDataTableを格納する辞書
        self.build_data_tables()
        self.new_key_field = ft.TextField(label="新しいキー", width=200)  # TextFieldをインスタンス変数として定義
        self.snack_bar = None # SnackBarをインスタンス変数として定義

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
            ],tight=True),
            actions=[
                ft.TextButton("キャンセル", on_click=self.close_add_item_dialog),
                ft.TextButton("追加", on_click=self.add_new_config_item),
            ],
        )

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
            columns = [ft.DataColumn(ft.Text(f"列{i+1}")) for i in range(len(data[0]) if data else 1)]  # 列の動的な生成
            rows = []
            for i, row_data in enumerate(data):
                cells = [ft.DataCell(ft.TextField(value=str(cell_value), width=70)) for cell_value in row_data]
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

            columns = [ft.DataColumn(ft.Text(f"列{i+1}")) for i in range(max_len)]  # 列数をリストの最大長にする
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
                    cells.append(ft.DataCell(ft.TextField(value=str(item_value), width=70))) # リストでない場合はそのまま表示
                rows.append(ft.DataRow(cells=cells))

            return ft.DataTable(
                columns=columns,
                rows=rows,
                width=800, # DataTableの幅を調整
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
            self.page.update() # 削除に失敗した場合もUIを更新

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
                            return # 保存を中断
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
            print(ex) # デバッグ用
            self.show_message(f"保存中にエラーが発生しました: {str(ex)}")
        self.page.update()

    def build(self):
        self.appbar = ft.AppBar(
            title=ft.Text("スケジュール作成詳細設定"),
            bgcolor=ft.Colors.ON_SURFACE_VARIANT,
        )

        # ダイアログを page.overlay に追加
        if self.add_item_dialog not in self.page.overlay:
            self.page.overlay.append(self.add_item_dialog)

        controls = []
        for key, value in self.data_tables.items():
            def delete_clicked(e, key=key):
                self.delete_config_item(key)
            controls.extend([
                ft.Row([
                    ft.Text(f"**{key}**", size=18),
                    ft.IconButton(icon=ft.Icons.REMOVE, on_click=delete_clicked) # 削除ボタン
                ]),
                ft.Text("Processing:", size=14),
                value["processing"],
                ft.Text("Description:", size=14),
                ft.Column(controls=[value["description"]], scroll=ft.ScrollMode.AUTO, height=200),  # DataTable を Column で囲み、スクロール可能にする
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

def main(page: ft.Page):
    page.title = "生産スケジュール管理アプリ"
    page.bgcolor = "#f4f4f4"
    page.padding = 20

    selected_file_schedule = ft.Text("ファイル未選択", size=14, color="gray")
    sheet_name_input_schedule = ft.TextField(label="シート名を入力してください", width=300)
    selected_file_personnel = ft.Text("ファイル未選択", size=14, color="gray")
    sheet_name_input_personnel = ft.TextField(label="シート名を入力してください", width=300)
    status = ft.Text("", size=16, weight="bold", color="green")

    # 設定の保持
    schedule_config = DEFAULT_SCHEDULE_CONFIG.copy()

    def update_schedule_config(new_config):
        nonlocal schedule_config
        schedule_config = new_config
        print("設定更新:", schedule_config)

    # ファイルピッカーの設定
    def on_file_selected_schedule(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file_schedule.value = e.files[0].path
            page.update()
    
    def on_file_selected_personnel(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file_personnel.value = e.files[0].path
            page.update()

    file_picker_schedule = ft.FilePicker(on_result=on_file_selected_schedule)
    file_picker_personnel = ft.FilePicker(on_result=on_file_selected_personnel)
    page.overlay.extend([file_picker_schedule, file_picker_personnel])

    # スケジュール作成
    def generate_schedule(e):
        file_path = selected_file_schedule.value
        sheet_name = sheet_name_input_schedule.value.strip()
        if not file_path or not os.path.exists(file_path):
            status.value = "スケジュール作成用のファイルを選択してください"
        elif not sheet_name:
            status.value = "スケジュール作成用のシート名を入力してください"
        else:
            output_path = file_path.replace(".xlsx", f"_{sheet_name}_schedule.xlsx")
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)

                # フィルタリング (元のロジックを維持、必要に応じて調整)
                # スケジュール列を追加、設定値で埋める (この部分は設定に基づいて調整)
                df["スケジュール"] = "生成済み"  # ダミーの処理。設定に基づいて動作するように修正が必要
                df.to_excel(output_path, index=False)
                status.value = f"スケジュールを生成しました: {output_path}"
            except Exception as ex:
                status.value = f"エラーが発生しました（スケジュール作成）: {str(ex)}"
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
                df["必要人数"] = df.get("生産量", 1) * 2
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
                                            ft.ElevatedButton("ファイル選択", icon=ft.Icons.UPLOAD_FILE, on_click=lambda e: file_picker_schedule.pick_files(allow_multiple=False)),
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
                                            ft.ElevatedButton("ファイル選択", icon=ft.Icons.UPLOAD_FILE, on_click=lambda e: file_picker_personnel.pick_files(allow_multiple=False)),
                                            sheet_name_input_personnel,
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
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
                        status,
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER, # Column の alignment を指定
                )
            ]
        )
    

    def route_change(e):
        # 現在のビューを保存
        if page.route != "/schedule_config":
            page.views.clear()
            page.views.append(
                main_view()
            )
        
        # /schedule_config 画面への遷移時に必要なビューだけ追加
        if page.route == "/schedule_config":
            config_view = ScheduleConfigView(page.route, schedule_config, update_schedule_config)
            page.views.append(config_view)
        
        page.update()

    def view_pop(e):
        page.views.pop()
        if page.route == "/schedule_config":
            page.go("/")  # 元の画面に戻る
        page.update()


    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main)