# llm-llm
大規模モデルユニット、大規模モデル推論サービスを提供するために使用します。

## setup
ユニットを設定します。

送信するJSON:
```json
{
    "request_id": "2",
    "work_id": "llm",
    "action": "setup",
    "object": "llm.setup",
    "data": {
        "model": "qwen2.5-0.5B-prefill-20e",
        "response_format": "llm.utf-8.stream",
        "input": "llm.utf-8",
        "enoutput": true,
        "max_token_len": 256,
        "prompt": "You are a knowledgeable assistant capable of answering various questions and providing information."
    }
}
```
- request_id: 基本データの説明を参照
- work_id: 設定ユニットの場合は `llm`
- action: 呼び出すメソッドは `setup`
- object: 送信するデータの種類は `llm.setup`
- model: 使用するモデルは中国語モデル `qwen2.5-0.5B-prefill-20e`
- response_format: 結果は `llm.utf-8.stream`（UTF-8ストリーミング出力）形式で返される
- input: 入力は `llm.utf-8`（ユーザーからの入力を表す）
- enoutput: ユーザー結果出力を有効にするかどうか
- max_token_len: 最大出力トークン数、この値はモデルの最大制限によって制限される
- prompt: モデルのプロンプト

レスポンスJSON:
```json
{
    "created": 1731488402,
    "data": "None",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "None",
    "request_id": "2",
    "work_id": "llm.1002"
}
```
- created: メッセージ作成時刻（Unixタイム）
- work_id: 正常に作成されたwork_idユニット

## link
上位ユニットの出力をリンクします。

送信するJSON:
```json
{
    "request_id": "3",
    "work_id": "llm.1002",
    "action": "link",
    "object": "work_id",
    "data": "kws.1000"
}
```

レスポンスJSON:
```json
{
    "created": 1731488402,
    "data": "None",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "None",
    "request_id": "3",
    "work_id": "llm.1002"
}
```
error::codeが0の場合は実行成功を示します。

llmとkwsユニットをリンクすることで、kwsがウェイクアップデータを発行した時に、llmユニットは繰り返しウェイクアップ機能のために前回の未完了の推論を停止します。

> **リンク時には、kwsが設定済みで動作状態にあることを確認してください。リンクはsetup段階でも行うことができます。**

例：
```json
{
    "request_id": "2",
    "work_id": "llm",
    "action": "setup",
    "object": "llm.setup",
    "data": {
        "model": "qwen2.5-0.5B-prefill-20e",
        "response_format": "llm.utf-8.stream",
        "input": ["llm.utf-8", "asr.1001", "kws.1000"],
        "enoutput": true,
        "max_token_len": 256,
        "prompt": "You are a knowledgeable assistant capable of answering various questions and providing information."
    }
}
```

## unlink
リンクを解除します。

送信するJSON:
```json
{
    "request_id": "4",
    "work_id": "llm.1002",
    "action": "unlink",
    "object": "work_id",
    "data": "kws.1000"
}
```

レスポンスJSON:
```json
{
    "created": 1731488402,
    "data": "None",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "None",
    "request_id": "4",
    "work_id": "llm.1002"
}
```
error::codeが0の場合は実行成功を示します。

## pause
ユニットを一時停止します。

送信するJSON:
```json
{
    "request_id": "5",
    "work_id": "llm.1002",
    "action": "pause"
}
```

レスポンスJSON:
```json
{
    "created": 1731488402,
    "data": "None",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "None",
    "request_id": "5",
    "work_id": "llm.1002"
}
```
error::codeが0の場合は実行成功を示します。

## work
ユニットを再開します。

送信するJSON:
```json
{
    "request_id": "6",
    "work_id": "llm.1002",
    "action": "work"
}
```

レスポンスJSON:
```json
{
    "created": 1731488402,
    "data": "None",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "None",
    "request_id": "6",
    "work_id": "llm.1002"
}
```
error::codeが0の場合は実行成功を示します。

## exit
ユニットを終了します。

送信するJSON:
```json
{
    "request_id": "7",
    "work_id": "llm.1002",
    "action": "exit"
}
```

レスポンスJSON:
```json
{
    "created": 1731488402,
    "data": "None",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "None",
    "request_id": "7",
    "work_id": "llm.1002"
}
```
error::codeが0の場合は実行成功を示します。

## タスク情報

タスクリストの取得：

送信するJSON:
```json
{
	"request_id": "2",
	"work_id": "llm",
	"action": "taskinfo"
}
```

レスポンスJSON:
```json
{
    "created":1731652149,
    "data":["llm.1002"],
    "error":{
        "code":0,
        "message":""
    },
    "object":"llm.tasklist",
    "request_id":"2",
    "work_id":"llm"
}
```

タスクの実行時パラメータの取得：

送信するJSON:
```json
{
	"request_id": "2",
	"work_id": "llm.1002",
	"action": "taskinfo"
}
```

レスポンスJSON:
```json
{
    "created":1731652187,
    "data":{
        "enoutput":true,
        "inputs_":["llm.utf-8"],
        "model":"qwen2.5-0.5B-prefill-20e",
        "response_format":"llm.utf-8.stream"
    },
    "error":{
        "code":0,
        "message":""
    },
    "object":"llm.taskinfo",
    "request_id":"2",
    "work_id":"llm.1002"
}
```

> **注意: work_idはユニットの初期化登録順に増加し、固定のインデックス値ではありません。**
