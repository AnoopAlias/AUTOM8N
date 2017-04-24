ChangeLog
====================

XtendWeb version 4.2.x ( 13 March 2017 )
----------------------------------------------

This version brings in lot of improvements and fix a lot of bugs, major ones being

1. Removal of Password protected location blocks as this conflicts with the subdir location

2. Change in SubDir include filename

3. Fix file permission of combined SSL files

4. Various UI improvement

5. Option to set 301 and 307 redirect from the UI

If you are upgrading from a previous release do the following
---------------------------------------------------------------
1. if you have Custom app template having subdir jinja2 logic - Remove the code from the template as this is now handled in server.j2

2. Remove the expire setting like below from any custom template as this is now handled in server.j2
`location ~* \.(?:jpg|jpeg|gif|png|ico|cur|gz|svg|svgz|mp4|ogg|ogv|webm|htc)$ {}`

3. Run /opt/nDeploy/scripts/attempt_autofix.sh postt upgrade and editing of custom template if any

4. Because of the way Auth Basic password protected URI is handled . You should re-enable password protection for the folder from UI
