# Gadget Entangle for Timeline / Blender (GETLB)

GETLB features a master-switching system that allows you to decide which application acts as the master depending on your current task, with its main function being the synchronization of timelines between both sides.<br>
Additionally, by controlling time, it implements an "Offline Bake" function that records real-time synchronized character motions directly onto the timeline on the fly, without relying on FBX files.<br>
This is a free tool specifically designed for controlling and baking timelines.<br>

---

## Key Features of GETLB<br>

1. Master-switching, bidirectional timeline synchronization.<br>
2. One-click animation baking.<br>
3. Customizable bake interval settings to prevent dropped frames.<br>
4. Support for both full-range baking and partial-range baking.<br>

---

## Operating Environment

- **Windows Only**
  GETLB utilizes Windows APIs within its code, making it strictly Windows-exclusive.<br>
- **Requires GECB** to be installed beforehand.<br>
- Local Port: `8993` `Blender -> Cascadeur`<br>
- Local Port: `8994` `Cascadeur -> Blender`<br>

## Important Notes

- Baked data will only function correctly on characters that have been **zero-calibrated**.<br>
  There is no issue if you complete your workflow entirely within Blender using a zero-calibrated character in the scene.<br>
  When exporting animated characters to game engines like UE/Unity or other DCC software, please use the traditional method of applying an FBX file.<br>

---

## Installation & Usage

## Installation Procedure<br>
1. Place `GETLB_Cascadeur_v1_0.py` into Cascadeur's Python plugin folder.<br>
   `[Cascadeur Installation Path]\resources\scripts\python\commands\`<br>
2. Install `GETLB_Blender_v1_0.py` as an add-on in Blender.<br> 

## How to Use<br>
step1: Launch Cascadeur and navigate to `Toolbar -> Commands -> GETLB TimeLine Sync(v1_0)`.<br>
step2: Ensure that `[GETLB] Running! (Rev:8993/Send:8994)` is displayed at the bottom right of Cascadeur's scene view.<br>
step3: Open the N-panel in Blender and verify that `Timeline Sync(GETLB)` is present under the `GECB TAB`.<br>
step4: Click the `Enable Timeline Sync` button to complete the synchronization.<br>
step5: When the **Blender** button is toggled ON, Blender's timeline becomes the master controller.<br>
step6: When the **Cascadeur** button is toggled ON, Cascadeur's timeline becomes the master controller.<br>

## Offline Baking<br>
Set the Blender side as the master. Switch to `Pose Mode` and make sure the bones are visible.<br>
Select all bones by pressing the `A key`. Set your desired frames in the `Start` and `End` fields.<br>
For `Bake Delay(s)`, starting with the default value of `0.20` should be fine. If some frames are not captured properly, try increasing this value.<br>
After that, simply click the `Bake from Cascadeur` button to start baking.<br>
This concludes the explanation for baking operations.

If you find GETLB useful, please subscribe to the channel and give it a thumbs-up!<br>
Your ratings and warm support deeply motivate future development.<br>
YouTube: [https://www.youtube.com/@TeamGadget](https://www.youtube.com/channel/UCj9OYwzMAIgYAeVkTV4wczw)

## Call for Feedback

Would you like to help grow this tool together?
Your feedback and opinions as a user will heavily influence future tool updates.<br>
It is no exaggeration to say that this is the greatest strength of open-source software.<br>
Let’s nurture it into a better tool that roots itself deeply into actual production environments.<br>

---

## About Support

GETLB is provided completely free of charge on an "as-is" basis.<br>

The developer is an individual FA (Factory Automation) engineer with a separate day job.<br> 
Therefore, providing technical support tailored to individual environments is virtually impossible.<br>

This tool is provided under the following conditions:<br>

- Completely Free<br>
- No Support<br>
- No Warranty<br>
- Use at your own risk<br>

I will do my best to respond to bug and issue reports, but updates may be irregular.<br>
Thank you for your understanding.<br>

---

## Disclaimer

GETLB is an independent project by TeamGadget.<br>

Cascadeur is a trademark or property of Nekki.<br> 
Blender is a trademark or property of the Blender Foundation.<br>

This project is not an official product of Nekki or the Blender Foundation, and is not endorsed, affiliated, sponsored, or officially supported by either organization.<br>

---

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
step3: Blender側でN-パネルを開き`GECB TAB`に`Timeline Sync(GETLB)`があることを確認して下さい。<br>
step4: `Enable Timeline Sync`ボタンを押せば同期完了です。<br>
step5: BlenderボタンがオンでBlender側タイムラインがマスターコントローラーになります。<br>
step6: CascadeurボタンがオンでCascadeur側タイムラインがマスターコントローラーになります。<br>

## オフラインベイク<br>
Blender側をマスターにします。`Pose Mode`に切り替えて、更にボーンを表示して下さい。
ボーンを全選択`Aキー`します。`Start`と`End`に任意のフレームを設定して下さい。
`Bake Delay(s)`はまずはデフォルトの`0.20`で良いと思います。上手く拾えない場合は数値を上げて下さい。
後は`Bake from Cascadeur`ボタンを押せばベイクを開始します。
以上でベイク操作説明は終わりです。

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
