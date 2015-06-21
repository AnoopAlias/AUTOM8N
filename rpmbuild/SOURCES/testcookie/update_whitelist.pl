#!/usr/bin/env perl

# http://www.iplists.com/

system("rm whitelist_ips.txt");

our @list;
our @urls = (
	'http://www.iplists.com/google.txt',
	'http://www.iplists.com/inktomi.txt',
	'whitelist_ips.custom.txt'
);

sub parse {
	my $url = shift;
	my @result;
	if($url =~ /^http:\/\//) {
		my $curl = `curl $url 2>/dev/null`;
		foreach(split(/\n/, $curl)) {
			if($_ =~ /^#/) {next;}
			push(@result, $_);
		}
	} else {
		open(FH, "<$url");
		foreach(<FH>) {
			if($_ =~ /^#/) {next;}
			chomp($_);
			push(@result, $_);
		}
		close(FH);
	}
	return @result;
}

foreach(@urls) {
	my @result = parse($_);
	push(@list, @result);
}

open(FH, ">whitelist_ips.txt");
foreach(@list) {
	$_ =~ s/^([0-9]+\.[0-9]+\.[0-9]+)$/\1.0\/24/;
	#print $_.";\n";
	print FH $_.";\n";
}
close(FH);