import flet as ft
import pandas as pd
import os

def main(page: ft.Page):
    page.title = "生産スケジュール管理アプリ"
    page.bgcolor = "#f4f4f4"  # 背景色
    page.padding = 20

    selected_file = ft.Text("ファイル未選択", size=14, color="gray")
    selected_file_personnel = ft.Text("ファイル未選択", size=14, color="gray")
    status = ft.Text("", size=16, weight="bold", color="green")

    # ファイルピッカーの設定
    def on_file_selected_schedule(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file.value = e.files[0].path
            page.update()
    
    def on_file_selected_personnel(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file_personnel.value = e.files[0].path
            page.update()

    file_picker_schedule = ft.FilePicker(on_result=on_file_selected_schedule)
    file_picker_personnel = ft.FilePicker(on_result=on_file_selected_personnel)
    page.overlay.append(file_picker_schedule)
    page.overlay.append(file_picker_personnel)

    # スケジュール作成
    def generate_schedule(e):
        if selected_file.value and os.path.exists(selected_file.value):
            file_path = selected_file.value
            output_path = file_path.replace(".xlsx", "_schedule.xlsx")
            df = pd.read_excel(file_path)  # 仮のデータ処理
            df["スケジュール"] = "生成済み"  # 仮の列追加
            df.to_excel(output_path, index=False)
            status.value = f"スケジュールを生成しました: {output_path}"
        else:
            status.value = "ファイルを選択してください"
        page.update()

    # 人数計算
    def calculate_personnel(e):
        if selected_file_personnel.value and os.path.exists(selected_file_personnel.value):
            file_path = selected_file_personnel.value
            df = pd.read_excel(file_path)
            df["必要人数"] = df.get("生産量", 1) * 2  # 仮の計算
            df.to_excel(file_path, index=False)
            status.value = f"人数計算を完了しました: {file_path}"
        else:
            status.value = "ファイルを選択してください"
        page.update()

    # UI 設計
    page.add(
        ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("生産スケジュール管理", size=24, weight="bold"),
                    padding=10,
                    alignment=ft.alignment.center
                ),
                ft.Divider(),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("📅 スケジュール作成", size=20, weight="bold"),
                            selected_file,
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton("ファイル選択", icon=ft.Icons.UPLOAD_FILE, on_click=lambda e: file_picker_schedule.pick_files(allow_multiple=False)),
                                    ft.ElevatedButton("スケジュール生成", icon=ft.Icons.CALENDAR_MONTH, on_click=generate_schedule),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        spacing=10
                    ),
                    padding=15,
                    bgcolor="white",
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=5, spread_radius=2, color=ft.Colors.GREY_400)
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
                                    ft.ElevatedButton("人数計算", icon=ft.Icons.CALCULATE, on_click=calculate_personnel),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        spacing=10
                    ),
                    padding=15,
                    bgcolor="white",
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=5, spread_radius=2, color=ft.Colors.GREY_400)
                ),
                ft.Divider(),
                status
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
