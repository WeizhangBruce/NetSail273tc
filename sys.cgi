# Sub Get Me #
sub get_me {
	return if $getmeflag;

	my $save = $_[1] ? 'read' : 'save';
	$Myfile = new Nfile("$usrdir\/$_[0]\.dat",$save);
	@ilines = $Myfile->read;
	if (!@ilines) { &error("ID $_[0] 讀取錯誤"); }
	if ($ilines[0] eq "Read Error") { &error("ID不存在"); }
	my $userline = shift(@ilines);
	($id,$name,$pass,$sex,$money,$atk,$cmd,$nav,$adven,$piracy,$trade,$food,$sailor,$load,$ship_line,
	 $area,$port,$point,$tactics,$record,$quest_flag,$quest_line,$friend_line,$battle_line,
	 $last,$moved,$end_quest,$intro,$mail,$url,$host,$os,$ip,$bz,$action,$item_line,$city_line,$reserv,$aexp,$pexp,$texp) = split(/<>/,$userline);
	@ship_ind = split(/△/,$ship_line);
	$t_item = 0;
	while ($item_line =~ /,/g) { $t_item++; }
	if ($F{'ps'} eq $adps)	    { $error = 1 }
	if (&get_crypt($F{'ps'},$pass)) { $error = 1 }
	&error("密碼錯誤") if !$error;
	$getmeflag = 1;
}

# Sub Get U #
sub get_u {
	undef $dead;
	my $save = $_[1] ? 'read' : 'save';
	$Ufile = new Nfile("$usrdir\/$_[0]\.dat",$save);
	@ulines = $Ufile->read;
	if ($ulines[0] eq "Read Error") { &fr_del($_[0]); }
	return(0) if $dead;
	my $userline = shift(@ulines);
	($uid,$uname,$upass,$usex,$umoney,$uatk,$ucmd,$unav,$uadven,$upiracy,$utrade,$ufood,$usailor,$uload,$uship_line,
	 $uarea,$uport,$upoint,$utactics,$urecord,$uquest_flag,$uquest_line,$ufriend_line,$ubattle_line,
	 $ulast,$umoved,$uend_quest,$uintro,$umail,$uurl,$uhost,$uos,$uip,$ubz,$uaction,$uitem_line,$ucity_line,$ureserv,$uaexp,$upexp,$utexp) = split(/<>/,$userline);
	@uship_ind = split(/△/,$uship_line);
	$ut_item = 0;
	while ($uitem_line =~ /,/g) { $ut_item++; }
	return(1);
}


