#!/usr/bin/perl
# ↑サーバに合わせて変更

# #############################################################
# ネット航海時代(new.cgi)
# Copyright (C) 2002 コスミー, All rights reserved.
# #############################################################

# 以下設定

$def_mp		= 200;		# 人數限制(推薦200人以下)
$def_fm		= 20000;	# 遊戲開始的所持金
$capacity	= 100;		# 登錄時船長能力值合計

use Nfile;
#require 'jcode.pl';
require 'setting.cgi';
require 'sys.cgi';
# 設定ここまで

#########################################################
&decode;
if (!$F{'mode'})                { &new_regist     }
else                            { &{$F{'mode'}}   }
exit;
#########################################################

# Sub New Regist #
sub new_regist {
	&dead_check;
	&restrict;
	&header;
	&title;
	&return_button('','br','link');
	&table('up',300);
	&label('創立帳戶');


print <<NEW;
船長名字<br>
<input type=text name=nm class=text size=$stx_wth><br>
船長密碼<br>
<input type=password name=ps class=text size=$stx_wth><br>
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
NEW
	&submit_button;
	&table('down');
	&home_button;
	&footer;
}

# Sub Return Button #
sub return_button {
    $type = $_[2];
    $type = 'link' if $def_rb;
    print qq|<a href="$seacgi">$bak_lbl</a><br>\n| if $type eq 'link';
    print qq|<div align=center><input type=button value="$bak_lbl" onClick="history.back()" class=button></div>| if $type eq 'button';
    print qq|<br>\n| if $_[1] eq 'br';
}

# Sub Dead Check #
sub dead_check {
	&get_all_users;
	$now = time;
	foreach (@alllines) {
		($aid,$alast)  = (split(/<>/))[0,24];
		$passed = int(($now - $alast) / (1 * 60 * 60 * 24));
		if ($passed > $def_dead) { unlink("$usrdir/$aid\.dat") }
	}
}

# Sub Restriction #
sub restrict {
	opendir (DIR, "$usrdir") || die "無法開啟用戶目錄\n";
	@usrfiles = readdir (DIR);
	closedir (DIR);
	&reg_cookie;
	if ($c_check ne 'check' && $def_ip == 1) { &error("瀏覽器無法與Cookie對應，或是有不是來自遊戲首頁進入的可能性。<br>請使用可與Cookie對應之瀏覽器由遊戲首頁進入。"); }
	if( ($def_mp && (@usrfiles - 2) >= $def_mp) || ($def_ip && $c_id)) { &error("因特殊情況限制登錄新玩家。<br>可能性 1：Cookie已存在。<br>可能性 2：人數已滿。") }
}

# Sub Submit Button #
sub submit_button {
	print qq|<input type=submit value="OK" class=button>\n|;
}

