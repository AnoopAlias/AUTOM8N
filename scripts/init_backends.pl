#!/usr/bin/env perl

#use strict;

use warnings;
use YAML::Tiny;
use Getopt::Long;
use Data::Dumper;

my $installation_path = '/opt/nDeploy';
my $backend_config_file = $installation_path.'/conf/backends.yaml';
our $php_fpm_config = $installation_path.'/conf/php-fpm.conf';
my $tries = 10;

sub start{
	my $ver = shift @_;
	my $path = shift @_;
	
	system("sysctl -q -w net.core.somaxconn=4096");
	
	my $php_bin = $path.'/sbin/php-fpm';
	my $php_conf_d = $path.'/etc/php-fpm.d';
	my $retry=$tries;
	
	print "Starting $ver: ";
	do {
		system($php_bin.' --fpm-config '.$php_fpm_config.' >/dev/null 2>&1');
		$? = $? >> 8;
		$retry--;
		print ". ";
		sleep(1);
	} while($? != 0 && $retry>0);
	if($? eq 0) {
		print "started\n";
	} else {
		print "cant start (exitcode=$?)\n";
	}
}

sub stop{
	my $ver = shift @_;
	my $path = shift @_;
	my $php_pidfile = $path.'/var/run/php-fpm.pid';
	my $type;
	
	my $pid;
	open(FH, "<$php_pidfile") or return;
	while(<FH>) {$pid .= $_;}
	close(FH);
	$pid = int($pid);
	
	if($pid <= 1) {print "Cant graceful stop $ver (pid=$pid)\n";}
	if($forced) {
		kill(TERM, $pid);
		$type='Forced';
	} else {
		kill(QUIT, $pid);
		$type='Graceful';
	}
	if($? eq 0) {
		print "$type stop successful $ver (pid=$pid)\n";
	} else {
		print "Cant $type stop $ver (exitcode=$?, pid=$pid)\n";
	}
}

sub reload{
	my $ver = shift @_;
	my $path = shift @_;
	my $php_pidfile = $path.'/var/run/php-fpm.pid';
	
	my $pid;
	open(FH, "<$php_pidfile") or return;
	while(<FH>) {$pid .= $_;}
	close(FH);
	$pid = int($pid);
	
	if($pid <= 1) {print "Cant reload $ver (pid=$pid)\n";}
	kill(USR2, $pid);
	if($? eq 0) {
		print "Reload successful $ver (pid=$pid)\n";
	} else {
		print "Cant reload $ver (exitcode=$?, pid=$pid)\n";
	}
}

my ($action, $help, $php_ver);
our $forced;
GetOptions (
	"action=s" => \$action,
	"help"     => \$help,
	"forced"   => \$forced,
	"php=s"    => \$php_ver
);

# Open the config
our $backends = YAML::Tiny->read($backend_config_file);

unless($action && !$help) {
	print "Usage $0 --action=<start/stop/restart/reload> [--php=<phpver>] [--forced]\n";
	exit 1;
}

my $ref_php = $backends->[0]->{'PHP'};
my %php = %$ref_php;

for my $ver (keys %php) {
	if($php_ver && $ver !~ /$php_ver/) {
		next;
	}
	if($action eq "start") {
		&start($ver, $php{$ver});
	} elsif($action eq "stop") {
		&stop($ver, $php{$ver});
	} elsif($action eq "restart") {
		&stop($ver, $php{$ver});
		&start($ver, $php{$ver});
	} elsif($action eq "reload") {
		&reload($ver, $php{$ver});
	}
}