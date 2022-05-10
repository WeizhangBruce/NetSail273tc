#!/usr/bin/perl
# ↑サーバに合わせて変更

# #############################################################
# ネット航海時代(admin.cgi)
# Copyright (C) 2002 コスミー, All rights reserved.
# #############################################################
# 中文化版權宣告###############################################
# 網路航海時代管理系統(admin.cgi)
# 中文化改造：藍色小鼠BSM
# 改造討論區：http://www.2233.idv.tw/viewforum.php?f=115
# 改造項目：增加新的排序功能，時間排序以及船艦數排序，較方便管理
# #############################################################

# 以下設定
use Nfile;
$adcgi = './admin.cgi';
$bdcol = "#63300";
$def_am = 300;		# 管理用手紙の長さ(半角)
$capacity	= 100;		# 登録時の船長パラメータの合計
$def_fm		= 20000;	# 開始所持金

# 以下変更不要
%stay = ('1001' => '伊比利亞海域', '1002' => '北歐海域' , '1003' => '地中海海域' , '1004' => '非洲海域' , '1005' => '中近東海域' , '1006' => '印度海域' , '1007' => '東南亞海域' , '1008' => '亞洲海域' , '1009' => '美洲海域');

#require 'jcode.pl';
require 'setting.cgi';
require 'sys.cgi';

# 設定ここまで

# ###################################################################
&error("請於[setting.cgi]更改用戶目錄名") if $usrdir eq 'userdir';
&decode_l;
if (!$F{'mode'})      { &top_view }
else                  { &{$F{'mode'}} }
exit;
# ##################################################################

# Sub Top View #
sub top_view {
	&header;
print <<TOP;
	<center><H2><font color=#4169e1>$title管理室</font></H2>
	<form method=$method action=$adcgi>
	管理者密碼:<input type=password name=ps class=text size=$stx_wth>
	<input type=hidden name=mode value="admin">
	<input type=submit value="OK" class=button>
	</form></center>
TOP
	&footer;
}

# Sub Admin #
sub admin {
	&error("密碼錯誤") if $F{'ps'} ne $adps;
	&header;
	$on_clickh = qq|onClick="return opWin('?mode=ahistory&ps=$F{'ps'}','win6')"|;
print <<ADM;
	<center><H2><font color=#4169e1>$title管理室</font></H2>
	<form method=$method action=$adcgi><table><tr><td>
	<input type=radio name=mode value="del_view" checked>管理玩家帳戶<br>
	<input type=radio name=mode value="new_regist">管理員專用創立帳戶<br>
	<input type=radio name=mode value="amail_form">發送訊息<br>
	<a href="?mode=ahistory&ps=$F{'ps'}" $on_clickh target=_blank>訊息接收</a><br>
	<input type=hidden name=ps value="$F{'ps'}">
	<input type=submit value="OK">
	</td></tr></table></form></center>
ADM
	&footer;
}