# Sub Table #
sub table {
if($_[0] eq 'up') {
print <<TAB;
	<center><form method=$method action=$newcgi>
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

# Sub Label #
sub label {
	print qq|<div align=center>\n|;
	print qq|$_[0]\n|;
	print qq|</div>\n|;
	print qq|<br>\n|;
}

# Sub Set Regist #
	sub set_regist {
	&error("[錯誤]名字尚未填寫。")	      if !$F{'nm'};
	&error("[錯誤]名字限定在半形$def_nb個文字以內。")	   if length $F{'nm'} > $def_nb;
	&error("[錯誤]名字內不得有空白字元「 」。") if $F{'nm'} =~ / / || $F{'nm'} =~ /　/;
	&error("[錯誤]名字內不得有半形冒號「:」。") if  $F{'nm'} =~ /:/;
	&error("[錯誤]名字內不得有三角「△」。")	  if  $F{'nm'} =~ /△/;
	&error("[錯誤]名字內含有不合法的字元。") if  $F{'nm'} =~ /([.,:;\t\r\n<>&])/;	#追加
	&error("[錯誤]密碼尚未填寫。")	if !$F{'ps'};
	&error("[錯誤]電子郵件的格式錯誤。")	      if  $F{'ml'} && $F{'ml'} !~ /(.*)\@(.*)\.(.*)/;
	&error("[錯誤]船長能力點數的分配需合計$capacity點。")  if ($F{'atk'} + $F{'cmd'} + $F{'nav'}) != $capacity;
	&error("[錯誤]船長能力點數的分配不得為負數。") if ( ($F{'atk'} < 0) || ($F{'cmd'} < 0) || ($F{'nav'} < 0) );

	&get_all_users;
	$def_mp && @alllines >= $def_mp && &error("[系統]登錄達到 $def_mp 人，停止創立新帳戶。");
	&get_host;
	&get_agent;

	($namecheck) = grep { $_->[0] eq $F{'nm'} }
	   	   	 map  { [(split(/<>/))[1]] } @alllines;
	($mailcheck) = grep { $_->[0] && $_->[0] eq $F{'ml'} }
	   	   	 map  { [(split(/<>/))[28]] } @alllines if $F{'ml'};
	($urlcheck)  = grep { $_->[0] && $_->[0] eq $F{'ul'} }
	   	   	 map  { [(split(/<>/))[29]] } @alllines if $F{'ul'};
	($ipcheck)   = grep { &ip_check($host,$_->[0]) && ($os eq $_->[1]) && ($bz eq $_->[2]) }
	   	   	   map  { [(split(/<>/))[30,31,33]] } @alllines if $def_ip;
	($idcheck)   = map  { $_->[0] }
	   	   	 sort { $b->[0] <=> $a->[0] }
	   	   	 map  { [(split(/<>/))[0]] } @alllines;

	if ($F{'ps'} =~ s/^$def_ei//) { undef $ipcheck }
	if ($namecheck) { &error("[錯誤]船長名字重複登記。") }
	if ($mailcheck) { &error("[錯誤]電子郵件重複登記。") }
	if ($urlcheck)  { &error("[錯誤]個人網頁重複登記。") }
	if ($ipcheck)   { &error("[錯誤]ＩＰ重複登記。") }

	$id   = sprintf("%05d",$idcheck + 1);
	$name = $F{'nm'};
	$pass = &set_crypt($F{'ps'});
	$sex  = $F{'sx'};
	$mail = $F{'ml'};
	$url  = $F{'ul'};
	$atk  = $F{'atk'} ? $F{'atk'} : 0;
	$cmd  = $F{'cmd'} ? $F{'cmd'} : 0;
	$nav  = $F{'nav'} ? $F{'nav'} : 0;
	($area,$port) = split(/△/,$F{'port'});

	$money = $def_fm;
	$food = 0;
	$sailor = 0;
	$piracy = $trade = $adven = 0;
	$point = 1;
	$last = time - 86400;

	$Myfile = new Nfile("$usrdir/$id.dat",'new');
	&set_me;
	eval {
		chmod(0666,"$usrdir/$id.dat");
	};

	$F{'id'} = $id;

	&set_cookie;
	&header;
	&table('up',300);
	&title;
	&label('註冊完成');

	print qq|註冊完成<br>\n|;
	print qq|您的帳號：$id<br>\n|;
	print qq|您的密碼：$F{'ps'}<br><br>\n|;
	print qq|請牢記您的帳號與密碼。<br>若遺失恕不補發。\n|;

	print qq|<a href="$seacgi">回首頁</a>\n|;
	&table('down');
	&home_button;
	&footer;
}

# Sub IP Check #
sub ip_check {
    $X = $_[0]; $Y = $_[1];
    $X =~ s/(\d+)\.(\d+)\.(\d+)\.(\d+)/$1\.$2\.$3\./;
    $Y =~ s/(\d+)\.(\d+)\.(\d+)\.(\d+)/$1\.$2\.$3\./;
    if ($X eq $Y) { return 1 } else { return 0 }
}

# Sub Title #
sub title {
	print qq|<center><H2><font size=5 color=#4169e1>$title</font></H2><br></center>\n|;
}

# Sub Home Button #
sub home_button {
    if (!$def_ho) { return }
    print qq|<br><center>|;
    print qq|<a href=$hom_url target=$hom_tgt>$hom_lbl</a><br>\n|;
    print qq|</center>\n|;
}

# Sub Header #
sub header {
print <<HEAD;
Content-type: text/html

<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>$title</title>
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

# Sub Error #
sub error {
	$_[1] || &unlock;
	if (!$headflag) { &header }
	print qq|<center>\n|;
	print qq|<hr width=80%>\n|;
	print qq|<B><font color=#FF0000>$_[0]</font></B>\n|;
	print qq|<hr width=80%>\n|;
	print qq|</center>\n|;
	&return_button('','','button') if !$def_rb;
	&footer;
	exit;
}

# Sub Decode #
sub decode {
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
		@pairs = split(/&/, $buffer);
	} else {
		@pairs = split(/&/, $ENV{'QUERY_STRING'});
		if($#pairs >= 0 && $method eq 'POST') { &error("不正なエラーです"); }
	}

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

# Sub Regist Cookie #
sub reg_cookie {
	@pairs = split(/\;/,$ENV{'HTTP_COOKIE'});
	foreach $pair (@pairs) {
		my($name, $value) = split(/\=/, $pair);
		$name =~ s/ //g;
		$DUMMY{$name} = $value;
	}
	@pairs = split(/\,/,$DUMMY{$cookname});
	foreach $pair (@pairs) {
		my($name, $value) = split(/\:/, $pair);
		$COOKIE{$name} = $value;
	}
	$c_id = $COOKIE{'id'};
	$c_ps = $COOKIE{'ps'};
	$c_check = $DUMMY{"T$cookname"};
}

# Sub Get Host #
sub get_host {
	$host = $ENV{'REMOTE_HOST'};
	$ad = $ENV{'REMOTE_ADDR'};
	if ($get_remotehost) {
		if ($host eq "" || $host eq "$ad") {
			$host = gethostbyaddr(pack("C4",split(/\./,$ad)),2);
		}
	}
	if ($host eq "") { $host = $ad }
}

# Sub Get Agent #
sub get_agent {
	$bz = $os = $ENV{'HTTP_USER_AGENT'};

	$_ = $bz;
	$bz = /MSIE 3/i		 ? 'MSIE 3':
		  /MSIE 4/i		 ? 'MSIE 4':
		  /MSIE 5/i		 ? 'MSIE 5':
		  /MSIE 6/i		 ? 'MSIE 6':
		  /MSIE 7/i		 ? 'MSIE 7':
		  /MSIE 8/i		 ? 'MSIE 8':
		  /Mozilla\/2/i	 ? 'Netscape 2':
		  /Mozilla\/3/i	 ? 'Netscape 3':
		  /Mozilla\/4/i	 ? 'Netscape 4':
		  /Mozilla\/5/i	 ? 'Netscape 5':
		  /Netscape ?6/i	? 'Netscape 6':
		  /Netscape ?7/i	? 'Netscape 7':
		  /Netscape ?8/i	? 'Netscape 8':
		  /AOL/			 ? 'AOL':
		  /Opera/i		  ? 'Opera':
		  /Lynx/i		   ? 'Lynx':
		  /Cuam/i		   ? 'Cuam':
		  /DoCoMo/i		 ? 'i-mode':
		  /J-PHONE/i		? 'J-Skyweb':
		  /Internet Ninja/i ? 'Internet Ninja':
							  'Unknown Browser';
	$_ = $os;
	$os = /Windows 95/i	   || /Win95/i	  ? 'Win95':
		  /Windows 9x/i	   || /Win 9x/i	  ? 'WinMe':
		  /Windows 98/i	   || /Win98/i	  ? 'Win98':
		  /Windows XP/i	   || /WinXP/i	  ? 'WinXP':
		  /Windows NT 5\.1/i || /WinNT 5\.1/i ? 'WinXP':
		  /Windows NT 5/i	   || /WinNT 5/i	  ? 'Win2000':
		  /Windows 2000/i	   || /Win2000/i	  ? 'Win2000':
		  /Windows NT/i	   || /WinNT/i	  ? 'WinNT':
		  /Windows CE/i	   || /WinCE/i	  ? 'WinCE':
		  /Mac/i					  ? 'Mac':
		  /sharp pda browser/i			  ? 'ZAURUS':
		  /X/			   ||
		  /Sun/i		   ||
		  /Linux/i		   ||
		  /HP-UX/i		   ||
		  /OSF1/i		   ||
		  /IRIX/i		   ||
		  /BSD/i					  ? 'UNIX':
								    'Unknown Os';
}
