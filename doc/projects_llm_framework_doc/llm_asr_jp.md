# llm-asr
音声をテキストに変換するモジュールで、音声テキスト変換サービスを提供します。中国語と英語のモデルをサポートし、これらの言語での音声からテキストへの変換が可能です。

## setup
ユニットの設定を行います。

送信するJSON:
```json
{
    "request_id": "2",
    "work_id": "asr",
    "action": "setup",
    "object": "asr.setup",
    "data": {
        "model": "sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23",
        "response_format": "asr.utf-8.stream",
        "input": "sys.pcm",
        "enoutput": true,
        "endpoint_config.rule1.min_trailing_silence": 2.4,
        "endpoint_config.rule2.min_trailing_silence": 1.2,
        "endpoint_config.rule3.min_trailing_silence": 30.1,
        "endpoint_config.rule1.must_contain_nonsilence": true,
        "endpoint_config.rule2.must_contain_nonsilence": true,
        "endpoint_config.rule3.must_contain_nonsilence": true
    }
}
```
- request_id: 基本データの説明を参照
- work_id: 設定ユニットの場合は `asr`
- action: 呼び出すメソッドは `setup`
- object: 送信するデータの種類は `asr.setup`
- model: 使用するモデルは中国語モデル `sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23`
- response_format: 結果フォーマットは `asr.utf-8.stream`（UTF-8ストリーム出力）
- input: 入力は `sys.pcm`（システムオーディオ）
- enoutput: ユーザー結果出力を有効にするかどうか
- endpoint_config.rule1.min_trailing_silence: ウェイクアップ後2.4秒で音声区切りが発生
- endpoint_config.rule2.min_trailing_silence: 音声認識後1.2秒で音声区切りが発生
- endpoint_config.rule3.min_trailing_silence: 最大30.1秒の認識後に音声区切りが発生

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
    "work_id": "asr.1001"
}
```
- created: メッセージ作成時刻（Unixタイム）
- work_id: 正常に作成されたwork_idユニット

## link
上流ユニットの出力をリンクします。

送信するJSON:
```json
{
    "request_id": "3",
    "work_id": "asr.1001",
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
    "work_id": "asr.1001"
}
```
error::codeが0の場合は実行成功を示します。

asrとkwsユニットをリンクすることで、kwsがウェイクアップデータを送信した時にasrユニットがユーザーの音声認識を開始し、認識後に自動的に一時停止して次のウェイクアップを待機します。

> **リンク時にはkwsが既に設定され動作していることを確認してください。また、setup段階でもリンクを行うことができます。**

例：
```json
{
    "request_id": "2",
    "work_id": "asr",
    "action": "setup",
    "object": "asr.setup",
    "data": {
        "model": "sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23",
        "response_format": "asr.utf-8.stream",
        "input": ["sys.pcm", "kws.1000"],
        "enoutput": true,
        "endpoint_config.rule1.min_trailing_silence": 2.4,
        "endpoint_config.rule2.min_trailing_silence": 1.2,
        "endpoint_config.rule3.min_trailing_silence": 30.1,
        "endpoint_config.rule1.must_contain_nonsilence": false,
        "endpoint_config.rule2.must_contain_nonsilence": false,
        "endpoint_config.rule3.must_contain_nonsilence": false
    }
}
```

## unlink
リンクを解除します。

送信するJSON:
```json
{
    "request_id": "4",
    "work_id": "asr.1001",
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
    "work_id": "asr.1001"
}
```
error::codeが0の場合は実行成功を示します。

## pause
ユニットの動作を一時停止します。

送信するJSON:
```json
{
    "request_id": "5",
    "work_id": "asr.1001",
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
    "work_id": "asr.1001"
}
```
error::codeが0の場合は実行成功を示します。

## work
ユニットの動作を再開します。

送信するJSON:
```json
{
    "request_id": "6",
    "work_id": "asr.1001",
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
    "work_id": "asr.1001"
}
```
error::codeが0の場合は実行成功を示します。

## exit
ユニットを終了します。

送信するJSON:
```json
{
    "request_id": "7",
    "work_id": "asr.1001",
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
    "work_id": "asr.1001"
}
```
error::codeが0の場合は実行成功を示します。

## タスク情報

タスクリストの取得：

送信するJSON:
```json
{
    "request_id": "2",
    "work_id": "asr",
    "action": "taskinfo"
}
```

レスポンスJSON:
```json
{
    "created":1731580350,
    "data":[
        "asr.1001"
    ],
    "error":{
        "code":0,
        "message":""
    },
    "object":"asr.tasklist",
    "request_id":"2",
    "work_id":"asr"
}
```

タスクの実行時パラメータの取得：

送信するJSON:
```json
{
    "request_id": "2",
    "work_id": "asr.1001",
    "action": "taskinfo"
}
```

レスポンスJSON:
```json
{
    "created":1731579679,
    "data":{
        "enoutput":false,
        "inputs_":[
            "sys.pcm"
            ],
        "model":"sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23",
        "response_format":"asr.utf-8-stream"
    },
    "error":{
        "code":0,
        "message":""
    },
    "object":"asr.taskinfo",
    "request_id":"2",
    "work_id":"asr.1001"
}
```

> **注意: work_idはユニットの初期化登録順に増加し、固定のインデックス値ではありません。**
