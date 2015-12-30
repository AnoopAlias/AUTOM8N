#!/usr/local/cpanel/3rdparty/bin/perl

#Author: Rajiv C.J
#Purpose: Adding and removing A records for domains using cPanel API
use strict;
use LWP::UserAgent;
use LWP::Protocol::https;
use MIME::Base64;
use Cpanel::JSON::XS qw(encode_json decode_json);
use Data::Dumper;


my $user = "root";
my $pass = "n?m}9(b4^gB3>1.I";
#This script accepts 3 arguments ( add/del,domain name,ip)
my $count_args = $#ARGV + 1;
my $task = $ARGV[0];
my $domain = $ARGV[1];
my $ip = $ARGV[2];

 if ( $task eq "add" )
 {
        if ( $count_args == 3 )
         {
           adddns();
         }
        else
        {
         print "invalid num of args";
        }
 }
   elsif ( $task eq "del" )
   {
     if ( $count_args == 3 )
         {
           deldns();
         }
        else
        {
         print "invalid num of args";
        }
    print "Del branch";
   }


else
{
 print "Invalid task provided";
}

sub adddns
{
 my $auth = "Basic " . MIME::Base64::encode( $user . ":" . $pass );
 my $ua = LWP::UserAgent->new(
    ssl_opts   => { verify_hostname => 0, SSL_verify_mode => 'SSL_VERIFY_NONE', SSL_use_cert => 0 },
 );
 my $request = HTTP::Request->new( GET => "https://127.0.0.1:2087/json-api/addzonerecord?api.version=1&domain=$domain&name=$domain.&type=A&address=$ip" );
 $request->header( Authorization => $auth );
 my $response = $ua->request($request);
 my $result = $response->content;
 $result = decode_json $result;
 my $status = $result->{metadata}{result};
  if ( $status )
  {
   print "Successfully added the A record\n";
  }
  else
  {
   print $result->{metadata}{reason};
  }
}

sub deldns
{
 my $auth = "Basic " . MIME::Base64::encode( $user . ":" . $pass );
 my $ua = LWP::UserAgent->new(
    ssl_opts   => { verify_hostname => 0, SSL_verify_mode => 'SSL_VERIFY_NONE', SSL_use_cert => 0 },
 );
 my $request = HTTP::Request->new( GET => "https://127.0.0.1:2087/json-api/dumpzone?domain=$domain");
 $request->header( Authorization => $auth );
 my $response = $ua->request($request);
 my $result = $response->content;
 $result = decode_json ($result);
 my $address;
 my $line;
  foreach my $record ( @{ $result->{result}[0]{record} } )
  {
   $address = $record->{address};
   if ($address =~ $ip)
   {
    $line = $record->{Line};
   }
  }
 $request = HTTP::Request->new( POST => "https://127.0.0.1:2087/json-api/removezonerecord?api.version=1&zone=$domain&line=$line");
 $request->header( Authorization => $auth );
 $response = $ua->request($request);
 $result = $response->content;
 $result = decode_json ($result);
 my $status = $result->{metadata}{result};
  if ( $status )
  {
   print "Successfully removed the record\n";
  }
  else
  {
   print $result->{metadata}{reason};
  }
}
