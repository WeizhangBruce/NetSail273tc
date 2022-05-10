# 基本設置
$ver		= '2.73';	#遊戲版本
$title		= '網路航海時代';	# 遊戲標題（上部）

$adps		= '0123';	# 管理者密碼（※必須更改）
$usrdir		= 'usrdir';	# 玩家帳戶資料存放目錄（※必須更改）
$datadir	= 'data';	# 遊戲資料存放目錄（※必須更改）
$citydir	= 'city';	# 城鎮資料存放目錄（※必須更改）
$img		= './img';	# 遊戲圖像存放目錄
$method		= 'POST';	# POST or GET（推薦POST）
$cookname	= 'NETKO';	# Cookie名稱(推薦更改)
$def_cp		= 0;		# 密碼加密(1=yes,0=no)
$def_ip		= 1;		# IP制限(開啟：1 or 2、關閉：0) ※1的場合非對應瀏覽器變得不能創立帳戶。
$def_ei		= 'esc';	# 暗碼(在密碼的開頭鍵入的話能迴避IP的限制※必須變更)
$def_dead	= 5;		# 未更新削除（日）

$hom_url	= 'http://';	# 遊戲的所屬網站URL
$hom_tgt	= '_self';	# 網頁開啟方式(トップ='_top',自身='_self',新視窗開啟='_blank')
$hom_lbl	= '<請自行設置>';	# 網站名稱
$def_ho		= 1;		# 是否要顯示「所屬網站的URL」(yes = 1,no = 0)
$sub_lbl	= 'OK';		# "確認"的按鈕名稱
$bak_lbl	= '返回';	# 返回的按鈕名稱
$bdcol		= '#000000';	# 框架顏色
$t_bgcol	= '#e9e2ce';	# 操作介面顏色

$body		= '<body bgcolor=#eacd9f text=#000000>'; #外圍介面顏色

# 以下是有關連結的設定
$before	= '#4169e1'; # 超連結的顏色(未)
$after	= '#4169e1'; # 超連結的顏色(既)
$over	= '#FF0000'; # 超連結的顏色(現)
$style = qq|
<STYLE TYPE="text/css">
	<!--
	body,tr,td,th { font-size: 10pt }
	A:link	{ text-decoration:none;color:$before;font-weight:bold }
	A:visited { text-decoration:none;color:$after;font-weight:bold }
	A:hover   { text-decoration:none;color:$over;font-weight:bold }
	.button	{ border:solid;border-width:1pt 2pt;border-color:#633000;background-color:#fff3e6}
	-->
	</STYLE>|;
#.text   {  } 追加可能
# スタイルシートここまで
$body .= $style;

$stx_wth	= 20;		# テキスト入力欄の幅(小)
$ltx_wth	= 35;		# テキスト入力欄の幅(大)
$txb_sze	= 10;		# テキスト入力欄の文字サイズ
$smw_wth	= 450;		# ポップアップウィンドウの幅
$smw_hgt	= 450;		# 高さ
$def_nb		= 12;		# 名字的長度上限（半形）
$def_ib		= 200;		# 自我介紹的長度上限（半形）
$def_om		= 25; 		# 履歷顯示筆數

# 以下不要更改
$get_remotehost = 0;		# ホストの取得方法（0 or 1）
$seacgi	= './sea.cgi';
$listcgi	= './list.cgi';
$newcgi	= './new.cgi';
$mailcgi	= './mail.cgi';
$eventdat	= './event.dat';
$man_img	= 'man.gif';
$wmn_img	= 'woman.gif';
$damgif	= 'dam.gif';	# 移動時，船的圖像
$seaimg	= 'sea.gif';	# 海圖像（背景）

1;