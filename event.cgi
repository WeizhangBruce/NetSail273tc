# Sub Event Write #
sub event_write {
	&get_date(time) if !$date;
	my $EventFile = new Nfile($eventdat,'save');
	my @eventlines = $EventFile->read;
	if (@eventlines >= $def_om) { pop @eventlines; }
	unshift (@eventlines,"[$date] $_[0]\n");
	$EventFile->write(@eventlines);
}

1;