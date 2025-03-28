# 生産スケジュール管理アプリ 取扱説明書

## 1. はじめに

本アプリは、生産スケジュールの作成および必要人員の計算を効率化するためのツールです。Excelファイルからデータを読み込み、設定に基づいてスケジュールを生成し、人員計算を行います。  
※ 本アプリは、Windows専用アプリケーションです。

## 2. アプリケーションの起動

1.  以下のリンクからアプリケーションを**ダウンロード**してください。  
    [Schedule Application Download link](https://github.com/shiyow5/mini_DX_aporon/releases/download/v1.0.1/schedule_application.zip) 👈

2.  ダウンロードした**zipファイルを解凍**してください。

3.  `Application.exe`をダブルクリックし実行してください。

## 3. メイン画面

アプリを起動すると、以下の要素を含むメイン画面が表示されます。

*   **ヘッダー**:  
    アプリケーションのタイトル（"生産スケジュール管理"）と、"使い方"ボタンが表示されます。

*   **スケジュール作成**:
    *   "スケジュール作成"の見出し
    *   ファイル選択: スケジュール作成に使用するExcelファイルを選択できます。
    *   シート名: Excelファイル内のシート名をドロップダウンから選択できます。
    *   詳細設定: スケジュール作成に関する詳細な設定を行えます（設定画面へ遷移します）。
    *   スケジュール生成: 選択されたファイルとシート名、設定に基づいてスケジュールを生成します。
*   **人数計算**:
    *   "人数計算"の見出し
    *   ファイル選択: 人数計算に使用するExcelファイルを選択できます。
    *   シート名: Excelファイル内のシート名をドロップダウンから選択できます。
    *   詳細設定: 人数計算に関する詳細な設定を行えます（設定画面へ遷移します）。
    *   人数計算: 選択されたファイルとシート名、設定に基づいて人数計算を行います。
*   **ステータス**:
    *   処理の進捗状況やエラーメッセージが表示されます。

## 4. 基本的な使い方

### 4.1 スケジュール作成

1.  **ファイル選択**:
    *   "ファイル選択"ボタンをクリックし、スケジュール作成に使用するExcelファイルを選択します。
    *   ファイルを選択すると、選択されたファイル名がラベルに表示されます。
2.  **シート名選択**:
    *   Excelファイルからシート名が自動的に抽出され、ドロップダウンリストに表示されます。
    *   適切なシート名をドロップダウンリストから選択します。
3.  **詳細設定 (オプション)**:
    *   必要に応じて、"詳細設定"ボタンをクリックして詳細設定画面へ移動し、スケジュール作成の詳細な設定を行います。
4.  **スケジュール生成**:
    *   "スケジュール生成"ボタンをクリックします。
    *   保存先を選択するダイアログが表示されるので、保存場所とファイル名を指定します。
    *   スケジュール生成が開始され、ステータス領域に処理状況が表示されます。

### 4.2 人数計算

1.  **ファイル選択**:
    *   "ファイル選択"ボタンをクリックし、人数計算に使用するExcelファイルを選択します。  
        ※ 選択するExcelファイルは「スケジュール作成」によって作成されたExcelファイル、もしくは同じ形式のものである必要があります。
    *   ファイルを選択すると、選択されたファイル名がラベルに表示されます。
2.  **シート名選択**:
    *   Excelファイルからシート名が自動的に抽出され、ドロップダウンリストに表示されます。
    *   適切なシート名をドロップダウンリストから選択します。
3.  **詳細設定 (オプション)**:
    *   必要に応じて、"詳細設定"ボタンをクリックして詳細設定画面へ移動し、人数計算の詳細な設定を行います。
4.  **人数計算**:
    *   "人数計算"ボタンをクリックします。
    *   人数計算が開始され、ステータス領域に処理状況が表示されます。

## 5. 詳細設定画面

メイン画面から"詳細設定"ボタンをクリックすると、詳細設定画面が表示されます。ここでは、スケジュール作成および人数計算の詳細なパラメータを設定できます。

### 5.1 スケジュール作成詳細設定

*   **キー**: 各設定項目の名称2が表示されます。
*   **Description**: その名称2に対する、スケジュール作成の設定が表示されます。
*   **Color**: 設定項目の色を指定します（例: cc0000）。
*   **操作**:
    *   削除ボタン: 設定項目を削除します。

#### 5.1.1 設定項目の追加

1.  **新しい項目を追加**:
    *   "新しい項目を追加"ボタンをクリックします。
    *   新しい設定項目の情報を入力するためのダイアログが表示されます。
        *   **新しいキー**: 設定項目の名称2を入力します。
        *   **Description**: 設定項目の説明をJSON形式で入力します（例: `{"項目1":[1,0], "項目2":[0,1]}`）。  
            ここで項目1や項目2は工程名、`[1,0]`や`[0,1]`は納品日の何日前かを表す。  
            工程名は`""`で囲むこと。  
            `[1,0]`は納品日の二日前にその工程があることを示す。また、`[0,1]`は納品日の一日前にその工程があることを示す。（`[]`の中は`0`か`1`）  
            例えば、名称2が「ノズル嵌め」という製品は"納品日の前日がノズル検査日"、"ノズル検査日の前日がノズル嵌め日"であるとする。この名称2を新たに設定したい場合。
            1. ノズル嵌め日は納品日の二日前であるので、`[1,0]`と書ける。
            2. ノズル検査日は納品日の一日前であるので、`[0,1]`と書ける。
            3. 1.と2.を`"工程名":[]`の形式で表す。  
               `[1,0]`→`"ノズル嵌め日":[1,0]`,　`[0,1]`→`"ノズル検査日":[0,1]`
            4. それぞれをカンマ（,）で区切り、並べて、`{}`で囲む。  
               `{"ノズル嵌め日":[1,0], "ノズル検査日":[0,1]}`  
            ※ この順番は納品日から遠い工程順に並べてください。  
　            つまり、`{"ノズル検査日":[0,1], "ノズル嵌め日":[1,0]}`は**不可**です。
        *   **色**: 設定項目の色を16進数で入力します（例: `CC0000`）。  
            以下のサイトで、指定した色を16進数に変換できます。「カラーピッカー」と書かれているところで好きな色を選択し、右に表示される`#FFFFFF`や`#CC0000`から`#`を取り除いた文字を入力してください。  
            [参考リンク](https://www.color-site.com/) 👈
    *   "追加"ボタンをクリックして新しい項目を追加します。

#### 5.1.2 設定項目の削除

1.  **削除**:
    *   削除したい設定項目の行にある"削除"ボタン（ゴミ箱マーク）をクリックします。
    *   確認ダイアログが表示されるので、"OK"をクリックして削除します。

#### 5.1.3 設定の保存

1.  **保存**:
    *   すべての設定が完了したら、"保存"ボタンをクリックします。
    *   設定が保存され、メイン画面に戻ります。

### 5.2 人数計算詳細設定

*   **項目**: 各計算項目の名前が表示されます。
*   **1人あたりの日産数**: 1人あたりの日産数を入力します。
*   **操作**:
    *   削除ボタン: 設定項目を削除します。

#### 5.2.1 設定項目の追加

1.  **新しい項目を追加**:
    *   "新しい項目を追加"ボタンをクリックします。
    *   新しい設定項目の情報を入力するためのダイアログが表示されます。
        *   **新しいキー**: 設定項目の名前を入力します。
        *   **1人あたりの日産数**: 1人あたりの日産数を入力します。
    *   "追加"ボタンをクリックして新しい項目を追加します。

#### 5.2.2 設定項目の削除

1.  **削除**:
    *   削除したい設定項目の行にある"削除"ボタンをクリックします。
    *   確認ダイアログが表示されるので、"OK"をクリックして削除します。

#### 5.2.3 設定の保存

1.  **保存**:
    *   すべての設定が完了したら、"保存"ボタンをクリックします。
    *   設定が保存され、メイン画面に戻ります。

## 6. 注意事項

*   Excelファイルの形式が本アプリでサポートされている形式であることを確認してください。
*   詳細設定のJSON形式は正確に入力してください。
*   処理中にエラーが発生した場合は、ステータス領域にエラーメッセージが表示されます。メッセージを確認し、必要に応じて設定を見直してください。

## 7. トラブルシューティング

*   **アプリが起動しない**:
    *   お使いの端末がWindowsであるか確認してください。
    *   セキュリティソフトの警告を確認してください。
    *   アプリが危険であると判断され、ブロックされることがあります。
*   **Excelファイルが読み込めない**:
    *   ファイルが破損していないか確認してください。
    *   正しいファイル（xlsx）が選択されているか確認してください。
*   **詳細設定が保存できない**:
    *   JSON形式が正しいか確認してください。
*   **スケジュール生成や人数計算が完了しない**:
    *   設定パラメータが適切か確認してください。
    *   データ量が多い場合、処理に時間がかかることがあります。

## 8. サポート

本アプリケーションに関するお問い合わせは、以下の連絡先までお願いいたします。

[サポート連絡先]  
s1300221@u-aizu.ac.jp

## 9. 更新履歴

*   2025/03/27: 初版