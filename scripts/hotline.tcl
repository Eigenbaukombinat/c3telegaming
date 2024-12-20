#!/usr/bin/tclsh
package require ygi

# paths
set sounds "/usr/local/share/yate/sounds"
set scripts [file dirname [info script]]

# Phony config
set phony_host 172.17.0.1
set phony_port 1234

# Caller information
set caller_id $ygi::env(caller)

::ygi::start_ivr
::ygi::set_dtmf_notify

# Grund warum ich nach X minuten raus fliege?

::ygi::idle_timeout 

::ygi::play_wait "$sounds/yintro"
::ygi::sleep 500

while { true } {
  set digit [::ygi::play_getdigit file "$sounds/hotline_auswahl.slin"]
  if { $digit == "1" } {
      ::ygi::log "$caller_id send $digit"
      exec echo -n $digit | nc -u -q 0 $client $port
      #::ygi::play_getdigit file "$sounds/pocmenu/warteschleife" stopdigits { 3 }
  }
  
  if { $digit == "2" } {
      ::ygi::play_getdigit file "$sounds/pocmenu/clan_chi_telekom" stopdigits { 3 }
  }

}
