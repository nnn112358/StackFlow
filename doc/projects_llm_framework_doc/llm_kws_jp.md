# llm-kws
音声ウェイクアップユニットで、音声ウェイクアップサービスを提供します。中国語または英語のモデルを選択して、それぞれの言語でウェイクアップサービスを提供できます。

## setup
ユニットの動作を設定します。

送信するJSON:
```json
{
    "request_id": "2",
    "work_id": "kws",
    "action": "setup",
    "object": "kws.setup",
    "data": {
        "model": "sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01",
        "response_format": "kws.bool",
        "input": "sys.pcm",
        "enoutput": true,
        "kws": "你好你好"
        }
}
```
- request_id: 基本データの説明を参照
- work_id: ユニットを設定する場合は `kws`
- action: 呼び出すメソッドは `setup`
- object: 送信するデータの種類は `kws.setup`
- model: 使用するモデルは中国語モデル `sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01`
- response_format: 結果は `kws.bool` 形式で返される
- input: 入力は `sys.pcm`（システムオーディオ）
- enoutput: ユーザー結果出力を有効にするかどうか
- kws: 中国語のウェイクアップワードは `"你好你好"`

レスポンスJSON:
```json
{
    "created":1731488402,
    "data":"None",
    "error":{
        "code":0,
        "message":""
    },
    "object":"None",
    "request_id":"2",
    "work_id":"kws.1000"
}
```
- created: メッセージ作成時刻（Unixタイム）
- work_id: 正常に作成されたwork_idユニット

## pause
ユニットの動作を一時停止します。

送信するJSON:
```json
{
    "request_id": "3",
    "work_id": "kws.1000",
    "action": "pause",
}
```

レスポンスJSON:
```json
{
    "created":1731488402,
    "data":"None",
    "error":{
        "code":0,
        "message":""
    },
    "object":"None",
    "request_id":"3",
    "work_id":"kws.1000"
}
```
error::codeが0の場合は実行成功を示します。

## work
ユニットの動作を再開します。

送信するJSON:
```json
{
    "request_id": "4",
    "work_id": "kws.1000",
    "action": "work",
}
```

レスポンスJSON:
```json
{
    "created":1731488402,
    "data":"None",
    "error":{
        "code":0,
        "message":""
    },
    "object":"None",
    "request_id":"4",
    "work_id":"kws.1000"
}
```
error::codeが0の場合は実行成功を示します。

## exit
ユニットを終了します。

送信するJSON:
```json
{
    "request_id": "5",
    "work_id": "kws.1000",
    "action": "exit",
}
```

レスポンスJSON:
```json
{
    "created":1731488402,
    "data":"None",
    "error":{
        "code":0,
        "message":""
    },
    "object":"None",
    "request_id":"5",
    "work_id":"kws.1000"
}
```
error::codeが0の場合は実行成功を示します。

## タスク情報

タスクリストの取得：

送信するJSON:
```json
{
	"request_id": "2",
	"work_id": "kws",
	"action": "taskinfo"
}
```

レスポンスJSON:
```json
{
    "created":1731580350,
    "data":[
        "kws.1000"
    ],
    "error":{
        "code":0,
        "message":""
    },
    "object":"kws.tasklist",
    "request_id":"2",
    "work_id":"kws"
}
```

タスクの実行時パラメータの取得：

送信するJSON:
```json
{
	"request_id": "2",
	"work_id": "kws.1000",
	"action": "taskinfo"
}
```

レスポンスJSON:
```json
{
    "created":1731652086,
    "data":{
        "enoutput":true,
        "inputs_":["sys.pcm"],
        "model":"sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01",
        "response_format":"kws.bool"
    },
    "error":{
        "code":0,
        "message":""
    },
    "object":"kws.taskinfo",
    "request_id":"2",
    "work_id":"kws.1000"
}
```

> **注意: work_idはユニットの初期化登録順に増加し、固定のインデックス値ではありません。**
