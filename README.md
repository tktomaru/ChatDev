# ChatDev 2.0 - DevAll

<p align="center">
  <img src="frontend/public/media/logo.png" alt="DevAll Logo" width="500"/>
</p>


<p align="center">
  <strong>あらゆるものを開発するためのゼロコード・マルチエージェントプラットフォーム</strong>
</p>

<p align="center">
  【<a href="./README.md">English</a> | <a href="./README-zh.md">简体中文</a> | <a href="./README_ja.md">日本語</a>】
</p>
<p align="center">
    【📚 <a href="#developers">開発者向け</a> | 👥 <a href="#primary-contributors">コントリビューター</a>｜⭐️ <a href="https://github.com/OpenBMB/ChatDev/tree/chatdev1.0">ChatDev 1.0 (レガシー)</a>】
</p>

## 📖 概要
ChatDevは、専門的なソフトウェア開発マルチエージェントシステムから、包括的なマルチエージェントオーケストレーションプラットフォームへと進化しました。

- <a href="https://github.com/OpenBMB/ChatDev/tree/main">**ChatDev 2.0 (DevAll)**</a> は「あらゆるものを開発する」ための**ゼロコード・マルチエージェントプラットフォーム**です。シンプルな設定でカスタマイズされたマルチエージェントシステムを迅速に構築・実行できます。コーディングは不要で、エージェント、ワークフロー、タスクを定義することで、データ可視化、3D生成、深層調査などの複雑なシナリオをオーケストレーションできます。
- <a href="https://github.com/OpenBMB/ChatDev/tree/chatdev1.0">**ChatDev 1.0 (レガシー)**</a> は**仮想ソフトウェア会社**として動作します。様々なインテリジェントエージェント（例：CEO、CTO、プログラマー）が専門的な機能セミナーに参加し、設計、コーディング、テスト、ドキュメント作成を含むソフトウェア開発ライフサイクル全体を自動化します。これはコミュニケーションエージェントの協調における基盤的パラダイムとして機能します。