# Sub Set Me #
sub set_me {
	$ship_line = join('△',@ship_ind);
	my $userline  = join('<>',$id,$name,$pass,$sex,$money,$atk,$cmd,$nav,$adven,$piracy,$trade,
				$food,$sailor,$load,$ship_line,$area,$port,$point,$tactics,
				$record,$quest_flag,$quest_line,$friend_line,$battle_line,
				$last,$moved,$end_quest,$intro,$mail,$url,$host,$os,$ip,$bz,$action,$item_line,$city_line,$reserv,$aexp,$pexp,$texp,"\n");
	unshift (@ilines,$userline);
	if (!$id || $#ilines < 0) { return }
	$Myfile->write(@ilines);
	undef $getmeflag;
}

# Sub Set U #
sub set_u {
	$uship_line = join('△',@uship_ind);
	my $userline  = join('<>',$uid,$uname,$upass,$usex,$umoney,$uatk,$ucmd,$unav,$uadven,$upiracy,$utrade,
				$ufood,$usailor,$uload,$uship_line,$uarea,$uport,$upoint,$utactics,
				$urecord,$uquest_flag,$uquest_line,$ufriend_line,$ubattle_line,
				$ulast,$umoved,$uend_quest,$uintro,$umail,$uurl,$uhost,$uos,$uip,$ubz,$uaction,$uitem_line,$ucity_line,$ureserv,$uaexp,$upexp,$utexp,"\n");
	unshift (@ulines,$userline);
	if (!$uid || $#ulines < 0) { return }
	$Ufile->write(@ulines);
}

# Sub Get All Users #
sub get_all_users {
	return if $getallusersflag;
	opendir(DIR,"$usrdir") || &error("ユーザデータ讀取錯誤:$usrdirという名前のユーザデータ用ディレクトリが無いかパーミッションが不正です");
	@userfiles = sort grep /\.dat/,readdir(DIR);
	closedir(DIR);
	foreach (@userfiles) {
		open(IN,"$usrdir\/$_") || &error("\/$_無法開啟");
		$line = <IN>;
		push(@alllines,$line);
		close(IN);
	}
	$getallusersflag = 1;
}

# Sub Friend Delete #
sub fr_del {
	$dead = 1;
	if ($F{'id'}) {
		&get_me($F{'id'});
		my @friend = split(/△/,$friend_line);
		@friend = grep { $_[0] != (split(/,/))[0] } @friend;
		$friend_line = join('△',@friend);
		&set_me;
		&error("$_[0]帳戶不存在")
	}
	else { &error("$_[0]帳戶不存在") }
}

# Sub Get Cryptogram #
sub get_crypt {
	if (!$def_cp) { if ($_[0] eq $_[1]) { return 1 } else { return 0 } }
	my $salt  = substr($_[1],0,2);
	if ($_[1] eq crypt($_[0],$salt))	{ return 1 } else { return 0 }
}

# Sub Table #第一＝上or下、第二＝幅、第三＝境界
sub form_table {
if($_[0] eq 'up') {
print <<TAB;
	<center><form method=$method action=$seacgi>
	<table width="$_[1]" border="$_[2]" bgcolor=$t_bgcol bordercolor=$bdcol cellspacing=0>
	<tr><td align=center>
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

# Sub Submit Button #
sub submit_button {
	print qq|<input type=submit value="OK" class=button>\n|;
}

# Sub Return Button #
sub return_button {
	print qq|<center><form method=$method action=$seacgi><input type="button" value="返回" onClick="history.back()"></form></center>\n|;
}

# Sub Home Button #
sub home_button {
	if (!$def_ho) { return }
	print qq|<center><a href=$hom_url target=$hom_tgt>$hom_lbl</a><br></center>\n|;
}

# Sub ID & Password #
sub id_ps {
	print qq|<input type=hidden name=id value="$F{'id'}">\n|;
	print qq|<input type=hidden name=ps value="$F{'ps'}">\n|;
}

# Sub Reload #
sub reload {
	$action = rand(1000) if !$reloadflag;
	print qq|<input type=hidden name=reload value="$action">\n|;
	$reloadflag = 1;
}

# Sub Header #
sub header {
print <<HEAD;
Content-type: text/html

<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Content-Style-Type" content="text/css">
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
	if (!$headflag) { &header }
print <<ERR;
<center>
<hr width=80%>
<B><font color=#FF0000>$_[0]</font></B>
<hr width=80%>
</center>
ERR
	&return_button if !$def_rb;
	&footer;
	exit;
}

# Sub Get Cookie #
sub get_cookie {
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
	$c_ps = $COOKIE{'ps'}
}

# Sub Set Cookie #
sub set_cookie {
	# クッキーは未更新削除期間有効
	($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg) = gmtime(time + $def_dead*24*60*60);
	($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg) = gmtime(time + $retry*60*60) if $_[0] eq 'del';
	$yearg += 1900;
	if ($secg  < 10) { $secg  = "0$secg";  }
	if ($ming  < 10) { $ming  = "0$ming";  }
	if ($hourg < 10) { $hourg = "0$hourg"; }
	if ($mdayg < 10) { $mdayg = "0$mdayg"; }
	$month = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[$mong];
	$youbi = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')[$wdayg];
	$date_gmt = "$youbi, $mdayg\-$month\-$yearg $hourg:$ming:$secg GMT";
	$cook = "id\:$F{'id'}\,ps\:$F{'ps'}";
	print "Set-Cookie: $cookname=$cook; expires=$date_gmt\n";
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

1;