# Sub Delete View #
sub del_view {
	&error("密碼錯誤") if $F{'ps'} ne $adps;
	&get_all_users;
	@alllines = map  { $_->[0] }
			sort { $a->[1] cmp $b->[1] || $a->[2] cmp $b->[2] }
			map  { [$_,(split(/<>/))[30,31]] } @alllines if $F{'sort'};
			if ($F{'sort'} ==2) {
				@alllines = map  { $_->[0] }
				sort { $b->[1] <=> $a->[1] }
				map  { $ships = (split(/<>/))[14]; [$_,$num = split(/△/,$ships)] } @alllines;
			}
			if ($F{'sort'} ==3) {
				@alllines = map  { $_->[0] }
				sort { $b->[1] <=> $a->[1] }
				map  { [$_,(split(/<>/))[24]] } @alllines;
			}
	&header;
	@checked = (0,0);
	$checked[$F{'sort'}] = ' checked';
print <<DEL;
	<center><H2><font color=#4169e1>$title室</font></H2>
	<table border=1 bordercolor=#000000 bgcolor=#e9e2ce cellspacing=0>
	<tr><td>刪除玩家帳戶資料。<br>
	<form method=$method action=$adcgi>
	<input type=radio name=sort value="0"$checked[0]>ID順 &nbsp;&nbsp;
	<input type=radio name=sort value="1"$checked[1]>IP順 &nbsp;&nbsp;
	<input type=radio name=sort value="2"$checked[2]>船數順 &nbsp;&nbsp;
	<input type=radio name=sort value="3"$checked[3]>時間順 &nbsp;&nbsp;
	<input type=hidden name=mode value="del_view">
	<input type=hidden name=ps value="$F{'ps'}">
	<input type=submit value="OK"></form></td></tr><tr><td>
	<form method=$method action=$adcgi><table>
	<tr><td>ID</td><td>名字</td><td>最後更新日期</td><td>信箱</td>
	<td>首頁</td><td>IP</td><td>OS</td><td>瀏覽器</td></tr>
DEL
	foreach (@alllines) {
		($id,$name,$last,$mail,$url,$host,$os,$bz) = (split(/<>/))[0,1,24,28,29,30,31,33];
		&get_date("$last");
		if ($mail) { $mail = "<a href=mailto:$mail>信箱</a>" }
		if ($url) { $url = "<a href=$url target=_blank>首頁</a>" }
	        $on_click = qq|onClick="return opWin('$listcgi?mode=uprofile&uid=$id','win6')"|;
		print qq|<tr>\n<td nowrap><input type=checkbox name="$id" value="on">$id</td>\n|;
		print qq|<td nowrap><a href="$listcgi?mode=uprofile&uid=$id&return=1" $on_click target=_blank>$name</a></td><td nowrap>$date</td><td nowrap>$mail</td>|;
		print qq|<td nowrap>$url</td><td nowrap>$host</td><td nowrap>$os</td>|;
		print qq|<td nowrap>$bz</td>\n</tr>\n|;
	}
print <<DWN;
	<tr><td colspan=8>
	<input type=hidden name=mode value="delete">
	<input type=hidden name=ps value="$F{'ps'}">
	<input type=hidden name=sort value="$F{'sort'}">
	<div align=right><input type=submit value="OK" class=button></div>
	</td></tr></table></form></td></tr></table><br>
	<a href="$adcgi?mode=admin&ps=$F{'ps'}">返回</a><br>
DWN
	&footer;
}

# Sub Delete #
sub delete {
	&error("密碼錯誤") if $F{'ps'} ne $adps;
	&get_all_users;
	foreach (@alllines) {
		$id = (split(/<>/))[0];
		if ($F{"$id"}) { unlink("$usrdir\/$id\.dat") }
	}
	$getallusersflag = 0;
	undef @alllines;
	&del_view;
}


# Sub New Regist #
sub new_regist {
	&error("密碼錯誤") if $F{'ps'} ne $adps;
	&header;
	&table('up',300);
	&label('新規登録');
	print qq|<a href="$adcgi?mode=admin&ps=$F{'ps'}">返回</a><br>\n|;

print <<NEW;
船長名字<br>
<input type=text name=nm class=text size=$stx_wth><br>
船長密碼<br>
<input type=password name=psb class=text size=$stx_wth><br>
電子郵件（可不填寫）<br>
<input type=text name=ml class=text size=$ltx_wth><br>
個人網頁（可不填寫）<br>
<input type=text name=ul class=text size=$ltx_wth><br>
性別
<img src="$img/$man_img"><input type=radio name=sx value="0" checked>
<img src="$img/$wmn_img"><input type=radio name=sx value="1">
<br>出發地點：
<select name="port">
<option value="1001△001">里斯本
<option value="1002△016">倫敦
<option value="1003△034">威尼斯
<option value="1004△051">聖喬治
</select>
<br>船長能力值（合計共$capacity）：<br>
戰鬥力<input type=text name=atk class=text size=5><br>
指揮力<input type=text name=cmd class=text size=5><br>
航海力<input type=text name=nav class=text size=5>
<input type=hidden name=mode value="set_regist">
<input type=hidden name=ps value="$F{'ps'}">
<input type=submit value="OK" class=button>
NEW
	&table('down');
	&footer;
}

