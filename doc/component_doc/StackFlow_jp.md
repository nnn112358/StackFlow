# StackFlow
StackFlowは、M5STACKによって開発された通信フレームワークで、主に組み込みLinuxプラットフォーム上で動作し、[zmq](https://zeromq.org/)が基盤となる通信サービスを提供しています。  
StackFlowは主に3つの機能を提供します：第一に、ユニット間の関数呼び出しのためのリモートRPC；第二に、より良いコンテキスト統合のための標準メッセージストリームサービスを提供するメッセージ通信；第三に、関連ユニット間の通信アドレスの競合を避け、一時的なデータストレージを提供するリソース割り当てです。

## pzmq
zmq APIは再パッケージ化され、ZMQ_PUB、ZMQ_SUB、ZMQ_PUSH、ZMQ_PULLの呼び出しをより簡単で便利にし、非同期コールバックメソッドを使用してメッセージ受信機能を提供します。  
ZMQ_REPとZMQ_REQの基礎の上に、シンプルなRPC機能がカプセル化され、RPCサービスを提供します。

### 関連例
1. ZMQ_PULL
```c++
/*
 * SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#include <iostream>
#include "pzmq.hpp"
#include <string>
using namespace StackFlows;
void pull_msg(const std::string &raw_msg){
    std::cout << raw_msg << std::endl;
}
int main(int argc, char *argv[]) {
    pzmq zpull_("ipc:///tmp.5000.socket", ZMQ_PULL, pull_msg);
    while(1) {
        sleep(1);
    }
    return 0;
}
```

2. ZMQ_PUSH
```c++
/*
 * SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#include <iostream>
#include "pzmq.hpp"
#include <string>
using namespace StackFlows;
int main(int argc, char *argv[]) {
    pzmq zpush_("ipc:///tmp.5000.socket", ZMQ_PUSH);
    zpush_.send_data("nihao");
    return 0;
}
```

3. ZMQ_PUB
```c++
/*
 * SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#include <iostream>
#include "pzmq.hpp"
#include <string>
using namespace StackFlows;
int main(int argc, char *argv[]) {
    pzmq zpush_("ipc:///tmp.5001.socket", ZMQ_PUB);
    zpush_.send_data("nihao");
    return 0;
}
```

4. ZMQ_SUB
```c++
/*
 * SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#include <iostream>
#include "pzmq.hpp"
#include <string>
using namespace StackFlows;
void sub_msg(const std::string &raw_msg){
    std::cout << raw_msg << std::endl;
}
int main(int argc, char *argv[]) {
    pzmq zpull_("ipc:///tmp.5001.socket", ZMQ_SUB, sub_msg);
    while(1) {
        sleep(1);
    }
    return 0;
}
```

5. ZMQ_RPC関数
```c++
/*
 * SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#include <iostream>
#include "pzmq.hpp"
#include <string>
using namespace StackFlows;
std::string fun1_(const std::string &raw_msg){
    std::cout << raw_msg << std::endl;
    return std::string("nihao");
}
std::string fun2_(const std::string &raw_msg){
    std::cout << raw_msg << std::endl;
    return std::string("hello");
}
int main(int argc, char *argv[]) {
    pzmq _rpc("test");
    _rpc.register_rpc_action("fun1", fun1_);
    _rpc.register_rpc_action("fun2", fun2_);
    while(1) {
        sleep(1);
    }
    return 0;
}
```

6. ZMQ_RPC呼び出し
```c++
/*
 * SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#include <iostream>
#include "pzmq.hpp"
#include <string>
using namespace StackFlows;
std::string fun1_(const std::string &raw_msg){
    return std::string("nihao");
}
std::string fun2_(const std::string &raw_msg){
    return std::string("hello");
}
int main(int argc, char *argv[]) {
    pzmq _rpc("test");
    _rpc.call_rpc_action("fun1", "call fun1_", [](const std::string &raw_msg){std::cout << raw_msg << std::endl;});
    _rpc.call_rpc_action("fun2", "call fun2_", [](const std::string &raw_msg){std::cout << raw_msg << std::endl;});
    return 0;
}
```

## StackFlow本体
StackFlowはpzmqとeventppをカプセル化し、加速ユニットの基本的なRPC機能、非同期処理、およびチャネル確立を提供します。  
StackFlowは、StackFlow JSONプロトコルの基本的な関数呼び出しのために7つの基本的なRPC機能を提供します：

- setup: ユニット設定機能、各ユニットが実装しなければならない機能です
- pause: ユニット機能の一時停止
- work: ユニット開始作業機能
- exit: ユニット終了機能、各ユニットが実装しなければならない機能です
- link: 上流出力機能へのリンク、メッセージ通信チェーンを構築するために使用
- unlink: 上流出力機能からのリンク解除、上流からのメッセージ受信を停止
- taskinfo: ユニット実行情報の取得

StackFlowはユニット使用のための便利なAPIを提供します：
- unit_call: ユニットRPC呼び出し機能、他のユニットのRPC機能を呼び出すため
- sys_sql_select: sysユニットの簡単なキーバリューデータベース照会機能
- sys_sql_set: sysユニットの簡単なキーバリューデータベース設定機能
- sys_sql_unset: sysユニットの簡単なキーバリューデータベース削除機能
- repeat_event: 非同期定期実行機能
- send: ユーザーメッセージ送信機能
- sys_register_unit: ユニット登録機能、通常は呼び出す必要はありません
- sys_release_unit: ユニット解放機能、通常は呼び出す必要はありません

llm_channel_objはユニットに必要な通信機能をカプセル化し、1つの設定が1つのllm_channel_objオブジェクトに対応します。  
llm_channel_objはユニット使用のための便利な通信APIを提供します：
- subscriber_work_id: 上流のwork_idユニットのpub出力を購読
- stop_subscriber_work_id: work_idの購読を解除
- subscriber: zmq URLのpub出力を購読
- stop_subscriber: zmq_urlの購読を解除
- send: このユニットのメッセージをpubを通じて送信

[以下、基本的な使用例のコード部分は原文のまま保持されているため省略]

## StackFlowUtil
以下のような簡単で使いやすい機能を提供します：
- sample_json_str_get: JSON内のキー値を読み取るシンプルな関数で、JSONオブジェクトを解析せずにJSONキーを素早く読み取るために使用
- sample_get_work_id_num: work_id文字列から数値インデックスを読み取る
- sample_get_work_id_name: work_id文字列からユニット名を読み取る
- sample_get_work_id: work_id文字列を合成するために使用
- sample_escapeString: 文字列内のエスケープ文字の単純なエンコード
- sample_unescapeString: 文字列内のエスケープ文字列の単純なデコード
- decode_stream: ストリーミングデータフローの解析
- decode_base64: base64のデコード
- encode_base64: base64のエンコード
