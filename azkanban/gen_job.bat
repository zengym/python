@echo off

if exist xx.zip del xx.zip

WINRAR a -r xx.zip *.job *.sh *.properties

exit