# Sub Table #
sub table {
if($_[0] eq 'up') {
print <<TAB;
	<center><form method=$method action=$adcgi>
	<table width="$_[1]">
	<tr><td>
TAB
}
if($_[0] eq 'down') {
print <<TAB;
	</td></tr>
	</table></form>
	</center>
TAB
}
}

# Sub Set Regist #
sub set_regist {
	&error("密碼錯誤") if $F{'ps'} ne $adps;
	&error("[錯誤]名字尚未填寫。")	      if !$F{'nm'};
	&error("[錯誤]名字限定在半形$def_nb個文字以內。")	   if length $F{'nm'} > $def_nb;
	&error("[錯誤]名字內不得有空白字元「 」。") if $F{'nm'} =~ / / || $F{'nm'} =~ /　/;
	&error("[錯誤]名字內不得有半形冒號「:」。") if  $F{'nm'} =~ /:/;
	&error("[錯誤]名字內不得有三角「△」。")	  if  $F{'nm'} =~ /△/;
	&error("[錯誤]密碼尚未填寫。")	if !$F{'psb'};
	&error("[錯誤]電子郵件的格式錯誤。")	      if  $F{'ml'} && $F{'ml'} !~ /(.*)\@(.*)\.(.*)/;
	&error("[錯誤]船長能力點數的分配需合計$capacity點。")  if ($F{'atk'} + $F{'cmd'} + $F{'nav'}) != $capacity;
	&error("[錯誤]船長能力點數的分配不得為負數。") if ( ($F{'atk'} < 0) || ($F{'cmd'} < 0) || ($F{'nav'} < 0) );

	&get_all_users;

	($namecheck) = grep { $_->[0] eq $F{'nm'} }
	   	   	 map  { [(split(/<>/))[1]] } @alllines;
	($mailcheck) = grep { $_->[0] && $_->[0] eq $F{'ml'} }
	   	   	 map  { [(split(/<>/))[28]] } @alllines if $F{'ml'};
	($urlcheck)  = grep { $_->[0] && $_->[0] eq $F{'ul'} }
	   	   	 map  { [(split(/<>/))[29]] } @alllines if $F{'ul'};
	($idcheck)   = map  { $_->[0] }
	   	   	 sort { $b->[0] <=> $a->[0] }
	   	   	 map  { [(split(/<>/))[0]] } @alllines;

	$F{'ps'} =~ s/^$def_ei//;
	if ($namecheck) { &error("[錯誤]船長名字重複登記。") }
	if ($mailcheck) { &error("[錯誤]電子郵件重複登記。") }
	if ($urlcheck)  { &error("[錯誤]個人網頁重複登記。") }

	$id   = sprintf("%05d",$idcheck + 1);
	$name = $F{'nm'};
	$pass = &set_crypt($F{'psb'});
	$sex  = $F{'sx'};
	$mail = $F{'ml'};
	$url  = $F{'ul'};
	$atk  = $F{'atk'} ? $F{'atk'} : 0;
	$cmd  = $F{'cmd'} ? $F{'cmd'} : 0;
	$nav  = $F{'nav'} ? $F{'nav'} : 0;
	$host = 'Admin';
	$os   = 'Admin';
	$bz   = 'Admin';

	($area,$port) = split(/△/,$F{'port'});

	$money = $def_fm;
	$food = 0;
	$sailor = 0;
	$piracy = $trade = $adven = 0;
	$point = 1;
	$last = time - 86400;

	$Myfile = new Nfile("$usrdir\/$id\.dat",'new');
	&set_me;
	chmod(0666,"$usrdir\/$id\.dat");

	$F{'id'} = $id;

	&header;
	&table('up',300);
	&label('註冊完成');

	print qq|註冊完成<br>\n|;
	print qq|您的帳號：$id<br>\n|;
	print qq|您的密碼：$F{'psb'}<br><br>\n|;
	print qq|請牢記您的帳號與密碼。<br>若遺失恕不補發。\n|;

	print qq|<a href="$adcgi?mode=admin&ps=$F{'ps'}">返回</a>\n|;
	&table('down');
	&footer;
}

