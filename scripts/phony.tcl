#!/usr/bin/tclsh
package require ygi

set path_sounds "/usr/local/share/yate/sounds"
set path_script [file dirname [info script]]

::ygi::start_ivr
::ygi::set_dtmf_notify
::ygi::idle_timeout

set client 172.17.0.1
set port 1234

set caller_id $ygi::env(caller)

#play audio einleitenden worte
::ygi::play_wait "$path_sounds/yintro"
::ygi::sleep 500
::ygi::log "START"

while { true } {
  set digit [::ygi::getdigit]
  ::ygi::log "$caller_id send $digit"
  exec echo -n $digit | nc -u -q 0 $client $port
}
