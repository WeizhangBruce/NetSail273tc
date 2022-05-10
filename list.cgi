#!/usr/bin/perl
# ↑サーバに合わせて変更

# #############################################################
# ネット航海時代(list.cgi)
# Copyright (C) 2002 コスミー, All rights reserved.
# #############################################################

# 以下設定
use Nfile;
$def_ml		= 300;		# メールの長さ
$def_pj		= 50;		# 一ページに表示する數

# 以下変更不要
%stay = ('1001' => '伊比利亞海域', '1002' => '北歐海域' , '1003' => '地中海海域' , '1004' => '非洲海域' , '1005' => '中近東海域' , '1006' => '印度海域' , '1007' => '東南亞海域' , '1008' => '亞洲海域' , '1009' => '美洲海域');

#require 'jcode.pl';
require 'setting.cgi';
require 'sys.cgi';
$mel_img = qq|<img src="$img/mail.gif" border=0>|;
$url_img = qq|<img src="$img/url.gif" border=0>|;
# 設定ここまで

# ###################################################################
&error("請於[setting.cgi]更改用戶目錄名") if $usrdir eq 'userdir';
&decode_l;
if ($F{'id'} =~ /\W/) { &error('[系統訊息]不正當的執行'); }
if (!$F{'mode'})      { &error('[系統訊息]不正當的呼叫');     }
else                  { require "$mailcgi" if $F{'mode'} =~ /mail/;
			require 'intro.cgi' if ($F{'mode'} eq 'introduce') || ($F{'mode'} eq 'set_introduce');
			&{$F{'mode'}}   }
exit;
# ##################################################################

# Sub History #
sub history {
	&header;
	&get_me($F{'id'},'read');
	&title;
	&table('up','95%','1');
	&label('履歷');
	foreach (@ilines) { print "$_<br>\n" }
	&table('down');
	print qq|<br>\n</body>\n</html>\n|;
}

# Sub Event Look #
sub event_look {
	my $EventFile = new Nfile($eventdat,'read');
	my @eventline = $EventFile->read;
	&header;
	&title;
	&table('up','95%','1');
	&label('事件');
	foreach (@eventline) { print "$_<br>\n" }
	&table('down');
	print qq|<br>\n</body>\n</html>\n|;
}

# Sub Header #
sub header {
print <<HEAD;
Content-type: text/html

<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Content-Style-Type" content="text/css">
<title>$title</title>
</head>$body
HEAD
	$headflag = 1;
}

# Sub Label #
sub label {
	print qq|<div align=center>\n|;
	print qq|$_[0]\n|;
	print qq|</div>\n|;
	print qq|<br>\n|;
}