# Sub Set Cryptogram #
sub set_crypt {
	return $_[0] if !$def_cp;
	srand($$ | time);
	$xx = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		. "abcdefghijklmnopqrstuvwxyz"
		. "0123456789./";
	$salt  = substr($xx,int(rand(64)),1);
	$salt .= substr($xx,int(rand(64)),1);
	return $crypt = crypt($_[0],$salt);

}

# Sub Label #
sub label {
	print qq|<div align=center>\n|;
	print qq|$_[0]\n|;
	print qq|</div>\n|;
	print qq|<br>\n|;
}

# Sub Get Date #
sub get_date {
	($sec,$min,$hour,$day,$month,$year) = localtime($_[0]);
	$year += 1900;
	$month++;
	$date   = sprintf("%04d\/%02d\/%02d",$year,$month,$day);
}

# Sub Admin Mail Form #
sub amail_form {
	&error("密碼錯誤") if $F{'ps'} ne $adps;
	&get_all_users;
	@alllines = map  { $_->[0] }
		    sort { $a->[1] cmp $b->[1] || $a->[2] cmp $b->[2] }
		    map  { [$_,(split(/<>/))[30,31]] } @alllines if $F{'sort'};
	&header;
print <<MAIL;
	<center><H2><font color=#4169e1>$title管理室・訊息發送</font></H2>
	<table border=1 bordercolor=#000000 bgcolor=#e9e2ce cellspacing=0>
	<tr><td>【管理員信件發信系統】<br>
	可以將信件同時發給多數人。<br>
	如果發送數量過多，容易導致伺服器負荷不了，請特別注意。<br><br>
MAIL
	if ($#sended >= 0) {
		foreach(@sended) {
			print qq|$_<br>\n|
		}
		print qq|送出訊息給以上玩家。|
	}
	@checked = (0,0);
	$checked[$F{'sort'}] = ' checked';
print <<MAILD;
	<form method=$method action=$adcgi>
	<input type=radio name=sort value="0"$checked[0]>ID順 &nbsp;&nbsp;
	<input type=radio name=sort value="1"$checked[1]>IP順 &nbsp;&nbsp;
	<input type=hidden name=mode value="amail_form">
	<input type=hidden name=ps value="$F{'ps'}">
	<input type=submit value="OK"></form></td></tr><tr><td>
	<form method=$method action=$adcgi><table>
	<tr><td>ID</td><td>名字</td><td>最後更新日期</td><td>信箱</td>
	<td>首頁</td><td>IP</td><td>OS</td><td>瀏覽器</td></tr>
MAILD
	foreach (0 .. $#alllines) {
		($id,$name,$last,$mail,$url,$host,$os,$bz) = (split(/<>/,$alllines[$_]))[0,1,24,28,29,30,31,33];
		&get_date("$last");
		if ($mail) { $mail = "<a href=mailto:$mail>信箱</a>" }
		if ($url) { $url = "<a href=$url target=_blank>首頁</a>" }
	        $on_click = qq|onClick="return opWin('$listcgi?mode=uprofile&uid=$id','win6')"|;
		print qq|<tr>\n<td nowrap><input type=checkbox name="$_" value="$id">$id</td>\n|;
		print qq|<td nowrap><a href="$listcgi?mode=uprofile&uid=$id&return=1" $on_click target=_blank>$name</a></td><td nowrap>$date</td><td nowrap>$mail</td>|;
		print qq|<td nowrap>$url</td><td nowrap>$host</td><td nowrap>$os</td>|;
		print qq|<td nowrap>$bz</td>\n</tr>\n|;
	}
print <<MDWN;
	<tr><td colspan=8>
	<hr class=text>
	<textarea name=message cols=30 rows=5 class=text></textarea><br>
	<input type=hidden name=mode value="asend_mail">
	<input type=hidden name=anum value="$#alllines">
	<input type=hidden name=ps value="$F{'ps'}">
	<input type=hidden name=sort value="$F{'sort'}">
	<div align=right><input type=submit value="OK" class=button></div>
	</td></tr></table></form></td></tr></table><br>
	<a href="$adcgi?mode=admin&ps=$F{'ps'}">返回</a><br>
MDWN
	&footer;
}

