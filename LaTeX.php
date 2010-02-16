<?php
$wgExtensionFunctions[] = 'efLatex_Setup';

function efLatex_Setup(){
	global $wgParser;
	$wgParser->setHook( 'latex', 'efLatex_Render' );
}

function efLatex_Render( $input, $args, $parser, $frame ) {
		global $wgTmpDirectory;
        $dir = dirname(__FILE__);
		$cmd = $dir.'/plastex_mediawiki.py '.$wgTmpDirectory;
		//$cmd = $dir.'/plastex_mediawiki.py';
        $descriptorspec = array(
           0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
           1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
           2 => array("pipe", "w")   // stderr is a pipe to write to
        );
        
        $env = array('some_option' => 'aeiou');
        $process = proc_open($cmd, $descriptorspec, $pipes, $dir, $env);
        
        if (is_resource($process)) {
            fwrite($pipes[0], $input); fclose($pipes[0]);
            $output = stream_get_contents($pipes[1]); fclose($pipes[1]);
            $return_value = proc_close($process);
        }
		return $parser->recursiveTagParse($output, $frame );
		//return $output;
}

?>
