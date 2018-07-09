@echo off

if exist userprofile.zip del userprofile.zip

WINRAR a -r userprofile.zip *.job *.sh *.properties

exit