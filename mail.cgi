# Sub Mail Form #
sub mail_form {
	&get_me($F{'id'},'read');
	&header;
	&title;
	&table('up','95%',1);
	&label('傳遞訊息');
	print qq|訊息已傳送至$uname<br><br>\n| if $uname;
	@friend = split(/△/,$friend_line);
	print qq|要送出訊息給誰？|;
	print qq|<form method=$method action=$listcgi><input type=hidden name=mode value='mail_check'>\n|;
	print qq|<input type=hidden name=id value="$F{'id'}"><input type=hidden name=ps value="$F{'ps'}"><input type=submit value='檢查友人' class=button></form>\n|;
	print qq|<hr class=text><form method=$method action=$listcgi>\n|;
	print qq|<input type=radio name=uid value="admin">　 管理者<br>\n|;
	foreach (0 .. $#friend) {
		($mid,$mnm) = split(/,/,$friend[$_]);
		print qq|<input type=radio name=uid value="$mid">|;
		print qq|　 <a href="$listcgi?mode=uprofile&uid=$mid&return=1">$mnm</a><br>\n|;
	}
	print qq|<hr class=text>\n|;
	print qq|<textarea name=message cols=30 rows=5 class=text></textarea><br>\n|;
	print qq|資金援助：<input type=text name=quan size=10> G<br>\n|;
	my @item_ind = split(/,/,$item_line);
	if ($#item_ind >= 0) {
		print qq|<input type=checkbox name="sell" value="1">\n|;
		print qq|贈送財寶：<select name="give">|;
	}
	foreach (0 .. $#item_ind) {
		print qq|<option value="$_">$item_ind[$_]|;
	}
	print qq|</select>| if $#item_ind >= 0;
	print qq|<input type=hidden name=mode value='send_mail'>\n|;
	print qq|<input type=hidden name=id value="$F{'id'}">\n|;
	print qq|<input type=hidden name=ps value="$F{'ps'}">\n|;
	&submit_button;
	print qq|</form>\n|;
	&table('down');
	print qq|<br>\n</body></html>\n|
}

# Sub Send Mail #
sub send_mail {
	&error("訊息的文字長度須在半形 $def_ml 個字之內") if length $F{'message'} > $def_ml;
	&error("未輸入內容") if !$F{'message'};
	&error("請先選擇對象") if !$F{'uid'};
	$F{'message'} =~ s/<br>//g;
	&get_me($F{'id'});
	if ($F{'uid'} eq 'admin') {
		my $AdMail = new Nfile("$datadir/admin.dat");
		my @mailline = $AdMail->read;
		&get_date(time) if !$date;
		pop(@mailline) if @mailline >= 50;
		unshift(@mailline,"[$date] $name：「$F{'message'}」\n");
		$AdMail->write(@mailline);
		$uname = "管理者";
		&mail_form
	} else {
		#Ver2.73
		if (!&uid_check($friend_line, $F{'uid'})) {
			&error("不正確的呼叫");
		}
		#
		if ($F{'quan'}) {
			&error("援助金輸入錯誤") if $F{'quan'} =~ /[^0-9]/;
			$aid = int($F{'quan'});
			&error("資金不足") if $aid > $money;
		}
		&get_u($F{'uid'});
		if ($dead) {
			&header;
			&table('up','95%',1);
			print qq|收件人不存在\n|;
			&return_button("mail_form",'','button');
			&table('down');
			print qq|<br>\n</body></html>\n|;
			exit
		}
		if (($F{'quan'} || $F{'sell'}) && $host eq $uhost && $os eq $uos && $bz eq $ubz && $host) { &error("你不能送援助金、財寶給對方") }
		if ($F{'sell'}) {
			my @item_ind = split(/,/,$item_line);
			&error("沒發現財寶") if $#item_ind < 0;
			my @uitem_ind = split(/,/,$uitem_line);
			foreach (@uitem_ind) { &error("$uname已經持有此寶物") if $_ eq $item_ind[$F{'give'}] }
			&add_record("$uname $item_ind[$F{'give'}] 獻上");
			$urecord .= qq|$name 贈與財寶＜$item_ind[$F{'give'}]＞給你<br>|;
			&add_record("$name 財寶＜$item_ind[$F{'give'}]＞受領",1);
			$uitem_line = join(',',@uitem_ind,$item_ind[$F{'give'}]);
			splice(@item_ind , $F{'give'} , 1);
			$item_line = join(',' ,@item_ind);
		}
		if ($aid) {
			$money -= $aid;
			$umoney += $aid;
			&add_record("援助$uname $aid G");
			&add_record("$name $aid G援助金送達",1);
			$urecord .= "收到援助金<br>";
		}
		&set_me;
		&add_record("$name：「$F{'message'}」",1);
		$urecord .= "收到訊息<br>";
		&set_u;
		&mail_form
	}
}
#Ver2.73
sub uid_check {
	my $found = 0;
	my @friend_check = split(/△/,$_[0]);
	foreach (0 .. $#friend_check) {
		my ($uid_chk,$unm_chk) = split(/,/,$friend_check[$_]);
		if ($uid_chk == $_[1]) {
			$found = 1;
			last;
		}
	}
	return $found;
}
##

# Sub Mail Check #
sub mail_check {
	&get_me($F{'id'});
	@friend = split(/△/,$friend_line);
	foreach (@friend) {
		($mid,$mnm) = split(/,/);
		open(IN,"$usrdir\/$mid\.dat") || next;
		$fline = <IN>;
		close(IN);
		($fid,$fname) = split(/<>/,$fline);
		if ($mnm ne $fname) { next }
		push(@alive,$_)
	}
	$friend_line = join('△',@alive);
	&set_me;
	&mail_form;
}

# Sub Submit Button #
sub submit_button {
print <<SUBMIT;
<div align=right>
<input type=submit value="$sub_lbl" class=button>
</div>
SUBMIT
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

# Sub Get Date #
sub get_date {
	($sec,$min,$hour,$day,$month,$year) = localtime($_[0]);
	$year += 1900;
	$month++;
	$date   = sprintf("%04d\/%02d\/%02d",$year,$month,$day);
}

1;