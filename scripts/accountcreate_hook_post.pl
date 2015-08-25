#!/usr/bin/perl
use IO::Select;
use JSON::Syck;
use Data::Dumper;

open(FH, ">>/opt/nDeploy/hook.log");
$input = get_passed_data();
my ( $result_status, $result_msg ) = do_something($input);

print "$result_status $result_msg";
exit;
 
sub do_something {
	my ($ref) = @_;
	my %input = %$ref;
	my ( $status, $msg );
	
	system("/opt/nDeploy/scripts/generate_config.py ".$input{'data'}{'user'});
	system("/opt/nDeploy/scripts/apache_php_config_generator.py ".$input{'data'}{'user'});
	system("/etc/init.d/ndeploy_backends restart");
	system("/opt/nDeploy/scripts/reload_nginx.sh");
	
	$status = 1;
	$msg    = "Successful.";
	return $status, $msg;
}
 
sub get_passed_data {
	my $raw_data   = '';
	my $input_data = {};
	my $selects    = IO::Select->new();
	$selects->add( \*STDIN );
	if ( $selects->can_read(.1) ) {
		while (<STDIN>) {
			$raw_data .= $_;
		}
		$input_data = JSON::Syck::Load($raw_data);
	}
	print FH Dumper($input_data);
	return $input_data;
}