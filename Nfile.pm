# #############################################################
# Nfileモジュール(クラス) v1.0
# 
# Copyright (C) 2005 コスミー, All rights reserved.
# E-Mail : impulse@kun.ne.jp
# Web : http://www.kosumi.vxx.jp/
# 本スクリプトはフリーウェアです。
# 利用する方は次のURL:http://www.kosumi.vxx.jp/rules.htm
# に記載された利用規定に同意したものと見なします。
# 著作権はコスミーが保有しますが、
# 本スクリプトを利用した事によるいかなる損害も作者(コスミー)は一切の責任を負いません。
# 質問等はサポート掲示板へ(http://www.kosumi.vxx.jp/support.htm)
# 
# 利用法:
# ○Nfileモジュールの使用宣言:
# 	use Nfile;
# ○操作するファイルの指定: 'save'(自動セーブ),'read'(読み込みのみ),'new'(ファイルの新規作成)
# 	$Data = new Nfile('filename' [,'save' | 'read' | 'new']);
# ○読み込み:
# 	@all = $Data->read;
# ○書き込み:
# 	$Data->write(@all);
# ○補足
# 	・呼び出し側で$NFILEDIRを定義することで、ロックファイルをそのディレクトリ内に作成するようにできる。
# ○注意事項
# 	・「lock_Nfile」というサイズ0のファイルがロック用に作成される。
# 	・->writeを行う場合は、'new'を指定した場合か、->readを呼び出した後でなければならない。
# 	・ロックはNfileが呼び出される間、ずっとかかる。
# 	　例えば、3つのファイルをオープンした場合、3つとも->writeするまで('read'でオープンしたものを除く)、
# 	　あるいはオブジェクトが開放されるまで、ロック状態が続く。
# 	　この間、他のプロセスはどのファイルもNfileを用いて操作できない。
# #############################################################
package Nfile;

# 引数1：ファイル名,引数2：オプション'save'(自動セーブ),'read'(読み込みのみ),'new'(ファイルの新規作成)
sub new {
	my $class  = shift;
	my $file   = shift;
	my %option = map { $_ => 1 } @_;
	my $lockfile = $main::NFILEDIR ? $main::NFILEDIR . '/lock_Nfile' : 'lock_Nfile';
	
	my $self = {
		'file'     => $file,
		'imflock'  => 0,
		'read_end' => 0,
		'write_end'=> 0,
		'save'     => $option{'save'},
		'read'     => $option{'read'},
		'new'      => $option{'new'},
		'lockkey'  => 2,
		'handle'   => undef,
		'lines'    => undef,
		'lockfile' => $lockfile
	};
	
	bless $self, $class;
	
	# Nfileオブジェクトの数をカウント
	if (!$Nfile_CALL) {
		$Nfile_CALL = 1;
		$self->lock;
		eval {
			open(TRUN, ">TruncateCheck_Nfile") || return $self;
			truncate(TRUN, 0);
			close(TRUN);
			CORE::unlink("TruncateCheck_Nfile") || return $self;
		};
		if ($@) {
			$ImpossibleTruncate;
		}
	} else {
		$Nfile_CALL++;
	}
	
	return $self;
}

sub DESTROY {
	my $self = shift;
	
	if ($self->{'save'} && $self->{'read_end'} && !$self->{'write_end'}) {
		$self->write(@{$self->{'lines'}});
	}
	$self->close_dat;
	
	return;
}

# Sub Read Data #
sub read {
	my $self = shift;
	
	if (!$self->{'read_end'}) {
		if ($self->open_dat) {
			return "Read Error";
		}
		
		$self->{'read_end'}  = 1;
		$self->{'write_end'} = 0;
		
		my $handle = $self->{'handle'};
		@{$self->{'lines'}} = <$handle>;
		if ($self->{'read'}) {
			$self->close_dat;
		}
	}
	return @{$self->{'lines'}};
}

# Sub Write Data #
sub write {
	my $self = shift;
	
	if (!$self->{'write_end'}) {
		if ($self->{'new'}) {
			if ($self->new_open) {
				return "Write Error";
			}
		}
		seek($self->{'handle'},0,0);
		
		if (!$ImpossibleTruncate) {	# truncateできるとき
			my $handle = $self->{'handle'};
			print $handle @_;
			truncate($handle, tell($handle));
		} else {	# truncateできないとき
			close($self->{'handle'});
			open($self->{'handle'},">$self->{'file'}") || return("Write Error");
			my $handle = $self->{'handle'};
			print $handle @_;
		}

		
		$self->close_dat;
		
		$self->{'write_end'} = 1;
	}

	return;
}

# Sub New Open #
sub new_open {
	my $self = shift;
	
	open($self->{'handle'}, ">$self->{'file'}") || return("Open Error");
		
	return undef;
}

# Sub Open Data #
sub open_dat {
	my $self = shift;
	return "No File" if !(-e $self->{'file'});
	my $open_method = $self->{'read'} ? $self->{'file'} : "+<$self->{'file'}";
	
	open($self->{'handle'}, $open_method) || return("Open Error");
	
	return undef;
}

# Sub Close Data #
sub close_dat {
	my $self = shift;
	
	if ( defined($self->{'handle'}) ) {
		close($self->{'handle'});
		undef $self->{'handle'};
	} else {
		return;
	}
	
	$Nfile_CALL--;
	if (!$Nfile_CALL) {
		$self->unlock;
	}
	return;
}

# Sub Set Data #
sub set_data {
	my $self = shift;
	
	@{$self->{'lines'}} = @_;
	$self->{'write_end'} = 0;
	return;
}

#TC ver
sub ver {
	$net_sail272tc ='by bsm';
}

# Sub Lock #
sub lock {
	my $self = shift;
	return if !$self->{'lockkey'};
	my $lockfile = $self->{'lockfile'};
	eval {
		open(LOCK, ">$lockfile") || return("Lock Err");
		flock(LOCK, 2);
	};
	my $flockerr = $@;
	if ($flockerr) {
		$self->{'imflock'} = 1;
		$self->unlock if (-e $lockfile) && (time - (stat($lockfile))[9] > 300);
		my $retry = 100;
		eval {
			while (!symlink(".",$lockfile)) {
				--$retry or return("Busy");
				select(undef,undef,undef,0.1);
			}
			$self->{'lockkey'} = 2;
		};
		if ($@) {
			while (!mkdir($lockfile,606)) {
				--$retry or return("Busy");
				select(undef,undef,undef,0.1);
			}
			$self->{'lockkey'} = 1;
		}
	}

	return;
}

# Sub Unlock #
sub unlock {
	my $self = shift;
	my $lockfile = $self->{'lockfile'};
	if ($self->{'imflock'}) {
		if    ($self->{'lockkey'} == 1) { rmdir($lockfile)  }
		elsif ($self->{'lockkey'} == 2) { unlink($lockfile) }
	} else {
		close(LOCK);
	}
	return;
}

1;
