# <img src="https://download.gattxxa.org/StarRailDiscordRPC/favicon.ico" align="top" width="48"> StarRailDiscordRPC.exe  
**[崩壊：スターレイル](https://hsr.hoyoverse.com/)を起動している間、DiscordのアクティビティにRich Presenceで表示させるやつ。**  
Support to Japanese and English named window.
  
![screenshot](https://github.com/Gattxxa/StarRailDiscordRPC/assets/61118664/2c476d88-7a71-4c05-9897-7788fac16b6f)


## 使い方
### 概要
崩壊：スターレイルを起動している間、Discordのアクティビティに Rich Presence として反映します。  
起動後はタスクトレイに常駐します。右クリックで出現するメニューから終了させられます。  
このアプリケーションは多重起動できますが推奨しません。  
  
### パソコン起動時に自動で起動させる
1\. ` StarRailDiscordRPC.exe ` を分かりやすい場所に配置。（ドキュメントなど）  
2\. ` StarRailDiscordRPC.exe ` のショートカットを作成する。  
3\. [Win] + [R] の同時押しで開いたウィンドウに ` shell:startup ` と入力して OK を押す。  
4\. 開かれたフォルダに ` StarRailDiscordRPC.exe - ショートカット ` を配置する。  

## ダウンロード
セキュリティソフトに検知される場合がありますので、信頼できる方のみ利用してください。  

| Version  | Time | Download |
| - | - | - |
| **latest ☆**  | **undefined**  | **[こちら](https://github.com/Gattxxa/StarRailDiscordRPC/releases/latest)** |
| 1.0.3  | 2023-05-05  | 配布終了 |
| 1.0.2  | 2023-05-03  | 配布終了 |
| 1.0.1  | 2023-04-30  | 配布終了 |
| 1.0.0 | 2023-04-29 | 配布終了 |

## config.ini sample
```
[Profile]
UID = 123456789
Username = 三月なのか
Character = march7th
ButtonLabel = 『崩壊：スターレイル』公式サイト
URL = https://hsr.hoyoverse.com/
Version = x.y.z
```

## スペシャルサンクス
- [niveshbirangal / discord-rpc](https://github.com/niveshbirangal/discord-rpc)  
- [【Python編】DiscordRPCを使ってプロフィールに乗せるまで](https://qiita.com/taitaitatata/items/1bcec7c09424518fb2af)
- [Windows のタスクトレイに Python アプリを常駐させ定期的にプログラムを実行する](https://qiita.com/bassan/items/3025eeb6fd2afa03081b)  
- [Star Rail Station Wiki](https://starrailstation.com/)
