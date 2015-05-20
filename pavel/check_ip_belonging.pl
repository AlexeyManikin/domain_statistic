#!/usr/bin/perl

use strict;
use warnings;

use Net::Patricia;

die unless scalar @ARGV == 2;

my ($our_subnets, $file_with_ips) = @ARGV;

open my $subnets_file, "<", $our_subnets or die "Can't open file";
my $pt = new Net::Patricia;

# Build lookup tree
for my $subnet (<$subnets_file>) {
    chomp $subnet;
    
    if ($subnet =~ /^#/) {
        next;
    }
   
    $pt->add_string($subnet); 
}

close $subnets_file;

open my $ips_file, "<", $file_with_ips or die "Can't open IPs file";
my $total_lines = 0;
my $matched_lines = 0;
for my $line (<$ips_file>) {
    chomp $line;
    
    unless ($line =~ /^\d/) {
        next;
    }

    $total_lines++;

    if ($pt->match_string($line)) {
        $matched_lines++;
    }
}

print "Total lines: $total_lines Total matched lines: $matched_lines\n";
