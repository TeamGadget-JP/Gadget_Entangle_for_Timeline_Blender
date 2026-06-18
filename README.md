# 日本語 #
# Gadget Entangle for Timeline / Blender (GETLB)

GETLBはその時の作業内容により、どちらをマスターとして働かせるのかを決めるスイッチング方式を採用し、<br>
双方のタイムラインを同期する事をメイン機能としています。<br>
また、時間を制御することでFBXファイル等に頼らずリアルタイム同期しているキャラクターのモーションを<br>
その場でタイムラインに記録する、オフラインベイク機能も実装。<br>
タイムラインをコントロール・ベイクする事に特化した無料ツールです。<br>

---

## GETLBの主要機能<br>

1. スイッチング方式、双方向タイムライン同期。<br>
2. ワンクリック・アニメーションベイク機能。<br>
3. フレーム欠けを防止するベイク間隔設定に対応。<br>
4. 全体ベイクのみならず部分ベイクへの対応。<br>

---

## 動作環境

- Windows専用
  GETLBはコード内でWindows APIを使用している為、Windows専用となります。<br>
- GETLBはGECBの導入が前提です。<br>
- ローカルポート : 8993 `Blender -> Cascadeur`<br>
- ローカルポート : 8994 `Cascadeur -> Blender`<br>

## 重要事項

- ベイクされたデータはゼロ・キャリブレーションされたキャラクターにのみ正常に作用します。<br>
　シーン内でゼロ・キャリブレーションされたキャラクターをBlender内で完結するなら問題はありません。<br>
  UEやUnity等のエンジン、他のDCCにアニメーション付きのキャラクターを出力する際は従来通りのFBX<br>
　を適用する方法をとってください。<br>

---

## 導入手順と使用方法

## 導入手順<br>
1. `GETLB_Cascadeur_v1_0.py`をCascadeurのPythonプラグインフォルダに配置します。<br>
   `[Cascadeurインストール先]\resources\scripts\python\commands\`<br>
2. `GETLB_Blender_v1_0.py`をBlenderのアドオン登録します。<br> 

## 使用方法<br>
step1: Cascadeurを起動して`ツールバー -> Commands -> GETLB TimeLine Sync(v1_0)`を選択。<br>
step2: Cascadeurのシーンビュー右下に`[GETLB] Running! (Rev:8993/Send:8994)`と表示されればOKです。<br>
step3: <br>
step4: <br>
step5: <br>
step6: <br>
step7: <br>
step8: <br>
step9: <br>
step10:<br>

GETLBを使用されてもし良かったら、チャネル登録、高評価の方をお願いします。<br>
皆様からの評価、温かい支援が今後の開発の励みになります。<br>
YouTube:[https://www.youtube.com/@TeamGadget](https://www.youtube.com/channel/UCj9OYwzMAIgYAeVkTV4wczw)

## フィードバックのお願い

ツールを一緒に育ててみませんか？
使用者様からの感想やご意見は、今後のツールアップデートに深く影響を与えます。<br>
オープンソースソフトウェアの最大の強みはそこにあると言っても過言ではありません。<br>
制作環境に根付くより良いツールに育てて行きましょう。<br>

---

## サポートについて

GETLBは完全無料・現状渡しで提供されます。<br>

開発者は普段、別の本業を抱えるFA系個人エンジニアです。<br> 
そのため、個別の環境に合わせた技術サポートを提供することは事実上不可能です。<br>

本ツールは以下の条件で提供されます。<br>

- 完全無料<br>
- サポートなし<br>
- 無保証<br>
- 自己責任での利用がベースとなります<br>

バグ不具合報告へはできる限り対応しますよう心掛けますが、不定期がちになってしまいます。<br>
ご理解のほど、よろしくお願いします。<br>

---

## 免責事項

GETLBはTeamGadgetによる独立したプロジェクトです。<br>

CascadeurはNekkiの商標または財産です。<br>  
BlenderはBlender Foundationの商標または財産です。<br>

本プロジェクトは、NekkiまたはBlender Foundationによる公式製品ではなく、承認、提携、<br>
スポンサー提供、または公式サポートを受けたものではありません。<br>