# Sub Player List #
sub player_list {
	&header;
	&title;
	&table('up','95%',1);

	print qq|<a href=$listcgi?mode=player_list&sort=0>[ID]</a>\n|;
	print qq|<a href=$listcgi?mode=player_list&sort=1>[名字]</a>\n|;
	print qq|<a href=$listcgi?mode=player_list&sort=4>[資金]</a>\n|;
	print qq|<a href=$listcgi?mode=player_list&sort=8>[冒險]</a>\n|;
	print qq|<a href=$listcgi?mode=player_list&sort=9>[海賊]</a>\n|;
	print qq|<a href=$listcgi?mode=player_list&sort=10>[商人]</a><br>\n|;
	print qq|<a href=$listcgi?mode=player_list&sort=14>[所持船數]</a>\n|;
	print qq|<a href=$listcgi?mode=player_list&sort=15>[海域]</a><br>\n|;
	&get_all_users;
	$st = $F{'sort'};
	if ($st != 0 && $st != 1 && $st != 4 && $st != 8 && $st != 9 && $st != 10 && $st != 14 && $st != 15) {
		$st = 0;
	}
	$lbl = $st ==  8 ? '冒險名聲' :
		 $st ==  9 ? '海賊名聲' :
		 $st == 10 ? '商人名聲' :
		 $st == 14 ? '所持船數' :
		 $st == 15 ? '海域'	:
				 '艦隊一覽';

	if	($st == 0 || $st == 15) {
		@alllines = map  { $_->[0] }
				sort { $a->[1] <=> $b->[1] }
				map  { [$_,(split(/<>/))[$st]] } @alllines;
	}
	elsif ($st == 1) {
		@alllines = map  { $_->[0] }
				sort { $a->[1] cmp $b->[1] }
				map  { [$_,(split(/<>/))[$st]] } @alllines;
	}
	elsif ($st == 14) {
		@alllines = map  { $_->[0] }
				sort { $b->[1] <=> $a->[1] }
				map  { $ships = (split(/<>/))[$st]; [$_,$num = split(/△/,$ships)] } @alllines;
	}
	else {
		@alllines = map  { $_->[0] }
				sort { $b->[1] <=> $a->[1] }
				map  { [$_,(split(/<>/))[$st]] } @alllines;
	}

	&page($F{'pg'},$#alllines,$def_pj);
	print qq|<b><a href=$listcgi?mode=player_list&pg=$back&sort=$st>[前]</a></b>| if $back >= 0;
	print qq|<b><a href=$listcgi?mode=player_list&pg=$next&sort=$st>[次]</a></b>| if $end != $total;

	for ($i=0; $i <= $#alllines; $i += $def_pj) {
		$pge_nm = $i / $def_pj + 1;
		$tag = $i == $F{'pg'} ? "[$pge_nm]" : "<a href=$listcgi?mode=player_list&pg=$i&sort=$st>[$pge_nm]</a>";
		print qq|<b>$tag</b>|;
	}

	print qq|<br><br>\n|;
	&label($lbl);

	print qq|<table align=center width=100%>\n|;
	foreach ($start .. $end) {
		($uid,$uname,$usex,$umoney,$uarea,$xx) = 
		(split(/<>/,$alllines[$_]))[0,1,3,4,15,$st];
		$sex_img = $usex ? 'woman.gif' : 'man.gif';
		print qq|<tr>\n|;
		print qq|<td><a href=$listcgi?mode=uprofile&uid=$uid&return=1>$uname</a></td>\n|;
		print qq|<td><img src="$img/$sex_img"></td>\n|;
		print qq|<td>$stay{"$uarea"}</td>\n|;
		if ($st == 8 || $st == 9 || $st == 10) { $lbl = "$xx pt" }
		elsif ($st == 10)	{ $lbl = "$xx G"  }
		elsif ($st == 14) { $xx = split(/△/,$xx); $lbl = "$xx 艦隊" }
		else	{ $lbl = "$umoney G"  }
		print qq|<td align=right nowrap>$lbl</td>\n|;
		print qq|</tr>\n|;
	}
	print qq|</table>\n|;
	&table('down');
	print qq|<br>\n</body>\n</html>\n|;
}

# Sub U Profile #
sub uprofile {
	&get_u($F{'uid'},'read');
	if ($umail) { $umail = "<a href=mailto:$umail>$mel_img</a>" }
	if ($uurl) { $uurl = "<a href=$uurl target=_blank>$url_img</a>" }
	$ship_total = @uship_ind;
	my($i) = 0;
	foreach (@uship_ind) {
		@{$uship[$i]} = split(/,/,$_);
		$i++;
	}
	&header;
	&title;
	&table('up','90%',1);
	($item_detail = $uitem_line) =~ s/,/　/g;
print <<PROF;
<table border=0 cellspacing=0 cellpadding=1 width=100%>
<tr><td>名字：$uname $umail $uurl</td></tr>
<tr><td>艦隊數：$ship_total</td><td>資金：$umoney G</td></tr>
</table><table border=0 cellspacing=0 cellpadding=1 width=100%>
<tr><td>
<br>
冒險名聲：$uadven<br>
海賊名聲：$upiracy<br>
商人名聲：$utrade<br><br>
財寶：<br>$item_detail<br><br>
現在海域：$stay{"$uarea"}</td><td align=right>
PROF
	&uships;
	print qq|</td></tr></table><br>\n|;
	print qq|<hr class=text>\n| if $uintro;
	print qq|<b>$uintro</b>\n| if $uintro;
	print qq|<br><br>\n|;
	&return_button("player_list",'','button') if $F{'return'};
	&table('down');
	print qq|<br>\n</body>\n</html>\n|;
}

# Sub U Ships #
sub uships {
	for ($i=0; $i <= 16; $i++){
		if(!$uship[$i][0]){ $uship[$i][0] = $damgif; }
	}
print <<SHIP_TABLE;
<table border=0 cellspacing=0 cellpadding=0 background="$img/$seaimg">
<tr>
<td height=20 width=20 align=center valign=center><br></td>
<td height=20 width=20 align=center valign=center><br></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[11][0]" alt="$uship[11][4]" width=20></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[15][0]" alt="$uship[15][4]" width=20></td>
<td height=20 width=20 align=center valign=center><br></td>
</tr>
<tr>
<td height=20 width=20 align=center valign=center><br></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[9][0]" alt="$uship[9][4]" width=20></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[3][0]" alt="$uship[3][4]" width=20></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[7][0]" alt="$uship[7][4]" width=20></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[13][0]" alt="$uship[13][4]" width=20></td>
</tr>
<tr>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[6][0]" alt="$uship[6][4]" width=20></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[2][0]" alt="$uship[2][4]" width=20></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[0][0]" alt="$uship[0][4]" width=20></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[1][0]" alt="$uship[1][4]" width=20></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[5][0]" alt="$uship[5][4]" width=20></td>
</tr>
<tr>
<td height=20 width=20 align=center valign=center><br></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[10][0]" alt="$uship[10][4]" width=20></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[4][0]" alt="$uship[4][4]" width=20></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[8][0]" alt="$uship[8][4]" width=20></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[14][0]" alt="$uship[14][4]" width=20></td>
</tr>
<tr>
<td height=20 width=20 align=center valign=center><br></td>
<td height=20 width=20 align=center valign=center><br></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[12][0]" alt="$uship[12][4]" width=20></td>
<td height=20 width=20 align=center valign=center><img src="$img/$uship[16][0]" alt="$uship[16][4]" width=20></td>
<td height=20 width=20 align=center valign=center><br></td>
</tr>
</table>
SHIP_TABLE
}


# Sub ID List #
sub id_list {
	&header;
	&title;
	&get_all_users;
	print qq|<table border=1 width="100%" bgcolor=$t_bgcol bordercolor=$bdcol cellspacing=0>\n|;
	foreach (@alllines) {
		($id,$name,$sex) = (split(/<>/))[0,1,3];
		$sex_img = $sex ? 'woman.gif' : 'man.gif';
		print qq|<tr><td>$id</td><td><img src="$img/$sex_img"></td><td>$name</td></tr>\n|;
	}
	print qq|</table>|;
	print qq|<br>\n</body>\n</html>\n|;
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

# Sub Return Button #
sub return_button {
	$type = $_[2];
	$type = 'link' if $def_rb;
	print qq|<a href=$listcgi?mode=$_[0]>$bak_lbl</a><br>\n| if $type eq 'link';
	print qq|<div align=center><input type=button value="$bak_lbl" onClick="history.back()" class=button></div>| if $type eq 'button';
	print qq|<br>\n| if $_[1] eq 'br';
}

# Sub Page #
sub page {
	($first,$total,$eachpage) = @_;
	$start = $first eq '' ? 0 : $first;
	$end   = $start + ($eachpage - 1);
	$end   = $total if $end >= $total;
	$next  = $end + 1;
	$back  = $start - $eachpage;
}

# Sub Title #
sub title {
	print qq|<center><H2><font color=#4169e1>$title</font></H2><br></center>\n|;
}

# Sub Table #
sub table {
if($_[0] eq 'up') {
print <<TAB;
	<center>
	<table border=$_[2] width="$_[1]" bgcolor=$t_bgcol bordercolor=$bdcol cellspacing=0>
	<tr><td>
TAB
}
if($_[0] eq 'down') {
print <<TAB;
	</td></tr>
	</table>
	</center>
TAB
}
}