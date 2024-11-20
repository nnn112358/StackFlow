# llm-tts
テキスト音声変換ユニットで、テキスト音声変換サービスを提供します。中国語と英語のモデルをサポートし、両言語でのテキスト音声変換サービスを提供できます。

## setup
ユニットを設定します。

送信するJSON:
```json
{
    "request_id": "2",
    "work_id": "tts",
    "action": "setup",
    "object": "tts.setup",
    "data": {
        "model": "single_speaker_fast",
        "response_format": "sys.pcm",
        "input": "tts.utf-8",
        "enoutput": false
    }
}
```
- request_id: 基本データの説明を参照
- work_id: ユニット設定時は `tts`
- action: 呼び出すメソッドは `setup`
- object: 送信するデータの種類は `tts.setup`
- model: 使用するモデルは中国語モデル `single_speaker_fast`
- response_format: 返される結果は `sys.pcm`（システムオーディオデータ）で、直接llm-audioモジュールに送信されて再生される
- input: 入力は `tts.utf-8`（ユーザー入力を表す）
- enoutput: ユーザー結果出力を有効にするかどうか

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
    "work_id":"llm.1003"
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
    "work_id": "tts.1003",
    "action": "link",
    "object":"work_id",
    "data":"kws.1000"
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
    "work_id":"tts.1003"
}
```
error::codeが0の場合は実行成功を示します。

llmとttsユニットをリンクすることで、kwsがウェイクアップした時にttsユニットは前回の未完了の推論を停止し、繰り返しウェイクアップ機能として使用されます。

> **リンク時にはkwsが設定済みで動作状態にあることを確認してください。リンクはsetup段階でも行うことができます。**

例：
```json
{
    "request_id": "2",
    "work_id": "tts",
    "action": "setup",
    "object": "tts.setup",
    "data": {
        "model": "single_speaker_fast",
        "response_format": "sys.pcm",
        "input": ["tts.utf-8", "llm.1002", "kws.1000"],
        "enoutput": false
    }
}
```

## unlink
リンクを解除します。

送信するJSON:
```json
{
    "request_id": "4",
    "work_id": "tts.1003",
    "action": "unlink",
    "object":"work_id",
    "data":"kws.1000"
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
    "work_id":"tts.1003"
}
```
error::codeが0の場合は実行成功を示します。

## pause
ユニットの動作を一時停止します。

送信するJSON:
```json
{
    "request_id": "5",
    "work_id": "llm.1003",
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
    "request_id":"5",
    "work_id":"llm.1003"
}
```
error::codeが0の場合は実行成功を示します。

## work
ユニットの動作を再開します。

送信するJSON:
```json
{
    "request_id": "6",
    "work_id": "llm.1003",
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
    "request_id":"6",
    "work_id":"llm.1003"
}
```
error::codeが0の場合は実行成功を示します。

## exit
ユニットを終了します。

送信するJSON:
```json
{
    "request_id": "7",
    "work_id": "llm.1003",
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
    "request_id":"7",
    "work_id":"llm.1003"
}
```
error::codeが0の場合は実行成功を示します。

## タスク情報

タスクリストの取得：

送信するJSON:
```json
{
	"request_id": "2",
	"work_id": "tts",
	"action": "taskinfo"
}
```

レスポンスJSON:
```json
{
    "created":1731652311,
    "data":["tts.1003"],
    "error":{
        "code":0,
        "message":""
    },
    "object":"tts.tasklist",
    "request_id":"2",
    "work_id":"tts"
}
```

タスクの実行時パラメータの取得：

送信するJSON:
```json
{
	"request_id": "2",
	"work_id": "tts.1003",
	"action": "taskinfo"
}
```

レスポンスJSON:
```json
{
    "created":1731652344,
    "data":{
        "enoutput":false,
        "inputs_":["tts.utf-8"],
        "model":"single_speaker_fast",
        "response_format":"sys.pcm"
    },
    "error":{
        "code":0,
        "message":""
    },
    "object":"tts.taskinfo",
    "request_id":"2",
    "work_id":"tts.1003"
}
```

> **注意: work_idはユニットの初期化登録順に増加し、固定のインデックス値ではありません。**  
> **同じタイプのユニットを同時に複数設定して動作させることはできません。不明なエラーが発生する可能性があります。例えば、ttsとmelo ttsを同時に動作させることはできません。**