# Sub Admin Send Mail #
sub asend_mail {
	&error("密碼錯誤") if $F{'ps'} ne $adps;
	&error("信箱の長さは半角$def_am文字まで") if length $F{'message'} > $def_am;
	&error("信箱内容が未入力です") if !$F{'message'};
	$F{'message'} =~ s/<br>//g;
	for (0 .. $F{'anum'}){
		if ($F{$_}) {
			if (@sended >= 5) {
				push(@sended ,"\<font color\=\'#FF0000\'\>一度に多く送りすぎです！上記以外は中止しました。\<\/font\>");
				last
			}
			&get_u($F{$_});
			if ($dead) { next }
			else {
				&add_record("管理者：「$F{'message'}」",1);
				$urecord  .= "管理者的訊息送達<br>";
				&set_u
			}
			push(@sended ,$uname)
		}
	}
	&amail_form
}

# Sub Admin History #
sub ahistory {
	&error("密碼錯誤") if $F{'ps'} ne $adps;
	my $AdminMail = new Nfile("$datadir/admin.dat",'read');
	@mailline = $AdminMail->read;
	&header;
	print qq|<table width="95%" border=1 bordercolor=#000000 bgcolor=#e9e2ce cellspacing=0><tr><td align=center>手紙</td></tr><tr><td>\n|;
	foreach (@mailline) { print "$_<br>\n" }
	print qq|</td></tr></table>\n</body>\n</html>\n|;
}

# Sub Add Record #
sub add_record {
	&get_date(time) if !$date;
	if ($_[1] && $_[0]) {
	    $words =  "[$date] $_[0]\n";
	    pop (@ulines) if @ulines >= $def_om;
	    unshift (@ulines,$words);
	}
	elsif ($_[0]) {
	    $words =  "[$date] $_[0]\n";
	    pop (@ilines) if @ilines >= $def_om;
	    unshift (@ilines,$words);
	}
}

# Sub Header #
sub header {
print <<HEAD;
Content-type: text/html

<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>$title</title>
<SCRIPT LANGUAGE="JavaScript">
<!--
	var w = window;
	function opWin(url,wname){
	if ((w == window) || w.closed) {
		w = open(url,wname,"scrollbars=yes,resizable=yes,width=$smw_wth,height=$smw_hgt");
	} else {
		w.location.replace(url);
		w.focus();
	}
	return(false);
	}
//-->
</SCRIPT>
</head>$body
HEAD
	$headflag = 1;
}

# Sub Footer #
sub footer {
	if ($_[0]) {
		print qq|<br>\n</body>\n</html>\n|;
	}
	else {
        # 著作権表示。絶対に消さないで下さい！
        # ここにリンクを貼る場合、・・・・と同じ行にせず、
        # 必ず改行を行って別行にしてください。
        # 改造者のリンクを貼る場合、改造者の前に必ず「Edit:」をつけること。
	print qq|<br><center>ネット航海時代 Ver $ver<br>\n|;
	print qq|<a href="http://red-treasure.com/NetCastle/" target="_blank" title="ネット航海時代・配布元">Net Castle</a>|;
	print qq|</font></center>\n</body>\n</html>\n|;
	}
}

# Sub Error #
sub error {
	&unlock if $locked;
	if (!$headflag) { &header }
print <<ERR;
<center>
<hr width=80%>
<B><font color=#FF0000>$_[0]</font></B>
<hr width=80%>
</center>
ERR
	&return_button if !$def_rb;
	&footer('no');
	exit;
}

# Sub Decode #
sub decode_l {
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
		@pairs = split(/&/, $buffer);
	} else { @pairs = split(/&/, $ENV{'QUERY_STRING'}); }
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$name =~ tr/+/ /;
		$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

#		&jcode'convert(*name,'sjis');
#		&jcode'convert(*value,'sjis');

		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
		$value =~ s/\,/，/g;
		$value =~ s/\r\n/<br>/g;
		$value =~ s/\r/<br>/g;
		$value =~ s/\n/<br>/g;

		$F{$name} = $value;
	}
}
