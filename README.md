# CobaltStrike-Auto-Keystore
Automate Cobalt Strike keystore file for Teamserver SSL.

Tested on Ubuntu 20.04 Server
 - apt-get install openjdk-11-jdk
 - apt-get install certbot
 - Runs certbot standalone, creates keystore file, copies keystore file to CS directory, prints HTTPS config to copy/paste into Malleable C2 Profile.
