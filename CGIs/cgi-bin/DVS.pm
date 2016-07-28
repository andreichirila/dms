package DVS;

use Exporter;

@ISA= qw (Exporter);
@EXPORT = qw (dbConnect MACdbConnect);


#$debug=1;      # Enable this line to produce tons of Debug information

#===========================================================================
# Make the Database connection and give handle back to caller
#===========================================================================

sub dbConnect {
        #=========================================================================
        # Global Configuration Variables should go out of this file
        #=========================================================================
        $dbserver="192.168.7.178";
        $database="CameronetDokVer";
        $dbuser="root";
        $dbpass="xebative123";
        #=========================================================================
        $connect_str = "DBI:mysql:$database:$dbserver";
        my $mdbh = DBI->connect("$connect_str",$dbuser,$dbpass);
        return($mdbh);
}