## 🎉 ニュース
• **2026年1月7日: 🚀 ChatDev 2.0 (DevAll) の正式リリースを発表しました！** このバージョンでは、ゼロコードのマルチエージェントオーケストレーションプラットフォームを導入しています。従来のChatDev (v1.x) はメンテナンスのため [`chatdev1.0`](https://github.com/OpenBMB/ChatDev/tree/chatdev1.0) ブランチに移動されました。ChatDev 2.0 の詳細は[公式投稿](https://x.com/OpenBMB/status/2008916790399701335)をご覧ください。

<details>
<summary>過去のニュース</summary>

•2025年9月24日: 🎉 私たちの論文 [Multi-Agent Collaboration via Evolving Orchestration](https://arxiv.org/abs/2505.19591) が NeurIPS 2025 に採択されました。実装はこのリポジトリの `puppeteer` ブランチで利用可能です。

•2025年5月26日: 🎉 大規模言語モデルベースのエージェント間のマルチエージェント協調のための新しいパペティアスタイルのパラダイムを提案しました。強化学習で最適化された学習可能な中央オーケストレーターを活用することで、我々の手法はエージェントを動的に活性化・シーケンス化し、効率的でコンテキスト対応の推論パスを構築します。このアプローチは推論品質を向上させるだけでなく、計算コストを削減し、複雑なタスクにおけるスケーラブルで適応可能なマルチエージェント協調を可能にします。
論文は [Multi-Agent Collaboration via Evolving Orchestration](https://arxiv.org/abs/2505.19591) をご覧ください。
  <p align="center">
  <img src='./assets/puppeteer.png' width=800>
  </p>

•2024年6月25日: 🎉LLMを活用したマルチエージェント協調🤖🤖および関連分野の発展を促進するため、ChatDevチームは重要な論文📄を収集し、[オープンソース](https://github.com/OpenBMB/ChatDev/tree/main/MultiAgentEbook)のインタラクティブ電子書籍📚形式で提供しています。[Ebook Website](https://thinkwee.top/multiagent_ebook)で最新の進歩を探索し、[論文リスト](https://github.com/OpenBMB/ChatDev/blob/main/MultiAgentEbook/papers.csv)をダウンロードできます。
  <p align="center">
  <img src='./assets/ebook.png' width=800>
  </p>

•2024年6月12日: マルチエージェント協調ネットワーク（MacNet）🎉を導入しました。有向非巡回グラフを活用して、言語的インタラクションを通じてエージェント間の効果的なタスク指向の協調を促進します。MacNetは様々なトポロジーや1000以上のエージェントでの協調をコンテキスト制限を超えることなくサポートします。より汎用的でスケーラブルなMacNetは、ChatDevのチェーン型トポロジーのより高度なバージョンと考えることができます。プレプリント論文は [https://arxiv.org/abs/2406.07155](https://arxiv.org/abs/2406.07155) で利用可能です。この技術は [macnet](https://github.com/OpenBMB/ChatDev/tree/macnet) ブランチに組み込まれており、多様な組織構造のサポートを強化し、ソフトウェア開発以外（例：論理的推論、データ分析、ストーリー生成など）のより豊富なソリューションを提供します。
  <p align="center">
  <img src='./assets/macnet.png' width=500>
  </p>

• 2024年5月7日、「反復的経験改良」（IER）を導入しました。これは、インストラクターとアシスタントエージェントがショートカット指向の経験を強化し、新しいタスクに効率的に適応する新しい手法です。このアプローチは、一連のタスクにわたる経験の獲得、活用、伝播、除去を包括し、プロセスをより短く効率的にします。プレプリント論文は https://arxiv.org/abs/2405.04219 で利用可能で、この技術は間もなくChatDevに組み込まれる予定です。
  <p align="center">
  <img src='./assets/ier.png' width=220>
  </p>

• 2024年1月25日: 経験的共同学習モジュールをChatDevに統合しました。[経験的共同学習ガイド](wiki.md#co-tracking)をご覧ください。

• 2023年12月28日: 経験的共同学習を発表しました。これは、インストラクターとアシスタントエージェントがショートカット指向の経験を蓄積し、新しいタスクを効果的に解決し、繰り返しのエラーを減らし、効率を向上させる革新的なアプローチです。プレプリント論文は https://arxiv.org/abs/2312.17025 でご覧いただけます。この技術は間もなくChatDevに統合される予定です。
  <p align="center">
  <img src='./assets/ecl.png' width=860>
  </p>
• 2023年11月15日: ChatDevをSaaSプラットフォームとしてローンチしました。これにより、ソフトウェア開発者や革新的な起業家が非常に低コストで効率的にソフトウェアを構築でき、参入障壁が取り除かれます。https://chatdev.modelbest.cn/ でお試しください。
  <p align="center">
  <img src='./assets/saas.png' width=560>
  </p>

• 2023年11月2日: ChatDevは増分開発という新機能をサポートするようになりました。これにより、エージェントは既存のコードを基に開発できます。```--config "incremental" --path "[source_code_directory_path]"``` で開始してください。
  <p align="center">
  <img src='./assets/increment.png' width=700>
  </p>

• 2023年10月26日: ChatDevは安全な実行のためにDockerをサポートするようになりました（[ManindraDeMel](https://github.com/ManindraDeMel)の貢献に感謝します）。[Docker開始ガイド](wiki.md#docker-start)をご覧ください。
  <p align="center">
  <img src='./assets/docker.png' width=400>
  </p>

• 2023年9月25日: **Git** モードが利用可能になりました。プログラマー <img src='visualizer/static/figures/programmer.png' height=20> がGitを使用してバージョン管理を行えます。この機能を有効にするには、``ChatChainConfig.json`` で ``"git_management"`` を ``"True"`` に設定してください。[ガイド](wiki.md#git-mode)を参照してください。
  <p align="center">
  <img src='./assets/github.png' width=600>
  </p>

• 2023年9月20日: **人間-エージェント間インタラクション** モードが利用可能になりました！レビュアー <img src='visualizer/static/figures/reviewer.png' height=20> の役割を担い、プログラマー <img src='visualizer/static/figures/programmer.png' height=20> に提案を行うことで、ChatDevチームに参加できます。``python3 run.py --task [description_of_your_idea] --config "Human"`` をお試しください。[ガイド](wiki.md#human-agent-interaction)と[例](WareHouse/Gomoku_HumanAgentInteraction_20230920135038)を参照してください。
  <p align="center">
  <img src='./assets/Human_intro.png' width=600>
  </p>

• 2023年9月1日: **Art** モードが利用可能になりました！デザイナーエージェント <img src='visualizer/static/figures/designer.png' height=20> を有効にして、ソフトウェアで使用される画像を生成できます。``python3 run.py --task [description_of_your_idea] --config "Art"`` をお試しください。[ガイド](wiki.md#art)と[例](WareHouse/gomokugameArtExample_THUNLP_20230831122822)を参照してください。

• 2023年8月28日: システムが一般公開されました。

• 2023年8月17日: v1.0.0バージョンがリリース準備完了しました。

• 2023年7月30日: ユーザーはChatChain、Phase、Role設定をカスタマイズできるようになりました。また、オンラインログモードとリプレイモードの両方がサポートされるようになりました。

• 2023年7月16日: このプロジェクトに関連する[プレプリント論文](https://arxiv.org/abs/2307.07924)が公開されました。

• 2023年6月30日: ChatDevリポジトリの初期バージョンがリリースされました。
</details>


## 🚀 クイックスタート

### 📋 前提条件

*   **OS**: macOS / Linux / WSL / Windows
*   **Python**: 3.12以上
*   **Node.js**: 18以上
*   **パッケージマネージャー**: [uv](https://docs.astral.sh/uv/)

### 📦 インストール

1.  **バックエンド依存関係** (Pythonは`uv`で管理):
    ```bash
    uv sync
    ```

2.  **フロントエンド依存関係** (Vite + Vue 3):
    ```bash
    cd frontend && npm install
    ```

### ⚡️ アプリケーションの実行

1.  **バックエンドの起動**:
    ```bash
    # プロジェクトルートから実行
    uv run python server_main.py --port 6400 --reload
    ```
    > 出力ファイル（例：GameDev）が再起動をトリガーする場合は `--reload` を削除してください。タスクが中断され、進捗が失われる可能性があります。

2.  **フロントエンドの起動**:
    ```bash
    cd frontend
    VITE_API_BASE_URL=http://localhost:6400 npm run dev
    ```
    > その後、**[http://localhost:5173](http://localhost:5173)** でWebコンソールにアクセスできます。


    > **💡 ヒント**: フロントエンドがバックエンドに接続できない場合、デフォルトポート `6400` が既に使用されている可能性があります。
    > 両方のサービスを利用可能なポートに切り替えてください。例：
    >
    > * **バックエンド**: `--port 6401` で起動
    > * **フロントエンド**: `VITE_API_BASE_URL=http://localhost:6401` を設定


### 🔑 設定

*   **環境変数**: プロジェクトルートに `.env` ファイルを作成します。
*   **モデルキー**: LLMプロバイダー用に `.env` で `API_KEY` と `BASE_URL` を設定します。
*   **YAMLプレースホルダー**: 設定ファイルで `${VAR}`（例：`${API_KEY}`）を使用してこれらの変数を参照します。

---

## 💡 使い方

### 🖥️ Webコンソール

DevAllインターフェースは、構築と実行の両方でシームレスな体験を提供します。

*   **チュートリアル**: 包括的なステップバイステップガイドとドキュメントがプラットフォームに直接統合されており、すぐに始められます。
<img src="assets/tutorial-en.png"/>

*   **ワークフロー**: マルチエージェントシステムを設計するための視覚的なキャンバス。ノードパラメータを設定し、コンテキストフローを定義し、ドラッグ＆ドロップで複雑なエージェントインタラクションをオーケストレーションできます。
<img src="assets/workflow.gif"/>

*   **起動**: ワークフローを開始し、リアルタイムログを監視し、中間成果物を検査し、ヒューマン・イン・ザ・ループのフィードバックを提供します。
<img src="assets/launch.gif"/>

### 🧰 Python SDK
自動化やバッチ処理のために、軽量なPython SDKを使用してプログラム的にワークフローを実行し、結果を直接取得できます。

```python
from runtime.sdk import run_workflow

# ワークフローを実行し、最終ノードのメッセージを取得
result = run_workflow(
    yaml_file="yaml_instance/demo.yaml",
    task_prompt="添付されたドキュメントを一文で要約してください。",
    attachments=["/path/to/document.pdf"],
    variables={"API_KEY": "sk-xxxx"} # 必要に応じて.env変数を上書き
)

if result.final_message:
    print(f"出力: {result.final_message.text_content()}")
```

---

<a id="developers"></a>
## ⚙️ 開発者向け

**二次開発や拡張については、このセクションをお進みください。**

新しいノード、プロバイダー、ツールでDevAllを拡張できます。
プロジェクトはモジュラー構造で構成されています：
*   **コアシステム**: `server/` はFastAPIバックエンドをホストし、`runtime/` はエージェントの抽象化とツール実行を管理します。
*   **オーケストレーション**: `workflow/` は `entity/` の設定に基づいてマルチエージェントロジックを処理します。
*   **フロントエンド**: `frontend/` にはVue 3 Webコンソールが含まれています。
*   **拡張性**: `functions/` はカスタムPythonツールの場所です。

関連リファレンスドキュメント：
*   **はじめに**: [スタートガイド](./docs/user_guide/en/index.md)
*   **コアモジュール**: [ワークフロー作成](./docs/user_guide/en/workflow_authoring.md)、[メモリ](./docs/user_guide/en/modules/memory.md)、[ツール](./docs/user_guide/en/modules/tooling/index.md)

---

## 🌟 注目のワークフロー
一般的なシナリオ向けの堅牢ですぐに使えるテンプレートを提供しています。すべての実行可能なワークフロー設定は `yaml_instance/` にあります。
*   **デモ**: `demo_*.yaml` という名前のファイルは、特定の機能やモジュールを紹介します。
*   **実装**: 直接名前が付けられたファイル（例：`ChatDev_v1.yaml`）は、完全な社内または再現されたワークフローです。以下のとおりです：

### 📋 ワークフローコレクション

| カテゴリ | ワークフロー | ケース |
| :--- |:------------------------------------------------------------------------------------------------------------| :--- |
| **📈 データ可視化** | `data_visualization_basic.yaml`<br>`data_visualization_enhanced.yaml`                                       | <img src="assets/cases/data_analysis/data_analysis.gif" width="100%"><br>プロンプト: *「大規模な不動産取引データセット用に4〜6個の高品質なPNGチャートを作成してください。」* |
| **🛠️ 3D生成**<br>*([Blender](https://www.blender.org/) と [blender-mcp](https://github.com/ahujasid/blender-mcp) が必要)* | `blender_3d_builder_simple.yaml`<br>`blender_3d_builder_hub.yaml`<br>`blender_scientific_illustration.yaml` | <img src="assets/cases/3d_generation/3d.gif" width="100%"><br>プロンプト: *「クリスマスツリーを作ってください。」* |
| **🎮 ゲーム開発** | `GameDev_v1.yaml`<br>`ChatDev_v1.yaml`                                                                      | <img src="assets/cases/game_development/game.gif" width="100%"><br>プロンプト: *「タンクバトルゲームの設計と開発を手伝ってください。」* |
| **📚 深層調査** | `deep_research_v1.yaml`                                                                                     | <img src="assets/cases/deep_research/deep_research.gif" width="85%"><br>プロンプト: *「LLMベースのエージェント強化学習分野における最近の進歩について調査してください」* |
| **🎓 教育ビデオ** | `teach_video.yaml` (このワークフローを実行する前に `uv add manim` コマンドを実行してください)                         | <img src="assets/cases/video_generation/video.gif" width="140%"><br>プロンプト: *「凸最適化とは何か説明してください」* |

---

### 💡 使用ガイド
これらの実装については、**起動** タブを使用して実行できます。
1.  **選択**: **起動** タブでワークフローを選択します。
2.  **アップロード**: 必要に応じて必要なファイル（例：データ分析用の `.csv`）をアップロードします。
3.  **プロンプト**: リクエストを入力します（例：*「売上トレンドを可視化して」* または *「スネークゲームを設計して」*）。

---

## 🤝 コントリビューション

コミュニティからの貢献を歓迎します！バグ修正、新しいワークフローテンプレートの追加、DevAllで作成された高品質なケース/成果物の共有など、どのような貢献も大変ありがたく思います。**Issue** や **Pull Request** を送信してお気軽にご貢献ください。

DevAllに貢献いただくと、以下の**コントリビューター**リストに掲載されます。始めるには[開発者ガイド](#developers)をご覧ください！

### 👥 コントリビューター

#### 主要コントリビューター

<table>
  <tr>
    <td align="center"><a href="https://github.com/NA-Wen"><img src="https://github.com/NA-Wen.png?size=100" width="64px;" alt=""/><br /><sub><b>NA-Wen</b></sub></a></td>
    <td align="center"><a href="https://github.com/zxrys"><img src="https://github.com/zxrys.png?size=100" width="64px;" alt=""/><br /><sub><b>zxrys</b></sub></a></td>
    <td align="center"><a href="https://github.com/swugi"><img src="https://github.com/swugi.png?size=100" width="64px;" alt=""/><br /><sub><b>swugi</b></sub></a></td>
    <td align="center"><a href="https://github.com/huatl98"><img src="https://github.com/huatl98.png?size=100" width="64px;" alt=""/><br /><sub><b>huatl98</b></sub></a></td>
  </tr>
</table>

#### コントリビューター
<table>
  <tr>
    <td align="center"><a href="https://github.com/shiowen"><img src="https://github.com/shiowen.png?size=100" width="64px;" alt=""/><br /><sub><b>shiowen</b></sub></a></td>
    <td align="center"><a href="https://github.com/kilo2127"><img src="https://github.com/kilo2127.png?size=100" width="64px;" alt=""/><br /><sub><b>kilo2127</b></sub></a></td>
    <td align="center"><a href="https://github.com/AckerlyLau"><img src="https://github.com/AckerlyLau.png?size=100" width="64px;" alt=""/><br /><sub><b>AckerlyLau</b></sub></a></td>
</table>

## 🤝 謝辞

<a href="http://nlp.csai.tsinghua.edu.cn/"><img src="assets/thunlp.png" height=50pt></a>&nbsp;&nbsp;
<a href="https://modelbest.cn/"><img src="assets/modelbest.png" height=50pt></a>&nbsp;&nbsp;
<a href="https://github.com/OpenBMB/AgentVerse/"><img src="assets/agentverse.png" height=50pt></a>&nbsp;&nbsp;
<a href="https://github.com/OpenBMB/RepoAgent"><img src="assets/repoagent.png"  height=50pt></a>
<a href="https://app.commanddash.io/agent?github=https://github.com/OpenBMB/ChatDev"><img src="assets/CommandDash.png" height=50pt></a>
<a href="www.teachmaster.cn"><img src="assets/teachmaster.png" height=50pt></a>
<a href="https://github.com/OpenBMB/AppCopilot"><img src="assets/appcopilot.png" height=50pt></a>

## 🔎 引用

```
@article{chatdev,
    title = {ChatDev: Communicative Agents for Software Development},
    author = {Chen Qian and Wei Liu and Hongzhang Liu and Nuo Chen and Yufan Dang and Jiahao Li and Cheng Yang and Weize Chen and Yusheng Su and Xin Cong and Juyuan Xu and Dahai Li and Zhiyuan Liu and Maosong Sun},
    journal = {arXiv preprint arXiv:2307.07924},
    url = {https://arxiv.org/abs/2307.07924},
    year = {2023}
}

@article{colearning,
    title = {Experiential Co-Learning of Software-Developing Agents},
    author = {Chen Qian and Yufan Dang and Jiahao Li and Wei Liu and Zihao Xie and Yifei Wang and Weize Chen and Cheng Yang and Xin Cong and Xiaoyin Che and Zhiyuan Liu and Maosong Sun},
    journal = {arXiv preprint arXiv:2312.17025},
    url = {https://arxiv.org/abs/2312.17025},
    year = {2023}
}

@article{macnet,
    title={Scaling Large-Language-Model-based Multi-Agent Collaboration},
    author={Chen Qian and Zihao Xie and Yifei Wang and Wei Liu and Yufan Dang and Zhuoyun Du and Weize Chen and Cheng Yang and Zhiyuan Liu and Maosong Sun}
    journal={arXiv preprint arXiv:2406.07155},
    url = {https://arxiv.org/abs/2406.07155},
    year={2024}
}

@article{iagents,
    title={Autonomous Agents for Collaborative Task under Information Asymmetry},
    author={Wei Liu and Chenxi Wang and Yifei Wang and Zihao Xie and Rennai Qiu and Yufan Dnag and Zhuoyun Du and Weize Chen and Cheng Yang and Chen Qian},
    journal={arXiv preprint arXiv:2406.14928},
    url = {https://arxiv.org/abs/2406.14928},
    year={2024}
}

@article{puppeteer,
      title={Multi-Agent Collaboration via Evolving Orchestration},
      author={Yufan Dang and Chen Qian and Xueheng Luo and Jingru Fan and Zihao Xie and Ruijie Shi and Weize Chen and Cheng Yang and Xiaoyin Che and Ye Tian and Xuantang Xiong and Lei Han and Zhiyuan Liu and Maosong Sun},
      journal={arXiv preprint arXiv:2505.19591},
      url={https://arxiv.org/abs/2505.19591},
      year={2025}
}
```

## 📬 お問い合わせ

ご質問、フィードバック、またはお問い合わせがございましたら、[qianc62@gmail.com](mailto:qianc62@gmail.com) までお気軽にメールでご連絡ください。
