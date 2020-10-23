###############################################################################
#
# IssInfo module implementation
#
###############################################################################


#
# This is the namespace in which all functions and variables below will exist.
# The name must match the configuration variable "NAME" in the
# [ModulePropagationMonitor] section in the configuration file. The name may
# be changed but it must be changed in both places.
#
namespace eval IssInfo {

#
# Check if this module is loaded in the current logic core
#
if {![info exists CFG_ID]} {
  return;
}


#
# Extract the module name from the current namespace
#
set module_name [namespace tail [namespace current]];


#
# A convenience function for printing out information prefixed by the
# module name
#
proc printInfo {msg} {
  variable module_name;
  puts "$module_name: $msg";
}

#
# A convenience function for calling an event handler
#
proc processEvent {ev} {
  variable module_name
  ::processEvent "$module_name" "$ev"
}


#
# Executed when this module is being activated
#
proc activateInit {} {
  printInfo "Module activated"
}


#
# Executed when this module is being deactivated.
#
proc deactivateCleanup {} {
  printInfo "Module deactivated"
}


#
# Executed when a DTMF digit (0-9, A-F, *, #) is received
#
proc dtmfDigitReceived {char duration} {
  printInfo "DTMF digit $char received with duration $duration milliseconds";
}


#
# Executed when a DTMF command is received
#
proc dtmfCmdReceived {cmd} {
  #printInfo "DTMF command received: $cmd";

  if {$cmd == "0"} {
    processEvent "play_help"
  } elseif {$cmd == ""} {
    deactivateModule
  } else {
    processEvent "unknown_command $cmd"
  }
}

#
# Play actual Info
#
proc playActualInfo {} {
  variable files
  variable tfile
  variable sortlist
  variable outfile
  variable filearray
  variable CFG_PLAY_DIR
  variable minute
  variable hour
  variable callsign

    playSilence 200
    CW::play "ISS"
    playSilence 200
    playMsg "message"
    playSilence 500
    CW::play "QRU"
}

#
# Executed when a DTMF command is received in idle mode. That is, a command is
# received when this module has not been activated first.
#
proc dtmfCmdReceivedWhenIdle {cmd} {
  printInfo "DTMF command received while idle: $cmd";
}


#
# Executed when the squelch open or close. If it's open is_open is set to 1,
# otherwise it's set to 0.
#
proc squelchOpen {is_open} {
  if {$is_open} {set str "OPEN"} else {set str "CLOSED"};
#  printInfo "The squelch is $str";
}


#
# Executed when all announcement messages has been played.
# Note that this function also may be called even if it wasn't this module
# that initiated the message playing.
#
proc allMsgsWritten {} {
  #printInfo "all_msgs_written called...";
}


#
# Verzeichnis prüfen auf neue Verkehrsmitteilungen
# und die vorhandenen Dateien entsprechen bearbeiten
#
proc check_dir {dir} {
  variable CFG_SPOOL_DIR
  variable CFG_PLAY_DIR
  variable CFG_DELETE_AFTER
  variable CFG_ALERT
  set alert $CFG_ALERT
  set diff [expr "60 * $CFG_DELETE_AFTER"]
  set callsign $Logic::CFG_CALLSIGN

  set msg_file [glob -nocomplain -directory "$CFG_SPOOL_DIR/" message.wav]

  if {[llength $msg_file] > 0} {

    if {$alert == 1} { 
      playAlertSound;
      playSilence 200
      CW::play "ISS"
    }

    foreach message $msg_file {
       playSilence 500
       file rename -force "$CFG_SPOOL_DIR/message.wav" "$CFG_PLAY_DIR/message.wav"
       playMsg "message"
       
    }
    CW::play "QRU";
    playSilence 200
  }
}


#
# executes the function weatherinfo
#
proc check_for_overflights {} {
  check_dir issinfo
}

append func $module_name "::check_for_overflights";
Logic::addTimerTickSubscriber $func;


# end of namespace
}


#
# This file has not been truncated
#
