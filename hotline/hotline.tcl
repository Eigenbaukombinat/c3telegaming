#!/usr/bin/tclsh
package require ygi

set sounds "/usr/local/share/yate/sounds"

::ygi::start_ivr
::ygi::set_dtmf_notify

::ygi::idle_timeout

::ygi::play_wait "$sounds/yintro"
::ygi::sleep 500

while { true } {
  set digit [::ygi::play_getdigit file "$sounds/pocmenu/123"]
  if { $digit == "1" } {
       ::ygi::play_getdigit file "$sounds/pocmenu/warteschleife" stopdigits { 3 }
  }
  
  if { $digit == "2" } {
       ::ygi::play_getdigit file "$sounds/pocmenu/clan_chi_telekom" stopdigits { 3 }
  }

}
