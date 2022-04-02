package ini;
#ini:設定

#掲示板の名前
$bbsName = "BBS";

#掲示板の説明
$bbsDescription = "掲示板です。";

#パスワード
$password = "password";

#サイト
$site = "";

#データフォルダ名
$data = "data";

#ロックフォルダ名
$lockdir = "lock";

#ファイルのパーミッション
$filePermission = 0666;

#名無しの名前（""なら名無しを許可しない）
$noName = "";

#パスワード無しを許可するか（1なら許可、0なら許可しない）
$noPassword = 0;

# 1ページのスレッドの数
$page_threads=5;

# 1ページのレスの数
$page_res=5;

# 検索時の最大表示件数
$search_max=50;

# 誰でも自分の投稿を削除できるか
$delete_free=1;

# トリップ機能を使用するか
$use_trip=0;

# アクセス禁止機能を使用するか
$use_akukin=0;

return 1;
