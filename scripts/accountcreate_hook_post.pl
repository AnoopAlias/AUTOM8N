#!/usr/bin/perl
use IO::Select;
use JSON::Syck;
use Data::Dumper;
use YAML::Tiny;

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
	
	my $user_data_file = "/opt/nDeploy/user-data/".$input{'data'}{'user'};
	my $udf_parsed = YAML::Tiny->read($user_data_file);
	
	my $php_ver = $udf_parsed->[0]->{'PHP'};
	
	system("/opt/nDeploy/scripts/init_backends.pl --action=reload --php=".$php_ver);
	system("/opt/nDeploy/scripts/reload_nginx.sh 2>&1");
	
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