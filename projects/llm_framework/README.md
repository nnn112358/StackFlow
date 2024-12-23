# LLM
AX630C AIは大規模モデルのローカル音声アシスタントプログラムです。M5STACK STACKFLOWが基本的な通信アーキテクチャを提供し、複数の作業ユニットを協調して動作させます。

- llm-audio: オーディオユニット - システムのオーディオサポートを提供
- llm-kws: キーワード検出ユニット - キーワードによる起動サービスを提供 
- llm-asr: 音声認識ユニット - 音声からテキストへの変換サービスを提供
- llm-llm: 大規模モデルユニット - AI大規模モデルの推論サービスを提供
- llm-melotts: NPU加速TTSユニット - テキスト音声変換と再生サービスを提供
- llm-tts: CPU実行TTSユニット - テキスト音声変換と再生サービスを提供

## コンパイル
```bash
wget https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/linux/llm/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu.tar.gz
sudo tar zxvf gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu.tar.gz -C /opt

sudo apt install python3 python3-pip libffi-dev
pip3 install parse scons requests 

git clone https://github.com/m5stack/StackFlow.git
cd StackFlow
git submodule update --init
cd projects/llm_framework
scons distclean
scons -j22
```

## アシスタントモード
llm-sys、llm-audio、llm-kws、llm-asr、llm-llm、llm-melottsが協調動作します。

中国語環境:

1、リセット
送信:

```json
{
    "request_id": "11212155", 
    "work_id": "sys",
    "action": "reset"
}
```
リセット完了を待ちます!

2、全ユニットの初期化
送信:
```json
{
    "request_id": "1",
    "work_id": "kws",
    "action": "setup",
    "object": "kws.setup",
    "data": {
        "model": "sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01","response_format": "kws.bool",
        "input": "sys.pcm",
        "enoutput": true,
        "kws": "你好你好"
        }
}

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
        "enkws":true,
        "rule1":2.4,
        "rule2":1.2,
        "rule3":30.1
        }
}

{
    "request_id": "3",
    "work_id": "llm",
    "action": "setup","object": "llm.setup",
    "data": {
        "model": "qwen2.5-0.5B-prefill-20e",
        "response_format": "llm.utf-8.stream",
        "input": "llm.utf-8",
        "enoutput": true,
        "max_token_len": 256,
        "prompt": "You are a knowledgeable assistant capable of answering various questions and providing information."
        }
}

{
    "request_id": "4",
    "work_id": "melotts",
    "action": "setup",
    "object": "melotts.setup",
    "data": {
        "model": "melotts_zh-cn",
        "response_format": "sys.pcm",
        "input": "tts.utf-8",
        "enoutput": false
    }
}
```
work_idの返信を待ちます:
```json
{"created":1731488371,"data":"None","error":{"code":0,"message":""},"object":"None","request_id":"3","work_id":"asr.1001"}
{"created":1731488377,"data":"None","error":{"code":0,"message":""},"object":"None","request_id":"4","work_id":"llm.1002"}
{"created":1731488392,"data":"None","error":{"code":0,"message":""},"object":"None","request_id":"4","work_id":"melotts.1003"}
{"created":1731488402,"data":"None","error":{"code":0,"message":""},"object":"None","request_id":"2","work_id":"kws.1000"}
```

アセンブリラインの作成：
```json
{
    "request_id": "2",
    "work_id": "asr.1001",
    "action": "link",
    "object":"work_id",
    "data":"kws.1000"
}

{
    "request_id": "3",
    "work_id": "llm.1002",
    "action": "link",
    "object":"work_id",
    "data":"asr.1001"
}

{
    "request_id": "4",
    "work_id": "melotts.1003",
    "action": "link",
    "object":"work_id",
    "data":"llm.1002"
}

{
    "request_id": "3",
    "work_id": "llm.1002",
    "action": "link",
    "object":"work_id",
    "data":"kws.1000"
}
{
    "request_id": "4",
    "work_id": "melotts.1003",
    "action": "link",
    "object":"work_id",
    "data":"kws.1000"
}

```

ステータスの返信を待ちます:
```json
{"created":1731488403,"data":"None","error":{"code":0,"message":""},"object":"None","request_id":"3","work_id":"llm.1002"}
{"created":1731488403,"data":"None","error":{"code":0,"message":""},"object":"None","request_id":"4","work_id":"melotts.1003"}
{"created":1731488403,"data":"None","error":{"code":0,"message":""},"object":"None","request_id":"2","work_id":"asr.1001"}
{"created":1731488403,"data":"None","error":{"code":0,"message":""},"object":"None","request_id":"4","work_id":"melotts.1003"}
{"created":1731488403,"data":"None","error":{"code":0,"message":""},"object":"None","request_id":"3","work_id":"llm.1002"}
```


**大規模モデル音声アシスタントをお楽しみください。**
