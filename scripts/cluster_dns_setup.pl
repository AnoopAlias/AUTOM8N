#!/usr/local/cpanel/3rdparty/bin/perl

#Author: Rajiv C.J.
#Purpose: Adding and removing A records for domains using cPanel API
use strict;
use LWP::UserAgent;
use LWP::Protocol::https;
use Cpanel::JSON::XS qw(encode_json decode_json);
my $hash;
 if ( -e "/root/.accesshash")
 {
  $hash = `cat /root/.accesshash`;
  $hash =~ s/\n//g;
 }
 else
 {
   print "Unable to locate .accesshash.Please generate one from WHM"
 }
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
         print "Invalid num of args\n";
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
         print "Invalid num of args\n";
        }
   }


else
{
 print "Invalid task provided\n";
}

sub adddns
{
  my $auth = "WHM root:" . $hash;
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
   print $result->{metadata}{reason},"\n";
  }
}

sub deldns
{
 my $auth = "WHM root:" . $hash;
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
 my $found;
  foreach my $record ( @{ $result->{result}[0]{record} } )
  {
   $address = $record->{address};
   if ($address =~ $ip)
   {
    $line = $record->{Line};
    $found +=1;
   }
  }
  if ($found)
  {
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
     print $result->{metadata}{reason},"\n";
    }
  }
  else
  {
    print "Record not found\n";
    exit;
  }
}
