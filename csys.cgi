# Sub Get City #
sub get_city {
	$CityFile = new Nfile("$citydir/$port\.dat",'save');
	($cityline) = $CityFile->read;
	if ($cityline eq "Read Error") { &check_city; }
	if ($no_city) { return }
	if (!$cityline) { &error("City file 讀取錯誤") }
	($owner,$owname,$cname,$chp,$cmoney,$cload,$cship,$citem,$cintro,$crate,$csell,$buyer) = split(/<>/,$cityline);
}

# Sub Set City #
sub set_city {
	$cityline = join('<>',$owner,$owname,$cname,$chp,$cmoney,$cload,$cship,$citem,$cintro,$crate,$csell,$buyer);
	$CityFile->write($cityline);
}

# Sub Check City #
sub check_city {
	$no_city = 1;
}

1;