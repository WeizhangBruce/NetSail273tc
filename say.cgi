#!/usr/bin/perl

# 製作者情報（嚴禁消除！）
# ize-Say version1.0
# http://www.ize-design.com/visualize/
# miyase@ize-design.com
# Copylight (c) VISUALIZE

# 中文化修改：藍色小鼠BSM
# http://www.2233.idv.tw/viewforum.php?f=115
# netsailbybsm@gmail.com

require './cgi-lib.pl';

############# 初期設定 #############
$cnt = "20";			#表示的文件數量
$bgcolor = "#eacd9f";	#背景顏色
$text = "#000000";		#文字顏色
$hr = "#000000";		#水平線顏色
$face = "#eacd9f";		#捲軸條棒顏色
$track = "#000000";		#捲軸的背景色
$arrow = "#eacd9f";		#捲軸的箭頭顏色

########## 格式設定 ##########

$log = "log.dat";

print "Content-type: text/html\n\n";

%form = &read_input('euc');
$name = $form{'edn'};
$comment = $form{'edc'};


if ( $ENV{'REQUEST_METHOD'} eq "POST" && $name ne "" && $comment ne "" ){

# 使用者文字格式宣告
$name =~ s/\&/\&amp;/g;		#←若刪除則可正常顯示日文等非繁體中文之文字
$name =~ s/\</\&lt;/g;		#html語法防止
$name =~ s/\>/\&gt;/g;		#html語法防止

$comment =~ s/\&/\&amp;/g;	#←若刪除則可正常顯示日文等非繁體中文之文字
$comment =~ s/\</\&lt;/g;	#html語法防止
$comment =~ s/\>/\&gt;/g;	#html語法防止

# 改行制御
$comment =~ s/\r\n/\n/g; # Windows系(CR,LF)->LF
$comment =~ s/\r/\n/g;   # Mac 系(CR)->LF
$comment =~ s/\n/<BR>/g; # LF -> <BR>


# 發言格式
if( $name ne "" && $comment ne "" ){
	@new = ("<font color=\"#000000\">${name}</font>：$comment</font> <HR SIZE=\"1\" COLOR=\"$hr\">\n");
}

}# POST確認終了
#######################################

	

if ( !open (LF, "$log") ){
print "　　\n";
}
else{
@old = <LF>;
close(LF);
}

if ( @new > 0 ){
if ( !open (LF, ">$log") ){
print "<HR>發送訊息失敗<HR>\n";
}
else{
@wrt_keiji = (@new,@old); 
$wrt_cnt = 0;
foreach $wrt_rec (@wrt_keiji){
print LF $wrt_rec;
$wrt_cnt++;
if( $wrt_cnt >= $cnt ){
last;
}
}
close (LF);
}
}

print <<"EOF";
<HTML>
<HEAD>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=utf-8">
<TITLE>聊天室</TITLE>
<STYLE type="text/css"><!--
BODY{font-family:verdana,Arial;font-size:12px;scrollbar-face-color:$face;scrollbar-highlight-color:$track;scrollbar-shadow-color:$track;scrollbar-3dlight-color:$face;scrollbar-arrow-color:$arrow;scrollbar-track-color:$track;scrollbar-darkshadow-color:$face;}
A{color:$link;text-decoration:none;}
A:hover,A:active{color:$hover;}
.input{color:$t_font;font-size:12px;background-color:$t_bgcolor;border-left:1px solid $t_line;border-right:1px solid $t_line;border-top:1px solid $t_line;border-bottom:1px solid $t_line;}
textarea{color:$t_font;font-size:12px;background-color:$t_bgcolor;border-left:1px solid $t_line;border-right:1px solid $t_line;border-top:1px solid $t_line;border-bottom:1px solid $t_line;}
TABLE,TD{font-size:12px;}
.m{margin: 5px 20px 20px;}
.m1{margin: 5px 20px 20px;}
.m2{margin: 0px 0px 5px;}
--></STYLE>
</HEAD>
<BODY BGCOLOR="$bgcolor" TEXT="$text">
<DIV ALIGN="CENTER">
<TABLE WIDTH="100%" BORDER="0" CELLPADDING="0" CELLSPACING="0">
<TR><TD ALIGN="LEFT">
<HR SIZE="1" COLOR="$hr">
@new
@old
</TD></TR></TABLE><BR>
<!-- 以下嚴禁消除 -->
-+- <A HREF="http://www.ize-design.com/visualize/" TARGET="_blank"><font color=#ffffff>VISUALIZE</font></A> -+-<br>
~ <A HREF="http://www.2233.idv.tw/viewforum.php?f=115" TARGET="_blank"><font color=#ffffff>改造by BSM</font></A> ~
</DIV></BODY>
</HTML>
EOF
__END__